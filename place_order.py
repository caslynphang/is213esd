from flask import Flask, request, jsonify
from invokes import invoke_http
import json

app = Flask(__name__)

# 1. route "buy" function for frontend Axios call with ticker symbol and amount passed through parameter "ticker_and_amount"
# 1.1 format for ticker_and_amount parameter to be passed from frontend - "ticker&amount" - Example - "TSLA&800"
@app.route("/place_order/buy/<string:ticker_and_amount>", methods=['POST'])
def buy(ticker_and_amount):
    
    #2. extracting individual ticker and amount bought
    ticker = ticker_and_amount.split("&")[0]
    amount = int(ticker_and_amount.split("&")[1])

    buy_information = {"ticker": ticker, "amount": amount}

    buy_information_json = json.dumps(buy_information)

    #3. invoke portfolio microservice using invoke_http function imported from invokes.py -- see line 2
    #3.1 pass in buy_information_json as json argument


if __name__ == '__main__':
    app.run(port=5000, debug=True)