# Imports
import os
import json
from pathlib import Path
import streamlit as st
from web3 import Web3 
from dotenv import load_dotenv
from crypto_wallet import generate_account, get_balance, send_transaction
import pandas as pd
load_dotenv("SAMPLE.env")

# Define and connect to a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Set as main streamlit page
st.markdown("# BlockGym 🎈")
st.sidebar.markdown("# BlockGym 🎈")

# Loads the contract once using cache
# Connects to the contract using the contract address and ABI
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./FlexCoin_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()

# Streamlit image and title 
st.image("Images/eth_weights.png", use_column_width = True)
st.title("FlexCoin for the BlockGym")
st.markdown("## FlexCoin incentivizes you to come to the gym at a time when it is not too busy, so that you can access the equipment you need now to flex your muscles later.")

# Access account and balance 
st.write("Choose your account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options = accounts)

# Get the current balance of the tokens
tx_hash = contract.functions.balanceOf(address).transact({
    "from": address,
    "gas": 1000000
    })
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
st.write("Transaction receipt mined:")
st.write(dict(receipt))

tokens = contract.functions.balanceOf(address).call()

st.markdown(f"#### This address owns {tokens} tokens.")

gym_private_key = "1f3dfc8865928cc5a03fbc7cf8168789c9c60ebf1064812d22cd62def0449ede"

# Items list
items = ["Towel", "Smoothie", "Water Bottle", "Gym Bag", "Gym Shirt", "Gym Shorts", "Full Body Massage"]

# Gym Store
item_database = {
    "Towel": ["Towel", 2, "Images/towel.jpeg"],
    "Smoothie": ["Smoothie", 7, "Images/smoothie.jpeg"],
    "Water Bottle": ["Water Bottle", 3, "Images/water_bottle.jpeg"],
    "Gym Bag": ["Gym Bag", 15, "Images/gym_bag.jpeg"],
    "Gym Shirt": ["Gym Shirt", 10, "Images/gym_shirt.jpeg"],
    "Gym Shorts": ["Gym Shorts", 12, "Images/gym_shorts.jpeg"],
    "Full Body Massage": ["Full Body Massage", 20, "Images/massage.jpeg"],
    "Additional Token": ["Additional Token", 1, "Images/token.jpeg"] 
    }

# Title for sidebar
st.sidebar.title('BlockGym Store')

# Create a select box to choose an item to buy 
select_item = st.sidebar.selectbox('Select an Item', items)

# Show image of item
st.sidebar.image(item_database[select_item][2])

df = pd.read_csv("gym_items.csv", index_col = "item", parse_dates=True, infer_datetime_format = True)

df.sort_index(inplace=True, ascending = False)

# Slider for quantity of item 
quantity = st.sidebar.slider("Select Quantity of Item:", 1, 50, 2)

# Identify the price 
price = item_database[select_item][1]

# Write the item price to the sidebar
st.sidebar.write(f'The price of this item is: {price} tokens')
st.sidebar.write(price)

# Calculate total price for the item by multiplying the item price by the quantity 
total = item_database[select_item][1] * quantity

# Show total cost of item(s)
st.sidebar.write(f'The Item(s) You Selected Cost: {total} tokens')
st.sidebar.write(total)

# Gym Store Header
st.markdown('### To purchase the items selected from the BlockGym Store, press the button below.')

# Purchase items button
# !!!!!!Note: The issue is in the transfer function 
if st.button("PURCHASE ITEM(S)"):
    tx_hash = contract.functions.transfer(address, total).transact({
        "from": address,
        "amount": total
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

# Membership description
st.markdown('## Membership Costs')
st.markdown('### Each month, members must purchase at least 50 tokens.') 
st.image('Images/member_token.png')

# Purchase button 

if st.button("PURCHASE 50 MEMBERSHIP TOKENS"):
    tx_hash = contract.functions.mint(address, 50).transact({
        "from": address,
        "amount": 50
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

# Purchase additional tokens
st.markdown('### Running out of tokens this month? Purchase additional tokens here!')
st.image(item_database["Additional Token"][2])
additional_quantity = st.slider('Select quantity of tokens:', 1, 100, 20)

if st.button("PURCHASE ADDITIONAL TOKENS"):
    tx_hash = contract.functions.mint(address, additional_quantity).transact({
        "from": address,
        "amount": additional_quantity 
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
