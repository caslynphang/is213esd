from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/esdproject' #dynamically retrieves db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #off as modifications require extra memory and is not necessary in this case
 
db = SQLAlchemy(app) #initialization of connection, stored in variable db


class GUID(TypeDecorator): #for generation of uuid
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class Portfolios(db.Model):
    __tablename__ = 'portfolios'


    portfolio_id = db.Column(GUID(), primary_key = True, default=uuid.uuid4()) #char(32) in mysql
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    time_created = db.Column(db.DateTime(), nullable=False)
    last_updated = db.Column(db.DateTime(), nullable = False)
    positions = db.relationship('Positions', backref = 'portfolio', cascade = 'all, delete') #for use in sqlalchemy
 
    def __init__(self, portfolio_id, user_id, time_created, last_updated): #constructor. initializes record
        self.portfolio_id = portfolio_id
        self.user_id = user_id
        self.time_created = time_created
        self.last_updated = last_updated
 
    def json(self): #returns json representation of the table in dict form
        return {"portfolio_id": self.portfolio_id, "user_id": self.user_id, "time_created": self.time_created, "last_updated":self.last_updated} 



@app.route("/get_all_portfolios") #get all portfolios
def get_all():
    portfolios = Portfolios.query.all() #SQLAlchemy magic
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


@app.route("/get_portfolio/<string:portfolio_id>")
def find_by_portfolio_id(portfolio_id):
    portfolio = Portfolios.query.filter_by(portfolio_id=portfolio_id).first() #returns a list of 1 item, .first() gets the first item. similar to limit 1 in sql
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
            "message": f"Portfolio {portfolio_id} not found"
        }
    ), 404

@app.route("/<string:user_id>/add_portfolio", methods=['POST'])
def create_portfolio(user_id): #create portfolio

    try:
        #query user
        #user don't exist: throw error
        #return 404 error coz user dont exist
        #use invokes and endpoint for user
        #else:
        portfolio = Portfolios(user_id = user_id, time_created = datetime.now(), last_updated = datetime.now()) #portfolio_id auto generated

        db.session.add(portfolio)
        #add portfolio to user
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": portfolio.json()
            }
        ), 201

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "user_id": user_id
                },
                "message": "An error occurred creating the porfolio for this user."
            }
        ), 500



@app.route("/update_portfolio/<string:portfolio_id>", methods = ['PUT'])
def update_portfolio(portfolio_id):
    try:
        if (Portfolios.query.filter_by(portfolio_id = portfolio_id).first()): #book found
                data = request.get_json() #gets json data from the body of the request
                to_update = Portfolios.query.filter_by(portfolio_id = portfolio_id).first().get()
                to_update.last_updated = datetime.now()

                #the other fields of portfolio should not have any changes since they are mostly keys, and time_created of a portfolio should never change

                return jsonify( #portfolio successfully updated
                    {
                        "code": 201,
                        "data": to_update.json()
                    }
                ), 201 
        else:
            return jsonify( #portfolio not found
                {
                    "code": 404,
                    "message": f"Portfolio {portfolio_id} not found"
                }
            ), 404
    except:
        return jsonify( #error in updating
            {
                "code": 500,
                "data": {
                    "portfolio_id" : portfolio_id
                },
            "message": f"An error occured updating the time for portfolio {portfolio_id}"
            }
        ), 500




@app.route("/delete_portfolio/<string:portfolio_id>", methods=['DELETE'])
def delete_portfolio(portfolio_id):
    try:
        portfolio = Portfolios.query.filter_by(portfolio_id=portfolio_id).first()
        if portfolio:
            db.session.delete(portfolio)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "portfolio_id": portfolio_id
                    },
                    "message": f"Portfolio {portfolio_id} deleted"
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "portfolio_id": portfolio_id
                    },
                    "message": f"Portfolio {portfolio_id} not found"
                }
            ), 404
    except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "portfolio_id": portfolio_id
                    },
                    "message": f"An error occured when trying to delete portfolio {portfolio_id}"
                }
            )


if __name__ == "__main__":
    app.run(port = 5000, debug = True) #adding host = 0.0.0.0 ensures that the service can be accessible in the network debug = true restarts the flask app if the source code is being changed as the flask app is running

#can specify which ip address and port that the flask app should start with, can communicate with other computers in this manner