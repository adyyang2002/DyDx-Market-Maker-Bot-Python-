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
markets = client.public.get_markets()

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
 

def trade(client, asset, target_size, position_id, order_side, price, live, total_imbalance = 0, log_file_name = text_file):
  if live:
    client.private.create_order(
      position_id = position_id, # required for creating the order signature
      market = asset,
      side = order_side,
      order_type = ORDER_TYPE_LIMIT,
      post_only = False,
      size = target_size,
      price = price,
      limit_fee = '0.015',
      expiration_epoch_seconds = time.time() + 300,
    )
  else:
    # Log the trade to a csv file. 
    if order_side == ORDER_SIDE_BUY:
      size = target_size 
    else:
      target_size * -1

    fields = [asset, size, order_side, price, total_imbalance]
    print(f'logging: {fields}')
    with open(os.path.join(__location__, log_file_name), 'a') as fd:
      writer = csv.writer(fd)
      writer.writerow(fields)

def checkbook(client, asset):
  orderbook = client.public.get_orderbook(
    market=asset,
  )
  # print(orderbook.data)
  # Check the quote imbalance
  bids = orderbook.data['bids']
  asks = orderbook.data['asks']
 
  bid_total = 0 
  for bid in bids:
      bid_total += float(bid['size']) * float(bid['price'])
 
  ask_total = 0 
  for ask in asks:
    ask_total += float(ask['size']) * float(ask['price'])

  #checks the profit in bid vs ask
  #bid is how much i'm selling and ask is how much they're willing to buy?
  if abs(bid_total - ask_total) > TOLERANCE:
    #clears order
    order_side = None
    #if my bid is greater than the ask, buy it because i believe it's worth more
    if bid_total > ask_total:
      order_side = ORDER_SIDE_BUY

    if bid_total < ask_total:
      order_side = ORDER_SIDE_SELL

    if order_side:
      print("Quote imbalance trade: ", order_side, abs(bid_total - ask_total))
      return order_side, bid_total - ask_total

  #what's the point of this random?
  if random.randint(0, 1):
    print("Random trade.")
    return ORDER_SIDE_BUY, bid_total - ask_total

  return ORDER_SIDE_SELL, bid_total - ask_total


def main(asset = MARKET_BTC_USD, host = API_HOST_ROPSTEN, live = False, log_file_name = text_file):
  network_id = NETWORK_ID_MAINNET if host == API_HOST_MAINNET else NETWORK_ID_ROPSTEN
  client = get_client(host, network_id)
  # Get current prices.
  markets = client.public.get_markets(asset)          
  curr_price = markets.data['markets'][asset]['indexPrice']

  # Set target trade size
  #target_size = round((TARGET_TRADE_SIZE)/float(curr_price) * LIMIT) / LIMIT

  #set it to 1 BTC?
  target_size = 1 

  position_id = 0
  size = 0

  # check positions, if breached revert
  if live or host == API_HOST_ROPSTEN:
    all_positions = client.private.get_positions(
      market=MARKET_BTC_USD,
      status=POSITION_STATUS_OPEN,
    )
 
  # Get account info
  account_response = client.private.get_account()
  position_id = account_response.data['account']['positionId']
 
  res = all_positions.data['positions']
  if len(res) > 0:
    size = res[0]['size']
  else: 
    size = get_total_csv_position_size(log_file_name)
 
  if size != 0:
    # Only check if size is over limit
    if abs(float(curr_price) * float(size)) > LIMIT:
      if float(size) > 0:
        print("selling from size")
        # Sell
        trade(client, asset, target_size, position_id, ORDER_SIDE_SELL, float(curr_price) - 10, live, 0 ,log_file_name)
      else: 
        # BUY
        print("Buying from size")
        trade(client, asset, target_size, position_id, ORDER_SIDE_BUY, float(curr_price) + 10, live, 0, log_file_name)

      return
 
 
  order_side, total_imbalance = checkbook(client, asset)
  print("trading: ", order_side)

  if order_side == ORDER_SIDE_BUY:
    trade(client, asset, target_size, position_id, order_side, float(curr_price) + 10, live, total_imbalance, log_file_name)
  else: 
    trade(client, asset, target_size, position_id, order_side, float(curr_price) - 10, live, total_imbalance, log_file_name)
 
  return