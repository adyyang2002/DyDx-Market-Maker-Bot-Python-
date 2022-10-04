from dydx3 import Client
from web3 import Web3
from dydx3.constants import MARKET_BTC_USD

orderbook = client.public.get_orderbook(
  market=MARKET_BTC_USD,
)



markets = client.public.get_markets()

client = Client(
    host='https://api.dydx.exchange',
    web3=Web3('...'),
    stark_private_key='01234abcd...',
)
