import requests
# get prices from dydx
# make a dydx account
# buy/sell on dydx programatically
# install dydx client on the aws instance
# track how much time i spend on it
# learn git?
# understand public/private key cryptography
# what is rsa algorithm wiki

# defining key/request url
key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
  
# requesting data from url
data = requests.get(key)  
data = data.json()
print(f"{data['symbol']} price is {data['price']}")