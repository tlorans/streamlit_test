import streamlit as st
import pandas as pd
import plotly.graph_objects as go



st.set_page_config(page_title="Worth the Effort")

st.title("Worth the Effort?")

st.subheader("Streaming Fees")

st.write("""
The Index Cooperative generates revenue through streaming fees, which are paid by users who mint and redeem index tokens.
These fees are distributed between the Index Coop and the methodologist who created the index.
""")

data = {
    'Month': ['Oct 2020', 'Nov 2020', 'Dec 2020', 'Jan 2021', 'Feb 2021', 'Mar 2021', 
              'Apr 2021', 'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021'],
    'Streaming Fees': [0, 10846, 21887, 54494, 97360, 112330, 172187, 443529, 288750, 307646, 545219, 503645],
    'Methodologist Portion':[0, 3353, 6566, 16348, 29208, 33645, 54385, 163316, 94594, 116771, 207160, 156500],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create the figure using Plotly
fig = go.Figure()

# Add Streaming Fees as the first bar in the stack
fig.add_trace(go.Bar(
    x=df['Month'],
    y=df['Streaming Fees'],
    name='Streaming Fees (Index Coop)',
    marker_color='orange'
))

# Add Methodologist Portion as the second bar in the stack
fig.add_trace(go.Bar(
    x=df['Month'],
    y=df['Methodologist Portion'],
    name='Streaming Fees (Methodologist Portion)',
    marker_color='blue'
))

# Update layout to make it a stacked bar plot
fig.update_layout(
    barmode='stack',
    title="Stacked Streaming Fees (Index Coop vs Methodologist Portion)",
    xaxis_title="Month",
    yaxis_title="Amount ($)",
    xaxis_tickangle=-45,
    template="plotly_white",
    legend_title="Revenue Sources",
    width=800,
    height=500
)

st.plotly_chart(fig)    

st.subheader("How Much Worth a Decentralized Index Protocol?")

st.write("""
The market capitalization of the Index Cooperative helps to assess the overall value of a decentralized index protocol.
The market cap is calculated by multiplying the total supply of index tokens by the current price of each token.
""")

# Load the CSV data
csv_file = 'indexcoop.csv'  # Adjust this path to match the actual path of your CSV file
df = pd.read_csv(csv_file)

# Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Create a Plotly line chart for market cap
fig = go.Figure()

# Add Market Cap line
fig.add_trace(go.Line(
    x=df['date'],
    y=df['market_cap'],
    mode='lines',
    name='Market Cap',
    marker_color='blue'
))

# Update layout
fig.update_layout(
    title="Market Cap of Index Cooperative",
    xaxis_title="Date",
    yaxis_title="Market Cap ($)",
    xaxis_tickformat='%Y-%m-%d',
    template="plotly_white",
    width=800,
    height=500
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)