from app import app, login
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response
from flask_cors import CORS, cross_origin
from flask_login import current_user, login_user, logout_user
from app.models import Login
from functools import wraps
from . import auth

app.register_blueprint(auth.bp)


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            print('current user: ', current_user)
            if not current_user.is_authenticated:
                return "unauthorized" 
            print('current role: ', current_user.get_role())
            urole = current_user.get_role()
            if ( (urole != role) and (role != "ANY")):
                return "insufficient role permission"     
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route('/test_login', methods=['GET', 'POST'])
@login_required(role="secretary")
def test_login():
    return Response("success")

    