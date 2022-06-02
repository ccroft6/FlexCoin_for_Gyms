# Imports
import os
import json
from pathlib import Path
import streamlit as st
from web3 import Web3
from dotenv import load_dotenv
import crypto_wallet.py
 
load_dotenv()

# Loads the contract once using cache
# Connects to the contract using the contract address and ABI
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/FlexCoin_abi.json')) as f:
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

# Define and connect to a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


# Streamlit image and title 
st.image("Images/eth_weights.png")
st.title("FlexCoin for the BlockGym")
st.markdown("## FlexCoin incentivizes you to come to the gym at a time when it is not too busy, so that you can access the equipment you need now to flex your muscles later.")

# Access account and balance 
st.write("Choose your account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options = accounts)
wallet_balance_wei = w3.eth.getBalance(address)
wallet_balance_flex_token = int(wallet_balance_wei/100000000000000000)
st.write(f"Your wallet contains {wallet_balance_flex_token} FLEX tokens.")

private_key = st.text_input("Your Private Key")

# Gym Store
item_database = {
    "Towel": ["Towel", 1, "Images/towel.jpeg"],
    "Smoothie": ["Smoothie", 7, "Images/smoothie.jpeg"],
    "Water Bottle": ["Water Bottle", 3, "Images/water_bottle.jpeg"],
    "Gym Bag": ["Gym Bag", 15, "Images/gym_bag.jpeg"],
    "Gym Shirt": ["Gym Shirt", 10, "Images/gym_shirt.jpeg"],
    "Gym Shorts": ["Gym Shorts", 12, "Images/gym_shorts.jpeg"],
    "Full Body Massage": ["Full Body Massage", 20, "Images/massage.jpeg"]
}

items = ["Towel", "Smoothie", "Water Bottle", "Gym Bag", "Gym Shirt", "Gym Shorts", "Full Body Massage"]

def get_items(w3):
    db_list = list(item_database.values())

    for number in range(len(items)):
        st.image(db_list[number][3], width=200)
        st.write("Gym Items", db_list[number][0])
        st.write("Price Per Item", db_list[number][1], "eth")

# Create a select box to choose an item to buy 
select_item = st.sidebar.selectbox('Select an Item', items)

df = pd.read_csv("gym_items.csv", index_col = "item", parse_dates=True, infer_datetime_format = True)

df.sort_index(inplace=True, ascending = False)

start = st.selectbox("Select a Gym item:", df.index)

st.table(df)

st.button("PURCHASE")



