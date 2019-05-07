import functools
from app import app, login
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response, Blueprint, make_response
from flask_login import current_user, login_user, logout_user
from app.models import Login
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        "not authenticated"
    uid = request.args.get('uid')
    password = request.args.get('password')
    print("received: {} {}".format(uid, password))
    login = Login.query.filter_by(uid=uid).first()
    if login is None or not login.check_password(password):
        return 'Invalid username or password'
    login_user(login)
    return "successful"

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))