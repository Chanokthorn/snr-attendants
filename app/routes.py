from app import app, login, login_required
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response
from flask_cors import CORS, cross_origin
from flask_login import current_user, login_user, logout_user
from app.models import Login
from functools import wraps
from . import auth, methods

app.register_blueprint(auth.bp)
app.register_blueprint(methods.bp)

@app.route('/test_login', methods=['GET', 'POST'])
@login_required(role="secretary")
def test_login():
    return Response("success")

    