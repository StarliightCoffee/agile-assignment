import flask
from flask import Flask

app = Flask(__name__)

@app.route("/")
def route():
    return "<p>hello world</p>"

@app.route("/")
def User_Registration():
    email = input("Please Enter Your Email Address \n")
    password = input("Please Create a Password \n")

    user_details = [email, password]

    