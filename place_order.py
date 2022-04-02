from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from invokes import invoke_http
import requests
import json
import datetime


app = Flask(__name__)
CORS(app)

""" app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/esdproject' #dynamically retrieves db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #off as modifications require extra memory and is not necessary in this case

db = SQLAlchemy(app) #initialization of connection, stored in variable db """

""" class Orders(db.model):
    __tablename__ = "orders"

    portfolio_id = db.Column(db.Integer, primary_key = True)
    order_type = db.column(db.String(4), nullable = False)
    ticker = db.Column(db.String(45), nullable = False)
    price = db.column(db.Float(), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    time_placed = db.Column(db.DateTime(), nullable = False)

    def __init__(self, portfolio_id, order_type, ticker, price, quantity, time_placed): #constructor. initializes record
        self.portfolio_id = portfolio_id
        self.order_type = order_type
        self.ticker = ticker
        self.price = price
        self.quantity = quantity
        self.time_placed = time_placed

    def json(self): #returns json representation of the table in dict form
        return {"portfolio_id": self.portfolio_id, "order_type": self.order_type, "ticker":self.ticker, "price": self.price, "quantity": self.quantity, "time_placed": self.time_placed}  """



# 1. route "buy" function for frontend Axios call
@app.route("/place_order/buy", methods=['POST'])
def buy():
    
    #2. extracting data from json request
    data = request.get_json()
    data = data['params'] #to be passed as JSON to next microservice * KEYS: ticker | price | quantity | order_type | portfolio_id,
    return data

    #3. invoke positions microservice to check if current portfolio has position 
    #       using invoke_http function imported from invokes.py -- see line 2
    
    #3.1 insert url to call positions microservice
    # format: http://127.0.0.1:5000/get_positions/<string:portfolio_id>/<string:ticker>
    url = "http://127.0.0.1:5000/get_positions/" + data['portfolio_id'] + "/" + data["ticker"]
    
    #3.2 invoking the position microservice to check if portfolio already has position
    result = invoke_http(url, method='POST', **kwargs)

    if(result["code"] == 404):
        #add ticker to portolio
    else:
        #update number of positions already in portfolio

    #3.3adding record to orders table
    if(result == 200 or result == 201):

        time_placed = datetime.datetime.now()
        
        order = Orders(portfolio_id, "buy", ticker, price, quantity, time_placed)

        try:
            db.session.add(order)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred recording the order."
                }
            ), 500

    else:
        return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred recording the order."
                }
        ), 500

# 4. route "sell" function for frontend Axios call with ticker symbol and amount passed through parameter "ticker_amount_quantity"
# 4.1 format for ticker_amount_quantity parameter to be passed from frontend - "ticker&price&quantity" - Example - "TSLA&800&8"
@app.route("/place_order/sell/<string:ticker_amount_quantity>", methods=['POST'])
def sell(ticker_amount_quantity):
    
    #5. extracting individual ticker and amount bought
    ticker = ticker_amount_quantity.split("&")[0]
    price = float(ticker_amount_quantity.split("&")[1])
    quantity = int(ticker_amount_quantity.split("&")[2])
    

    #5.1 Preparing buy_information in JSON format to be sent to portfolio microservice
    sell_information = {"ticker": ticker, "price": price, "quantity:" : quantity, "order_type" : "sell"}

    sell_information_json = json.dumps(sell_information)

    #5.2 Temporary return statement for testing purposes
    return sell_information

    #6. invoke portfolio microservice using invoke_http function imported from invokes.py -- see line 2
    
    #6.1 insert url to call portfolio microservice
    # format: http://127.0.0.1:5000/portfolios/<portfolio_id>/order **Ask XE how to get portfolio ID
    url = "#"
    
    #6.2 invoking the portfolio microservice with buy information passed in as json argument
    result = invoke_http(url, method='POST', json=sell_information_json, **kwargs)

    return result

if __name__ == '__main__':
    app.run(port=5001, debug=True)