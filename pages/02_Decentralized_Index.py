import streamlit as st
import graphviz as gv

st.set_page_config(page_title="Decentralized Index Protocol")

st.title("Decentralized Index Protocol")


st.write("""
A Decentralized Index Protocol is a platform that allows investors to create and manage their own index funds.
Investors can issue their own index tokens, which represent a basket of underlying assets, and trade them on decentralized exchanges.
""")

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


st.subheader("Step 1: Investor sends ETH to the Contract")

eth_price_per_example = 0.5  # Example ETH price per EXAMPLE token

st.write(f"""The investor sends ETH to the contract to buy Index tokens. The current price of Index tokens is **{eth_price_per_example} ETH** per token.""")

num_tokens_buy = st.number_input("Enter the number of Index tokens to buy", min_value=1, value=100)

# Calculate the required ETH to buy the tokens
required_eth = num_tokens_buy * eth_price_per_example

st.write(f"To buy {num_tokens_buy} Index tokens, you will need **{required_eth} ETH**.")
st.write("""
Buying Index tokens involves sending ETH to the Index contract, which will convert it into the required collateral via a DEX and issue the tokens to your wallet.
""")


st.subheader("Steps 2 and 3: Collateral Swaps on Decentralized Exchanges (DEX) and Issue Tokens")

st.write("""
The Index contract will use the ETH to perform swaps on decentralized exchanges to acquire the required collateral (example, WBTC, WETH, DPI) for the Index tokens.
""")
st.write("The collateral composition of the Index token is as follows (example):")
# Define the composition of 1 EXAMPLE token
WBTC_per_token = 0.4  # Example collateral required per token
WETH_per_token = 0.1
DPI_per_token = 0.5

st.table({
    "Collateral": ["WBTC", "WETH", "DPI"],
    "Weight (%)": [WBTC_per_token * 100, WETH_per_token * 100, DPI_per_token * 100]
})


# Calculate the required collateral
required_wbtc = num_tokens_buy * WBTC_per_token
required_weth = num_tokens_buy * WETH_per_token
required_dpi = num_tokens_buy * DPI_per_token


st.write(f"To issue {num_tokens_buy} Index tokens, the contract will need the following collateral:")
st.write(f"- **{required_wbtc} WBTC**")
st.write(f"- **{required_weth} WETH**")
st.write(f"- **{required_dpi} DPI**")

st.write("The contract will perform swaps on decentralized exchanges to acquire the required collateral.")

st.write(fr"""
         The Index contract will then issue {num_tokens_buy} Index tokens to your wallet. These tokens represent a claim on the underlying collateral and can be traded on decentralized exchanges.
         """)


st.subheader("Redeeming Index Tokens")

st.write("""
Investors can redeem their Index tokens to receive the underlying collateral. 
         The contract will burn the tokens and return the collateral to the investor's wallet.
            """)

# Calculate the collateral that will be received
received_wbtc = num_tokens_buy * WBTC_per_token
received_weth = num_tokens_buy * WETH_per_token
received_dpi = num_tokens_buy * DPI_per_token

st.write(f"To redeem {num_tokens_buy} Index tokens, you will receive the following collateral:")
st.write(f"- **{received_wbtc} WBTC**")
st.write(f"- **{received_weth} WETH**")
st.write(f"- **{received_dpi} DPI**")

