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
    front_end_json = request.get_json()
    # front_end_json = front_end_json['params'] #to be passed as JSON to next microservice * KEYS: ticker | price | quantity | order_type | portfolio_id,
    return front_end_json

    #3 check if portfolio is valid
    url = "http://127.0.0.1:5000/get_portfolio/" + str(front_end_json["portfolio_id"])

    portfolio_validation = invoke_http(url, method='GET')

    if(portfolio_validation["code"] != 404): #portfolio valid!

        #4. invoke positions microservice to check if current portfolio already has position 
        url = "http://127.0.0.1:5000/get_positions/" + front_end_json['portfolio_id'] + "/" + front_end_json["ticker"]

        position_validation = invoke_http(url, method='GET', **kwargs)

        if(position_validation["code"] == 404):
            #No initial positions: add quantity of new positions to positions table

            url = "http://127.0.0.1:5000/add_position/" + str(front_end_json["portfolio_id"])
            
            add_position_validation = invoke_http(url, method='POST', json=front_end_json, **kwargs)

            if(add_position_validation["code"] == 200):
                return "Order Filled!"

            else:
                return "Something went wrong, please try again!"
            
        else:
            #portfolio already has some positions of requested ticker: update number of positions already in portfolio

            #creating new json for updating quantity
            position_json = position_validation["data"]

            new_total_bought_at = position_validation["total_bought_at"] + (front_end_json["price"] * front_end_json["quantity"])
            new_total_quantity = position_validation["total_quantity"] + front_end_json["quantity"]
            new_last_bought_price = front_end_json["price"]
            new_last_updated_price = front_end_json["price"]
            new_last_transaction_status = "buy"
            new_last_transaction_quantity = front_end_json["quantity"]

            update_position_json = {portfolio_id: position_json["portfolio_id"], ticker: position_json["ticker"], total_bought_at: new_total_bought_at, total_quantity: new_total_quantity, last_bought_price: new_last_bought_price, last_sold_price: position_json["last_sold_price"], last_updated_price: new_last_updated_price, last_transaction_status: new_last_transaction_status, last_transaction_quantity: new_last_transaction_quantity, last_updated: position_json["last_updated"]}

            #call update positions function to update position record in positions table

            url = "http://127.0.0.1:5000/update_position/" + str(front_end_json["portfolio_id"])

            position_update_validation = invoke_http(url, method='PUT', json = update_position_json, **kwargs)

            #update portfolio timing

            url = "http://127.0.0.1:5000/update_portfolio/" + str(front_end_json["portfolio_id"])

            portfolio_update_validation = invoke_http(url, method='PUT', **kwargs)



            return position_update_validation

    else:
        return "Invalid Portfolio ID!"

    # adding record to orders table **Insert once above is tested successfully
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


@app.route("/place_order/sell", methods=['POST'])
def sell():
    
    #2. extracting data from json request
    front_end_json = request.get_json()
    front_end_json = front_end_json['params'] #to be passed as JSON to next microservice * KEYS: ticker | price | quantity | order_type | portfolio_id,
    return front_end_json

    #3 check if portfolio is valid
    url = "http://127.0.0.1:5000/get_portfolio/" + front_end_json["portfolio_id"]

    portfolio_validation = invoke_http(url, method='GET', **kwargs)

    if(portfolio_validation["code"] != 404): #portfolio valid!

        #4. invoke positions microservice to check if current portfolio has position of ticker inputted
        url = "http://127.0.0.1:5000/get_positions/" + front_end_json['portfolio_id'] + "/" + front_end_json["ticker"]

        position_validation = invoke_http(url, method='GET', **kwargs)

        if(position_validation["code"] == 404):
            #No initial positions: no positions to sell

            return "No positions to sell!"
            
        else:
            #portfolio already has some positions of requested ticker to sell: check if current positions > quantity intended to sell

            #creating new json for updating quantity
            position_json = position_validation["data"]

            if(position_json["total_quantity"] < front_end_json["quantity"]):
                
                return "Not enough positions to sell!"
            
            else:
                new_total_sold_at = position_validation["total_sold_at"] + (front_end_json["price"] * front_end_json["quantity"])
                new_total_quantity = position_validation["total_quantity"] - front_end_json["quantity"]
                new_last_sold_price = front_end_json["price"]
                new_last_updated_price = front_end_json["price"]
                new_last_transaction_status = "sell"
                new_last_transaction_quantity = front_end_json["quantity"]

                update_position_json = {portfolio_id: position_json["portfolio_id"], ticker: position_json["ticker"], total_sold_at: new_total_sold_at, total_quantity: new_total_quantity, last_bought_price: position_json["last_bought_price"], last_sold_price: new_last_sold_price, last_updated_price: new_last_updated_price, last_transaction_status: new_last_transaction_status, last_transaction_quantity: new_last_transaction_quantity, last_updated: position_json["last_updated"]}

                #call update positions function to update position record in positions table

                url = "http://127.0.0.1:5000/update_position/" + front_end_json["portfolio_id"]

                position_update_validation = invoke_http(url, method='PUT', json = update_position_json, **kwargs)

                #update portfolio timing

                url = "http://127.0.0.1:5000/update_portfolio/" + front_end_json["portfolio_id"]

                portfolio_update_validation = invoke_http(url, method='PUT', **kwargs)

                return position_update_validation

    else:
        return "Invalid Portfolio ID!"


if __name__ == '__main__':
    app.run(port=5001, debug=True)