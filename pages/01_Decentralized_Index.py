import streamlit as st
import graphviz as gv

st.set_page_config(page_title="Decentralized Index Protocol")

st.title("Decentralized Index Protocol")

# Create a Graphviz diagram
dot = gv.Digraph()

# Set graph and node attributes to control size
dot.attr(size="12,12")  # This limits the width and height of the output


# Define nodes
dot.node('Investor', 'Investor', shape='box', style='rounded')
dot.node('ETH', 'Send ETH', shape='box', style='filled', fillcolor='lightblue')
dot.node('SetContract', 'Index Contract', shape='box', style='rounded')
dot.node('DEX', 'DEX', shape='box', style='rounded')
dot.node('Issue', 'Issue Index Token', shape='box', style='filled', fillcolor='lightblue')
dot.node('Collateral', 'ETH ⇄ Collateral Swaps', shape='box', style='filled', fillcolor='lightblue')

# Define edges (arrows)
dot.edge('Investor', 'ETH', label='1')
dot.edge('ETH', 'SetContract')
dot.edge('SetContract', 'DEX', label='2')
dot.edge('SetContract', 'Issue', label='3')
dot.edge('Investor', 'Issue', dir='back')
dot.edge('DEX', 'Collateral')
dot.edge('Collateral', 'SetContract')

# Render diagram in Streamlit
st.graphviz_chart(dot)

st.caption("Investor interaction with Index Protocol for issuing Index Tokens")
