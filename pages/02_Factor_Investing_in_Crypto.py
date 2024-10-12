import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# Add references section with clickable links
st.subheader("References")
st.markdown("""
[1] [Liu, Y., & Tsyvinski, A. (2018). Risks and Returns of Cryptocurrency. The Review of Financial Studies.](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)  
[2] [Liu, Y., Tsyvinski, A., & Wu, X. (2022). Common Risk Factors in Cryptocurrency. The Journal of Finance.](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13119)
""")