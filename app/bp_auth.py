import functools
from app import app, login, BASE_URI
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response, Blueprint, make_response
from flask_login import current_user, login_user, logout_user
from app.models import Login
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

@app.route(BASE_URI + '/index')
def index():
    return "Hello, World!"

@app.route(BASE_URI + '/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        "already authenticated"
#     uid = request.args.get('uid')
#     password = request.args.get('password')
    username = request.form['username']
    password = request.form['password']
    mode = request.form['mode']
    print("received: {} {}".format(username, password))
    login = Login.query.filter_by(username=username).first()
    if login is None or not login.check_password(password):
        return 'Invalid username or password'
    if (int(mode) == 0 and login.role != "secretary") or (int(mode) == 1 and login.role != "admin"):
        return 'Invalid username or password'
    login_user(login)
    return "successful"

@app.route(BASE_URI + '/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))