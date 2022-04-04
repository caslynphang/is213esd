from flask import Flask, redirect, request, render_template
from flask_cors import CORS
from flask_login import current_user, login_user, login_required, logout_user
from user import login #loginmanager from user model
import logging
import os, sys
import requests
from invokes import invoke_http


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

login.init_app(app)
login.login_view = 'login' #sets login_view to the login path/view below


@app.route('/home')
@login_required #redirects to loginpage if you 
def home():
    return render_template('stock_view.html')


@app.route("/login", methods = ['POST', 'GET']) #retrieve user object, do comparison, render page
def login():
    if current_user.is_authenticated: #if authenticated, redirect to user home page 
        return redirect('/home') 
    if request.method == 'POST': #if a new login req is made with post
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = invoke_http(f"http://localhost:5000/for_login/{email}") #get user object based off email since email is unique
        if user is not None and user.check_password(password): #if user is found and password is verified. check_password method from user obj, will compared pw
            login_user(user) #login user with login_user 
            return redirect('/home') #redirect to home view

    return render_template('login.html') #if not already authenticated or if post req not made, essentially just getting the login page, so return login view


@app.route("/signup", methods = ['POST', 'GET']) 
def signup():
    if current_user.is_authenticated: #logout and go to signout page? maybe they wanna make new account, need to look into this
        return redirect('/home')

    if request.method == 'POST': #posting new user to register
        data = request.get_json()
        signup_results = invoke_http("http://localhost:5000/add_user", method = 'POST', json = data)
        code = signup_results['code']

        if code == 201: #successful register
            return redirect('/home')
    
    return render_template('signup.html') #if not already authenticated or if post req not made, essentially just getting the login page, so return signup view

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

app.secret_key = "fd08462624b345138cfd113014ce76bb" #change out in prod

if __name__ == '__main__':
    app.run(port=5001, debug=True)