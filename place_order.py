from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. route "buy" function for frontend Axios call with ticker symbol and amount passed through parameter "ticker_amount_quantity"
# 1.1 format for ticker_amount_quantity parameter to be passed from frontend - "ticker&amount" - Example - "TSLA&800&8"
@app.route("/place_order/buy/<string:ticker_amount_quantity>", methods=['POST'])
def buy(ticker_amount_quantity):
    
    #2. extracting individual ticker and amount bought
    ticker = ticker_amount_quantity.split("&")[0]
    amount = float(ticker_amount_quantity.split("&")[1])
    quantity = int(ticker_amount_quantity.split("&")[2])
    

    buy_information = {"ticker": ticker, "amount": amount, "quantity:" : quantity, "order_type" : "buy"}

    buy_information_json = json.dumps(buy_information)

    return buy_information

    #3. invoke portfolio microservice using invoke_http function imported from invokes.py -- see line 2
    #3.1 pass in buy_information_json as json argument


if __name__ == '__main__':
    app.run(port=5001, debug=True)