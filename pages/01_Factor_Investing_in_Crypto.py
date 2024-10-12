import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from auth import check_password  # Import the password check


# Apply the password check
if not check_password():
    st.stop()  # Stop rendering the page if password is incorrect
    
st.set_page_config(page_title="Factor Investing")

st.title("Factor Investing in Crypto")

st.subheader("Risk Factors")

st.write("""
Liu and Tsyvinski (2018 [1]) and Liu *et al.* (2022 [2])
have shown that the cryptocurrency market is characterized by large risk premia.
These risk premia are uncorrelated with risk factors in traditional markets.
""")


# Load the data, skipping the first 5 rows and setting the header row
factors_liu = pd.read_excel("LTW_3factor.xlsx", skiprows=5)

# Define a function to convert yyww format into a proper date
def convert_yyww_to_date(yyww):
    # Convert yyww to string first, in case it's an integer
    yyww = str(yyww)
    # Extract the year and week number
    year = int(yyww[:4])
    week = int(yyww[4:])

    # Convert to date using the ISO week format
    return pd.to_datetime(f'{year}-W{week}-1', format='%Y-W%W-%w')

# Apply the function to the 'yyww' column
factors_liu = (
    factors_liu
    .assign(
        date=lambda x: x['yyww'].apply(convert_yyww_to_date)
    )
    .drop(columns=['yyww'])
    .set_index('date')
)

# Calculate cumulative returns
cum_ret = (1 + factors_liu).cumprod() - 1  # Adjust for cumulative returns formula

# Create a Plotly line chart for cumulative returns
fig = go.Figure()

# Add the cumulative returns for each factor
for col in cum_ret.columns:
    fig.add_trace(go.Line(
        x=cum_ret.index,
        y=cum_ret[col],
        name=col
    ))

# Update layout
fig.update_layout(
    title="Cumulative Returns of Risk Factors",
    xaxis_title="Date",
    yaxis_title="Cumulative Return",
    xaxis_tickangle=-45,
    template="plotly_white",
    width=800,
    height=500
)

# Display the Plotly chart
st.plotly_chart(fig)

st.subheader("Factor Replication Strategy")

st.write("""
We can replicate the factor investing strategy by constructing a portfolio based on the risk factors.
Here, we test the size factor by constructing a size portfolio based on the market capitalization of cryptocurrencies.
""")

st.write("""
         You can select the percentile for the size portfolio to test the factor investing strategy.
         Portfolios are equally weighted and rebalanced weekly.
""")


data = pd.read_csv("data.csv")

cmkt_portfolio = (data
    .get(['coin_id', 'date', 'market_cap'])  # Select relevant columns
    .groupby('date', group_keys=False)  # Group by date, and ensure the group keys are not included
    .apply(lambda x: x.nlargest(20, 'market_cap'))  # Select the top 10 coins by market cap for each date
    .assign(weight=lambda x: x['market_cap'] / x['market_cap'].sum())  # Assign weights based on market cap proportion
    .assign(strat='cmkt - 20')  # Add a strategy column
    .reset_index(drop=True)  # Reset index to flatten the DataFrame
)


# function to build the size portfolio with percentile we want to use
def build_portfolio(data, percentile):
    return (data
        .get(['coin_id', 'date', 'market_cap'])
        .groupby(['date'])
        .apply(lambda x: x.assign(size_rank=np.where(x['market_cap'] < x['market_cap'].quantile(percentile), 'small', 
                                                     np.where(x['market_cap'] > x['market_cap'].quantile(1-percentile), 'big', 'medium'))))
        .reset_index(drop=True)
        .query('size_rank == "small"')
        .groupby(['date'])
        .apply(lambda x: x.assign(
            weight= 1/len(x)
        )
        )
        .assign(strat=f'csize - {percentile*100}%')
        .reset_index(drop=True)
    )

# Radio buttons for percentile choices
user_portfolio = st.radio(
    "Select the percentile for the size portfolio", 
    options=[0.01, 0.05, 0.10, 0.20, 0.30], 
    format_func=lambda x: f'{int(x * 100)}%'  # Format the options to be shown as percentages
)

size_portfolio = build_portfolio(data, user_portfolio)

bitcoin = (data
    .query('coin_id == "bitcoin"')
    .assign(strat='bitcoin')
    .assign(weight=1)
)

portfolios = pd.concat([cmkt_portfolio, size_portfolio, bitcoin])

