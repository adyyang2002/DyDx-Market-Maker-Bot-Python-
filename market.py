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

from dydx3.constants import TIME_IN_FORCE_GTT

from web3 import Web3
import dydx3.constants as consts
import json
import random
import os
import logging
import sys
import csv

# buy/sell on dydx programatically
# install dydx client on the aws instance
# track how much time i spend on it - 
# understand public/private key cryptography
# what is rsa algorithm wiki
 
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
 
test_private_key = ""
with open(os.path.join(__location__, "private_key.txt")) as f:
    test_private_key = f.readlines()[0].rstrip()

text_file = "trade_file.csv"

API_HOST_MAINNET = 'https://api.dydx.exchange/'
API_HOST_GOERLI = 'https://api.stage.dydx.exchange/'
NETWORK_ID_GOERLI = 5
ETHEREUM_ADDRESS = '0xA72390121F5c362753bE288CD63e9034A1277042'
WEB_PROVIDER_URL = 'https://goerli.infura.io/v3/49d9273a4f5c446697ee32b9af8bc7cc'

TOLERANCE = 100000
#calculate 1% from the index price for limit
LIMIT = 1000000
TARGET_TRADE_SIZE = 1
timer = 60

def get_client(host, network_id):
 
    source_client = Client(
        eth_private_key=test_private_key,
        host=host,
        web3_provider=WEB_PROVIDER_URL # Can use url of any Ethereum node
    )
 
    stark_private_key = source_client.onboarding.derive_stark_key(
    # Optional if eth_private_key or web3.eth.defaultAccount was provided.
        ethereum_address=ETHEREUM_ADDRESS,
    )
 
    # Create client for the new user.
    client = Client(
        host=host,
        network_id=network_id,
        stark_private_key=stark_private_key,
        eth_private_key=test_private_key,
        web3_provider=WEB_PROVIDER_URL,
    )
    # Onboard the user for new accounts on dydx.
    # res = client.onboarding.create_user()
    # api_key_credentials = res['apiKey']
 
    return client

client = get_client(API_HOST_GOERLI, NETWORK_ID_GOERLI)
# response = client.public.get_markets()
# print(response.data)

# print('Waiting for funds...')
# transfer = client.private.request_testnet_tokens()
# print('...done.', transfer.data)

#putting a buy and sell order, and order every 5 mins, 
#put a buy and sell order 1% below and 1% above
#remove an existing order if they arent fulfilled

def get_total_csv_position_size(filename):
  """
  File for mock trading function.
  """
  with open(os.path.join(__location__, filename)) as fin:
    total = 0
    for row in csv.reader(fin):
      # row 1 is size
      total += float(row[1])
    return total

def get_low(btc_price):
  #calculate 1% lower for price of bitcoin
  return float(btc_price * 1.01)

def get_high(btc_price):
  #calculate 1% higher for price of bitcoin
  return float(btc_price * .99)

def trade():
  #buy and sell
  
  buy_order = client.private.create_order(
    #what is position id?
    position_id = 1,
    market = MARKET_BTC_USD,
    side = ORDER_SIDE_BUY,
    order_type = ORDER_TYPE_LIMIT,
    post_only = False,
    size='1',
    price = get_low(MARKET_BTC_USD),
    limit_fee='0.015',
    expiration_epoch_seconds=60,
    time_in_force = TIME_IN_FORCE_GTT,
  )

  sell_order = client.private.create_order(
    position_id = 1,
    market = MARKET_BTC_USD,
    side = ORDER_SIDE_SELL,
    order_type=ORDER_TYPE_LIMIT,
    post_only=False,
    size='1',
    price=get_high(MARKET_BTC_USD),
    limit_fee='0.015',
    expiration_epoch_seconds=60,
    time_in_force=TIME_IN_FORCE_GTT,
  )

def main():
  counter = 0
  print("Time: " + str(time.time()))
  while(counter < 1440):
    #calls the buy and sell function
    time.sleep(60)
    client.private.cancel_all_orders(market=MARKET_BTC_USD)
    counter += 1
    print(counter)
  print("End: " + str(time.time()))
  print("Done")

main()