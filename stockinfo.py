from flask import Flask, jsonify
from datetime import date, timedelta
import datetime
import requests
import json
from flask_cors import CORS

# if saturday and sunday return fridays' prices, else return today's prices
weekno = datetime.datetime.today().weekday()
if weekno == 5:
    mostrecentday = str(date.today() - timedelta(days=1))
elif weekno == 6:
    mostrecentday = str(date.today() - timedelta(days=2))
else:
    mostrecentday = str(datetime.date.today()- timedelta(days=6))

app = Flask(__name__)
CORS(app)

@app.route("/stock_info/buy/<string:stockName>")
def buy(stockName):   
# get yesterday's/today's close prices for all stocks (USE YOUR OWN KEYS LOL[i only hv 5 req/min] -- polygon.io)
    r = requests.get('https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/'+mostrecentday+'?adjusted=true&apiKey=JVUOJpz7eTK1LXR6J0bZxnQVnyifIbvt')
    results = r.json()['results']

# find close price of stock chosen by user
    for result in results:
        if result['T'] == stockName:
            user_ticker_close_price = result['c']
            final_result = {"Ticker" : str(result['T']), "Close Price" : str(user_ticker_close_price)}
            final_result1 = json.dumps(final_result)
            return final_result1



@app.route("/stock_info/get_all_stock_info/")
def get_all_stock_info():
# get yesterday's/today's close prices for all stocks (USE YOUR OWN KEYS LOL[i only hv 5 req/min] -- polygon.io)
    r = requests.get('https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/'+mostrecentday+'?adjusted=true&apiKey=JVUOJpz7eTK1LXR6J0bZxnQVnyifIbvt')
    results = r.json()['results']
    return results

if __name__ == '__main__':
    app.run(port=5000, debug=True)
