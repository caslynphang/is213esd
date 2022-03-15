import requests
from datetime import date, timedelta
# yesterday / today->(api may not update that quickly :|)
yesterday = str(date.today() - timedelta(days=1))
# today = str(date.today())


def recommend_by_closeprice(user_chosen_ticker):

# get yesterday's/today's close prices for all stocks (USE YOUR OWN KEYS LOL[i only hv 5 req/min] -- polygon.io)
    r = requests.get('https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/'+ yesterday +'?adjusted=true&apiKey=JVUOJpz7eTK1LXR6J0bZxnQVnyifIbvt')
    results = r.json()['results']

# find close price of stock chosen by user
    for result in results:
        if result['T'] == user_chosen_ticker:
            user_ticker_close_price = result['c']

            print('Ticker: '+ str(result['T'])+'; Close price: '+ str(user_ticker_close_price))

# find a suitable stock price range 
    upper_limit = user_ticker_close_price * 1.1
    lower_limit = user_ticker_close_price *0.9
# using the stock price range based on users' ticker, we can find other tickers within the range
    for result in results:
        if result['c'] <upper_limit and result['c'] > lower_limit and result['T'] != user_chosen_ticker:
            ticker_close_price = result['c']
            print('Ticker: '+ str(result['T'])+'; Close price: '+ str(ticker_close_price))

# User select this ticker
recommend_by_closeprice("TSLA")