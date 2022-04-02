from flask import Flask, jsonify
from datetime import date, timedelta, datetime
import requests
import json

app = Flask(__name__)
CORS(app)

date_ticker = {}
rangelist = []

# recommmend by closeprice
@app.route("/stock_recommender/recommend_by_closeprice/<string:portfolio_id>")
def recommend_by_closeprice(portfolio):
    # talk to portfolio.py
    url = ""
    portfolio = invoke_http(url, method='GET', json=None, **kwargs)

    # retrieve last updated position for portfolio
    for objs in portfolio:
        
        # if not datetime format
        # datetime_object = datetime.strptime(objs['last_updated'],'%Y-%m-%d')
        # date_list.append(datetime_object)
    
        ticker = objs['ticker']
        date_ticker[ticker] = objs['last_updated']
    stockName = max(date_ticker, key=date_ticker.get)

    # talk to stockinfo.py
    url = "http://127.0.0.1:5000/stockinfo/get_all_stock_info/<string:stockName>"
    results = invoke_http(url, method='GET', json=None, **kwargs)
    
    # find close price of stock chosen by user
    for result in results:
        if result['T'] == stockName:
            user_ticker_close_price = result['c']
# find a suitable stock price range 
    upper_limit = user_ticker_close_price * 1.1
    lower_limit = user_ticker_close_price *0.9

# using the stock price range based on users' ticker, we can find other tickers within the range
    for result in results:
        if result['c'] <upper_limit and result['c'] > lower_limit and result['T'] != stockName:
            rangelist.append({"Ticker" : str(result['T']), "Close Price" : str(result['c'])})
        return jsonify(
                {
            "code": 200,
            "data": rangelist
        }
    )

# recommmend by tradevolume
@app.route("/stock_recommender/recommend_by_tradevolume")
def recommend_by_tradevolume():
    final_result = {}
    # talk to stockinfo.py
    url = "http://127.0.0.1:5000/stockinfo/get_all_stock_info/<string:stockName>"
    results = invoke_http(url, method='GET', json=None, **kwargs)
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
    return jsonify(
        {
        "code": 200,
        "data": final_result
        }
    )

if __name__ == '__main__':
    app.run(port=5000, debug=True)


# just to test

# recommend_by_closeprice([{"ticker":"NIO",
# "total_bought_at":500,
# "no_of_positions":5,
# "last_updated": "2022-03-15",
# "last_bought_at":20
# },
# {"ticker":"TSLA",
# "total_bought_at":20,
# "no_of_positions":51,
# "last_updated": "2022-03-13",
# "last_bought_at":673.12
# },
# {"ticker":"AAPL",
# "total_bought_at":12,
# "no_of_positions":6,
# "last_updated": "2022-03-22",
# "last_bought_at":200
# }])


