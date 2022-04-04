from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

import uuid
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/esdproject' #dynamically retrieves db url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #off as modifications require extra memory and is not necessary in this case
 
db = SQLAlchemy(app) #initialization of connection, stored in variable db
login = LoginManager() #init of flask-login manager



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
 
class Users(UserMixin, db.Model):
    __tablename__ = 'users'


    user_id = db.Column(GUID(), primary_key = True, default=uuid.uuid4()) #uuid, char(32) in mysql
    first_name = db.Column(db.String(120), nullable = False)
    last_name = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String())    
    time_created = db.Column(db.DateTime(), nullable=False)
    last_updated = db.Column(db.DateTime(), nullable = False)
    portfolios = db.relationship('Portfolio', backref = 'user', cascade = 'all, delete')
 
    def __init__(self, user_id, first_name, last_name, email, time_created, last_updated): #constructor. initializes record
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.time_created = time_created
        self.last_updated = last_updated
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
 
    def json(self): #returns json representation of the table in dict form
        return {"user_id": self.user_id, "first_name": self.first_name, "last_name": self.last_name, "email": self.email, "time_created": self.time_created, "last_updated":self.last_updated} 


@login.user_loader
def load_user(id):
    return Users.query.get(id)



@app.route("/get_all_users") #get all users
def get_all():
    users = Users.query.all() #SQLAlchemy magic
    if len(users):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in users] #returns list of users in json format
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404 #if status code is not specified, 200 OK is returned by default -- hence error 404 code is needed.


@app.route("/get_user/<string:email>")
def get_user_by_email(email):
    user = Users.query.filter_by(email=email).first() #returns a list of 1 item, .first() gets the first item. similar to limit 1 in sql
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": f"No user with {email} not found"
        }
    ), 404

@app.route("/add_user", methods=['POST'])
def add_user(): #create user
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']


    try:
        user = Users(first_name = first_name, last_name = last_name, email = email, password = password, time_created = datetime.now(), last_updated = datetime.now()) #user_id auto generated

        db.session.add(user)
        #add user to user table
        db.session.commit()
        return jsonify(
            {
                "code": 201,
                "data": user.json() #show user info added to db
            }
        ), 201

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "email": email
                },
                "message": "An error occurred while creating this user account."
            }
        ), 500


@app.route("/update_user", methods = ['PUT'])
def update_user():
    try:
        email = data['email']
        if (Users.query.filter_by(email = email).first()): #user found
                data = request.get_json() #gets json data from the body of the request
    
                to_update = Users.query.filter_by(email = email).first()
                if data['first_name']:
                    to_update.first_name = data['first_name']
                    to_update.last_updated = datetime.now()
                if data['last_name']:
                    to_update.last_name = data['last_name']
                    to_update.last_updated = datetime.now()
                if data['email']:
                    to_update.email = data['email']
                    to_update.last_updated = datetime.now()
                if data['password']:
                    to_update.password = data['password']
                    to_update.last_updated = datetime.now()

                db.session.commit()
                return jsonify( #user successfully updated
                    {
                        "code": 201,
                        "data": to_update.json()
                    }
                ), 201 
        else:
            return jsonify( #user not found
                {
                    "code": 404,
                    "message": f"User not found"
                }
            ), 404
    except:
        return jsonify( #error in updating
            {
                "code": 500,
                "data": {
                    "email" : email
                },
            "message": f"An error occured updating user information for user with email {email}"
            }
        ), 500




@app.route("/delete_user/<string:email>", methods=['DELETE'])
def delete_user(email):
    try:
        user = Users.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "email": email
                    },
                    "message": f"User {email} deleted"
                }
            )
        else:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "email": email
                    },
                    "message": f"User {email} not found"
                }
            ), 404
    except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "email": email
                    },
                    "message": f"An error occured when trying to delete user {email}"
                }
            )


if __name__ == '__main__':
    app.run(port=5002, debug=True)