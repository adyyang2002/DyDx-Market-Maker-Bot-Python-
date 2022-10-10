import time
import math
from dydx3 import Client
from dydx3.constants import API_HOST_ROPSTEN
from dydx3.constants import API_HOST_MAINNET
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import NETWORK_ID_ROPSTEN
from dydx3.constants import NETWORK_ID_MAINNET
from dydx3.constants import POSITION_STATUS_OPEN
from dydx3.constants import ORDER_SIDE_BUY
from dydx3.constants import ORDER_SIDE_SELL
from dydx3.constants import ORDER_STATUS_OPEN
from dydx3.constants import ORDER_TYPE_LIMIT
from web3 import Web3
import dydx3.constants as consts
import json
import random
import os
import logging
import sys
import csv
# get prices from dydx
# make a dydx account
# buy/sell on dydx programatically
# install dydx client on the aws instance
# track how much time i spend on it - 
# learn git?
# understand public/private key cryptography
# what is rsa algorithm wiki
 
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
 
test_private_key = ""
with open(os.path.join(__location__, "private_key.txt")) as f:
    test_private_key = f.readlines()[0].rstrip()
 
ETHEREUM_ADDRESS = '0x66aCb0bB35894bc68c7802F7DEa5ed3bdfe3a233'
WEB_PROVIDER_URL = 'https://mainnet.infura.io/v3/49d9273a4f5c446697ee32b9af8bc7cc'

def get_client(host, network_id):
 
    source_client = Client(
        eth_private_key=test_private_key,
        host=host,
        web3_provider=WEB_PROVIDER_URL # Can use url of any Ethereum node
    )
 
    key_pair_with_y_coordinate = source_client.onboarding.derive_stark_key(
    # Optional if eth_private_key or web3.eth.defaultAccount was provided.
        ethereum_address=ETHEREUM_ADDRESS,
    )
 
    stark_private_key = key_pair_with_y_coordinate['private_key']   
    # Create client for the new user.
    client = Client(
        host=host,
        network_id=network_id,
        stark_private_key=stark_private_key,
        eth_private_key=test_private_key,
        web3_provider=WEB_PROVIDER_URL,
    )
    # Onboard the user for new accounts on dydx.
    #res = client.onboarding.create_user()
    #api_key_credentials = res['apiKey']
 
    return client

client = get_client(API_HOST_MAINNET, NETWORK_ID_MAINNET)
response = client.public.get_markets()
print(response)