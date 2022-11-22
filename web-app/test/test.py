'''
This is just a test for using IPFS api Pinata
Will switch to ether.js implementation moving forward
'''

import json
import os
import requests
from pinatapy import PinataPy
from web3 import Web3, eth

# 0x600bB4F97Ca7Fc5eB3B9672eDf0C771011dD941D -- ipfs storage smart contract addr
abi = [
    {
        "inputs": [{"internalType": "string", "name": "file", "type": "string"}],
        "name": "setFile",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "fileHashes",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
]

filename = "example.jpg"

# # Start Pinata.cloud client
# with open("secret.txt") as f:
#     keys = json.load(f)

# pinata = PinataPy(keys["key"], keys["secret"])

# # Pin file to IPFS
# result = pinata.pin_file_to_ipfs(filename)
# ipfs_id = result["IpfsHash"]


# print(f"Result: {result}")
# print(f"Currently running jobs: {pinata.pin_jobs()}")
# print(f"Total data usage: {pinata.user_pinned_data_total()}")

temp = "Qmd8QsxrXTDr6nMTGvocZt3mUtXCrDhk1ZmvpHgosbuWdt"
# Store ipfs hash in blockchain
storageContract = eth.Contract(address="0x600bB4F97Ca7Fc5eB3B9672eDf0C771011dD941D")
res = storageContract.functions.setFile(temp).call()

# # Get request for added image file
# gateway = "https://ipfs.io/ipfs/"
# # print(requests.get(url=gateway + result['IpfsHash']).text)
# print(gateway + result["IpfsHash"])
# print(pinata.pin_list())

# https://ipfs.io/ipfs/Qmd8QsxrXTDr6nMTGvocZt3mUtXCrDhk1ZmvpHgosbuWdt
