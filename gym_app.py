# Imports
import os
import json
from pathlib import Path
from sqlite3 import Time
import streamlit as st
from web3 import Web3 
from dotenv import load_dotenv
from checkin import check_price
import pandas as pd
from datetime import datetime
load_dotenv('SAMPLE.env')

# Define and connect to a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URI')))

# Set as main streamlit page
st.markdown('# BlockGym')
st.sidebar.markdown('')

# Loads the contract once using cache
# Connects to the contract using the contract address and ABI
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./FlexCoin_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv('SMART_CONTRACT_ADDRESS')

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
    return contract

# Load the contract
contract = load_contract()

# Streamlit image and title 
st.image('Images/eth_weights.jpg', use_column_width = True)
st.title('FlexCoin for the BlockGym')
st.markdown('### FlexCoin incentivizes you to come to the gym at a time when it is not too busy, so that you can access the equipment you need now to flex your muscles later.')

# Access account and token balance 
st.write('Choose your account to get started')
accounts = w3.eth.accounts
address = st.selectbox('Select Account', options = accounts)
gym_address = os.getenv('OWNER_ADD')

tokens = contract.functions.balanceOf(address).call()

st.markdown(f'#### This address owns {tokens/1000000000000000000} tokens.')

# Items list
items = ['Towel', 'Smoothie', 'Water Bottle', 'Gym Bag', 'Gym Shirt', 'Gym Shorts', 'Full Body Massage']

# Gym Store database
item_database = {
    'Towel': ['Towel', 2, 'Images/towel.jpg'],
    'Smoothie': ['Smoothie', 7, 'Images/smoothie.jpeg'],
    'Water Bottle': ['Water Bottle', 3, 'Images/water_bottle.jpg'],
    'Gym Bag': ['Gym Bag', 15, 'Images/gym_bag.jpg'],
    'Gym Shirt': ['Gym Shirt', 10, 'Images/gym_shirt.jpg'],
    'Gym Shorts': ['Gym Shorts', 12, 'Images/gym_shorts.jpg'],
    'Full Body Massage': ['Full Body Massage', 20, 'Images/massage.jpeg'],
    'Additional Token': ['Additional Token', 1, 'Images/token.jpg'] 
    }

# Title for sidebar
st.sidebar.title('BlockGym Store')

# Create a select box to choose an item to buy 
select_item = st.sidebar.selectbox('Select an Item', items)

# Show image of item
st.sidebar.image(item_database[select_item][2])

# Read in csv file with gym items
df = pd.read_csv('gym_items.csv', index_col = 'item', parse_dates=True, infer_datetime_format = True)

df.sort_index(inplace=True, ascending = False)

# Slider for quantity of item 
quantity = st.sidebar.slider('Select Quantity of Item:', 1, 50, 2)

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

# Transfer function definition 
def transfer(toAddress, fromAddress, amount):
    amount = amount * 1000000000000000000
    tx_hash = contract.functions.transfer(toAddress, amount).transact({
        'from': fromAddress,
        'chainId': 1337,
        'nonce': w3.eth.get_transaction_count(fromAddress)
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write('Transaction receipt mined:')
    st.write(dict(receipt))

# Purchase items button
if st.sidebar.button('PURCHASE ITEM(S)'):
    transfer(gym_address, address, total)

# Membership description
st.markdown('## Membership Costs')
st.markdown('### Each month, members must purchase at least 50 tokens.') 
st.image('Images/member_token.jpg')

# Purchase membership tokens button 
if st.button('PURCHASE 50 MEMBERSHIP TOKENS'):
    transfer(address, os.getenv('OWNER_ADD'), 50)

# Purchase additional tokens 
st.markdown('### Running out of tokens this month? Purchase additional tokens here!')
st.image(item_database['Additional Token'][2])
additional_quantity = st.slider('Select quantity of tokens:', 1, 100, 20)

# Purchase additional tokens button
if st.button('PURCHASE ADDITIONAL TOKENS'):
    transfer(address, gym_address, additional_quantity)

# Create check-in list
checkinhistory = []

if 'history' not in st.session_state:
    st.session_state['history'] = checkinhistory

if 'history' in st.session_state:
    checkinhistory = st.session_state['history']

# Check current price of entering gym based on number of people checked in
st.markdown('## Check Into the Gym Here!')
st.image('Images/check_in.png')

# Create button to check the current price
if st.button('Get Current Price'):
    price = check_price(checkinhistory)
    st.markdown(f'### There are currently {price - 2} people in the Gym. The price is {price} tokens.')

# Create check-in button to have memebers check-in to the gym
if st.button('CHECK IN'):
    price = check_price(checkinhistory)
    checkinhistory.append(datetime.now())
    transfer(gym_address, address, price)
    st.write(checkinhistory)
    st.markdown(f'### You checked in for {price} tokens.')

