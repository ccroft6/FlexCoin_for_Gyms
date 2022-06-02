from web3 import Web3
from dotenv import load_dotenv, find_dotenv
import json
import os

load_dotenv('SAMPLE.env')

w3=Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

owner_add=os.getenv('OWNER_ADD')
owner_sk=os.getenv('OWNER_SK')

with open('FlexCoin.abi.txt') as f: 
    abi_json=json.load(f)

flexcoin_contract=w3.eth.contract(os.getenv('CONTRACT_ADDRESS'), abi=abi_json)

def reward_token(recipient_add): 
    amount=1
    nonce=w3.eth.get_transaction_count(owner_add)
    txn={'from': owner_add, 'gas': 1000000, 'nonce': nonce}
    contract_tnx=fandomcash_contract.functions.transfer(recipient_add, amount).buildTransaction(txn)
    signed_txn=w3.eth.account.sign_transaction(contract_tnx, private_key=owner_sk)
    return w3.eth.send_raw_transaction(signed_txn.rawTransaction)