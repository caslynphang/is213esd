#addportfolio
#getportfolio
#updatepositions -- total bought value and total current value
#getpositions

from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/esdproject' #dynamically retrieves db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #off as modifications require extra memory and is not necessary in this case
 
db = SQLAlchemy(app) #initialization of connection, stored in variable db
 
class Portfolio(db.Model):
    __tablename__ = 'portfolio'


    portfolio_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    dob = db.Column(db.String(45), nullable=False)
    time_created = db.Column(db.DateTime(), nullable=False)
    last_updated = db.Column(db.DateTime(), nullable = False)
 
    def __init__(self, portfolio_id, first_name, last_name, dob, time_created, last_updated): #constructor. initializes record
        self.portfolio_id = portfolio_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.time_created = time_created
        self.last_updated = last_updated
 
    def json(self): #returns json representation of the table in dict form
        return {"portfolio_id": self.portfolio_id, "first_name":self.first_name, "last_name": self.last_name, "dob": self.dob, "time_created": self.time_created, "last_updated":self.last_updated} 

class Positions(db.Model):
    __tablename__ = 'positions'


    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.portfolio_id'), primary_key = True)
    ticker = db.Column(db.String(45), nullable = False, primary_key = True)
    total_bought_at = db.Column(db.Float(), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    last_updated = db.Column(db.DateTime(), nullable = False)
 
 
    def __init__(self, portfolio_id, ticker, total_bought_at, quantity, last_updated): #constructor. initializes record
        self.portfolio_id = portfolio_id
        self.ticker = ticker
        self.total_bought_at = total_bought_at
        self.quantity = quantity
        self.last_updated = last_updated
 
    def json(self): #returns json representation of the table in dict form
        return {"portfolio_id": self.portfolio_id, "ticker":self.ticker, "total_bought_at": self.total_bought_at, "quantity": self.quantity, "last_updated": self.last_updated} 

@app.route("/portfolios")
def get_all():
    portfolios = Portfolio.query.all() #SQLAlchemy magic
    if len(portfolios):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "portfolios": [portfolio.json() for portfolio in portfolios] #returns list of portfolios in json format
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no portfolios."
        }
    ), 404 #if status code is not specified, 200 OK is returned by default -- hence error 404 code is needed.


@app.route("/portfolios/<string:portfolio_id>")
def find_by_portfolio_id(portfolio_id):
    portfolio = Portfolio.query.filter_by(portfolio_id=portfolio_id).first() #returns a list of 1 item, .first() gets the first item. similar to limit 1 in sql
    if portfolio:
        return jsonify(
            {
                "code": 200,
                "data": portfolio.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Portfolio not found."
        }
    ), 404

@app.route("/portfolios/add", methods=['POST'])
def create_portfolio(): #create portfolio
    '''
    if (Portfolio.query.filter_by(isbn13=isbn13).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "isbn13": isbn13
                },
                "message": "Book already exists."
            }
        ), 400

        '''

    data = request.get_json()

    portfolio = Portfolio(**data, time_created = datetime.now(), last_updated = datetime.now() )


    db.session.add(portfolio)
    db.session.commit()
    '''
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "isbn13": isbn13
                },
                "message": "An error occurred creating the book."
            }
        ), 500
        '''

    return jsonify(
        {
            "code": 201,
            "data": portfolio.json()
        }
    ), 201


@app.route("/portfolios/<string:portfolio_id>/order", methods = ['PUT']) #default method is GET unless specified 
def buy_sell_positions(portfolio_id):
    if (Portfolio.query.filter_by(portfolio_id = portfolio_id)): #portfolio found
            data = request.get_json() #gets json data from the body of the request
            ##getting values from request json body
            order_type = data['order_type']
            ticker = data['ticker']
            quantity = data['quantity']
            buy_price = data['price']

            to_update = Portfolio.query.filter_by(portfolio_id = portfolio_id) #get portfolio to update

            position_to_update = Positions.query.filter_by(portfolio_id = portfolio_id, ticker = ticker).first() #get position record to update

            if order_type == "buy": #check for order type
                if position_to_update != None: #if position exists ie user has already bought into positions for the ticker before
                    position_to_update.quantity += quantity #add on qty
                    position_to_update.total_bought_at += quantity * buy_price #add on total buy in value
                    position_to_update.last_updated = datetime.now() #set last_updated to time at which request was made for the specific position
                    to_update.last_updated = datetime.now() #set last_updated to time at which portfolio, including its positions had any form of modification
                    db.session.commit() #make changes
                    return jsonify( 
                        {
                            "code" : 201,
                            "data": position_to_update.json()
                        }
                    ), 201
                else: #if position does not exist, ie user has not bought into position before
                    add_position = Positions(portfolio_id = portfolio_id, ticker = ticker, total_bought_at = (quantity * buy_price), quantity = quantity, last_updated = datetime.now()) #create position record to be added to db
                    db.session.add(add_position)
                    db.session.commit()
                    return jsonify( #return added_position
                        {
                            "code" : 200,
                            "data": add_position.json() 
                        }
                    ), 200





if __name__ == "__main__":
    app.run(port = 5000, debug = True) #adding host = 0.0.0.0 ensures that the service can be accessible in the network debug = true restarts the flask app if the source code is being changed as the flask app is running

#can specify which ip address and port that the flask app should start with, can communicate with other computers in this manner