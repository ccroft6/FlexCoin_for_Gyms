# Imports
import streamlit as st
from web3 import Web3
import os
from dotenv import load_dotenv
 
load_dotenv()

# Define and connect to a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Streamlit 
st.title("FlexCoin for the BlockGym")
st.markdown("## FlexCoin incentivizes you to come to the gym at a time when it is not too busy, so that you can access the equipment you need now to flex your muscles later.")

st.write("Choose your account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options = accounts)

