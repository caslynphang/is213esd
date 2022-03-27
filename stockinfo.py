from flask import Flask, jsonify
from datetime import date, timedelta
import requests
import json
from flask_cors import CORS

# yesterday / today->(api may not update that quickly :|)
yesterday = str(date.today() - timedelta(days=1))
# today = str(date.today())

app = Flask(__name__)
CORS(app)

@app.route("/stock_info/buy/<string:stockName>")
def buy(stockName):   
# get yesterday's/today's close prices for all stocks (USE YOUR OWN KEYS LOL[i only hv 5 req/min] -- polygon.io)
    r = requests.get('https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2022-03-25?adjusted=true&apiKey=')
    results = r.json()['results']
    
# find close price of stock chosen by user
    for result in results:
        if result['T'] == stockName:
            user_ticker_close_price = result['c']
            final_result = {"Ticker" : str(result['T']), "Close Price" : str(user_ticker_close_price)}
            final_result1 = json.dumps(final_result)
            return final_result1

        
@app.route("/stock_info/recommend_by_close_price/<string:stockName>")
def recommend_by_close_price(stockName):
# recommend by close price

# get yesterday's/today's close prices for all stocks (USE YOUR OWN KEYS LOL[i only hv 5 req/min] -- polygon.io)
    r = requests.get('https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2022-03-25?adjusted=true&apiKey=')
    results = r.json()['results']

# find close price of stock chosen by user
    for result in results:
        if result['T'] == stockName:
            user_ticker_close_price = result['c']

# find a suitable stock price range 
    upper_limit = user_ticker_close_price * 1.1
    lower_limit = user_ticker_close_price *0.9
# using the stock price range based on users' ticker, we can find other tickers within the range
    for result in results:
        if result['c'] <upper_limit and result['c'] > lower_limit and result['T'] != user_chosen_ticker:
            ticker_close_price = result['c']
            final_result = {"Ticker" : str(result['T']), "Close Price" : str(ticker_close_price)}
            return final_result

        
@app.route("/stock_info/recommend_by_tradevolume")
def recommend_by_tradevolume():
# recommmend by tradevolume
    final_result = {}
# get all the stocks trade volume (USE YOUR OWN KEYS LOL[i only hv 5 req/min]-- polygon.io)
    r = requests.get('https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2022-03-25?adjusted=true&apiKey=')
    results = r.json()['results']
    trade_volume_list = []

    # get top 20 stocks trade volume in order
    for result in results:
        trade_volume_list.append(result['v'])
    trade_volume_list.sort()
    top20_volume_list = trade_volume_list[-20:]
    
    for a in top20_volume_list:
        for result in results:
            if result['v'] == a:
                final_result[result['T']] = result['v']
    return final_result

if __name__ == '__main__':
    app.run(port=5000, debug=True)