returns = (portfolios[["coin_id", "date", "strat", "weight"]]   # Select relevant columns
    .merge(data[['coin_id', 'date', 'ret']].assign(
        ret=lambda x: x.groupby('coin_id')['ret'].shift(-1) - 0.01 # transaction cost
    ), on=['coin_id', 'date'], how='inner')
    .groupby(['date', 'strat'])
    .apply(lambda x: (x['weight'] * x['ret']).sum())  # Calculate weighted returns
    .reset_index(name='ret')
    .assign(cum_ret=lambda x: (1 + x['ret']).groupby(x['strat']).cumprod() - 1)  # Cumulative returns
    .dropna()
)


# Define a function to calculate the performance metrics for weekly returns
def calculate_performance(returns, cmkt_mean_return=None):
    summary = {}
    
    # Annualized return (assuming weekly returns)
    summary['Mean return'] = returns.mean() * 52 * 100  # Annualized mean return
    
    # Annualized volatility (assuming weekly returns)
    summary['Volatility'] = returns.std() * np.sqrt(52) * 100
    
    # Sharpe ratio (assuming risk-free rate of 0)
    summary['Sharpe Ratio'] = (returns.mean() / returns.std()) * np.sqrt(52)
    
    # Sortino ratio
    downside_risk = returns[returns < 0].std() * np.sqrt(52)
    summary['Sortino Ratio'] = (returns.mean() / downside_risk) * np.sqrt(52)
    
    # Calmar ratio (mean return divided by max drawdown)
    max_drawdown = calculate_max_drawdown(returns) * 100  # Define max drawdown elsewhere
    summary['Calmar Ratio'] = (returns.mean() * 52) / -max_drawdown  # Negative since it's a loss
    
    # Skewness and Kurtosis
    summary['Skewness'] = returns.skew()
    summary['Kurtosis'] = returns.kurtosis()

    # Max Drawdown
    summary['Max Drawdown'] = max_drawdown
    
    # Value Added (difference from cmkt)
    if cmkt_mean_return is not None:
        summary['Value Added'] = summary['Mean return'] - cmkt_mean_return

    return pd.Series(summary)

# Function to calculate max drawdown
def calculate_max_drawdown(returns):
    cum_returns = (1 + returns).cumprod()
    peak = cum_returns.cummax()
    drawdown = (cum_returns - peak) / peak
    return drawdown.min()

# Calculate performance metrics for the cmkt portfolio
cmkt_returns = returns.query('strat == "cmkt - 20"')['ret']
cmkt_mean_return = cmkt_returns.mean() * 52 * 100  # Annualized mean return for cmkt

# Calculate performance metrics for all portfolios, adding Value Added relative to cmkt
performance_metrics = returns.groupby('strat').apply(lambda x: calculate_performance(x['ret'], cmkt_mean_return if x.name != 'cmkt - 20' else None))

# Show the calculated performance metrics for each strategy
performance_metrics = (performance_metrics.reset_index()
                       .pivot(index='strat', columns='level_1', values=0)
                       .round(2)
                       .get(['Mean return','Volatility', 'Value Added', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio', 'Max Drawdown'])
                       .fillna(0)
                       .T
)

# Display the performance metrics as a table in Streamlit
st.table(performance_metrics)

# Add the note below the table
st.write("""
**Note**: 
- All returns are in percent. 
- **Mean return** is the average annualized return.
- **Volatility** is the annualized standard deviation of the return.
- **Value Added** is the difference between the mean return and the cmkt mean return.
- **Sharpe Ratio** is the ratio of the mean return to the standard deviation of the return.
- **Sortino Ratio** is the ratio of the mean return to the downside standard deviation of the return.
- **Calmar Ratio** is the ratio of the mean return to the maximum drawdown.
- **Max Drawdown** is the maximum drawdown over the period.
""")


st.subheader("Value Proposition: A Decentralized Factor Index")

st.write("""
A decentralized factor index is a tokenized representation of a factor investing strategy.
Investors can buy and sell index tokens that track the performance of a specific factor.
         See the next page for more details about decentralized factor index protocol!
""")


# Add references section with clickable links
st.subheader("References")
st.markdown("""
[1] [Liu, Y., & Tsyvinski, A. (2018). Risks and Returns of Cryptocurrency. The Review of Financial Studies.](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)  
[2] [Liu, Y., Tsyvinski, A., & Wu, X. (2022). Common Risk Factors in Cryptocurrency. The Journal of Finance.](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13119)
""")