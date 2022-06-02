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
st.image("Images/eth_weights.png")
st.title("FlexCoin for the BlockGym")
st.markdown("## FlexCoin incentivizes you to come to the gym at a time when it is not too busy, so that you can access the equipment you need now to flex your muscles later.")

# Access account and balance 
st.write("Choose your account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options = accounts)
wallet_balance_wei = w3.eth.getBalance(address)
wallet_balance_flex_token = int(wallet_balance_wei/1000000000000000000)
# Wallet_FLEX_balance = contract.functions.balanceOf(address).transact()
# st.write(f"Your wallet contains {Wallet_FLEX_balance} FLEX tokens.")

private_key = st.text_input("Your Private Key")

# Items list
items = ["Towel", "Smoothie", "Water Bottle", "Gym Bag", "Gym Shirt", "Gym Shorts", "Full Body Massage", "Additional Token"]

# Gym Store
item_database = {
    "Towel": ["Towel", 1, "Images/towel.jpeg"],
    "Smoothie": ["Smoothie", 7, "Images/smoothie.jpeg"],
    "Water Bottle": ["Water Bottle", 3, "Images/water_bottle.jpeg"],
    "Gym Bag": ["Gym Bag", 15, "Images/gym_bag.jpeg"],
    "Gym Shirt": ["Gym Shirt", 10, "Images/gym_shirt.jpeg"],
    "Gym Shorts": ["Gym Shorts", 12, "Images/gym_shorts.jpeg"],
    "Full Body Massage": ["Full Body Massage", 20, "Images/massage.jpeg"],
    "Additional Token": ["Additional Token", 1, "Images/token.png"] 
    }

# Title for sidebar
st.sidebar.title('Gym Store')

# Create a select box to choose an item to buy 
select_item = st.sidebar.selectbox('Select an Item', items)

# Show image of item
st.sidebar.image(item_database[select_item][2])

df = pd.read_csv("gym_items.csv", index_col = "item", parse_dates=True, infer_datetime_format = True)

df.sort_index(inplace=True, ascending = False)

# Slider for quantity of item 
quantity = st.sidebar.slider("Select Quantity of Item:", 1, 100, 2)

# Identify the price 
price = df.loc[:, "token_cost"]

# Write the item price to the sidebar
st.sidebar.write(price)

# Calculate total price for the item by multiplying the item price by the quantity 
total = item_database[select_item][1] * quantity

# Show total cost of item(s)
st.sidebar.write('The Item(s) You Selected Cost:')
st.sidebar.write(total)

# Purchase items button
if st.button("PURCHASE ITEM(S)"):
    tx_hash = contract.functions.transfer(address, total).transact({
        "from": address,
        "gas": 1000000
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

# Membership description
st.markdown('## Membership Costs')
st.markdown('### Each month, members must purchase at least 50 tokens. Additional tokens can be purchased from the gym store on the sidebar.') 

# Purchase button 

if st.button("PURCHASE 50 MEMBERSHIP TOKENS"):
    tx_hash = contract.functions.transfer(address, 50).transact({
        "from": address,
        "gas": 1000000
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))