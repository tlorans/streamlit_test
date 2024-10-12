import streamlit as st
import pandas as pd
import plotly.graph_objects as go



st.set_page_config(page_title="Worth the Effort")

st.title("Worth the Effort?")

st.subheader("Streaming Fees")

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

st.subheader("Token Value")

