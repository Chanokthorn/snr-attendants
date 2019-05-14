from app import app, login, login_required, BASE_URI
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response
import json
from flask_cors import CORS, cross_origin
from flask_login import current_user, login_user, logout_user
from app.models import Login
from functools import wraps
from . import bp_auth, bp_meeting, bp_recog, bp_committee, bp_personnel

app.register_blueprint(bp_auth.bp)
app.register_blueprint(bp_meeting.bp)
# app.register_blueprint(bp_recog.bp)
app.register_blueprint(bp_committee.bp)
app.register_blueprint(bp_personnel.bp)

@app.route(BASE_URI + '/profiles/<path:fileName>')
def send_js(fileName):
    print("path: ", fileName)
    return send_from_directory('profiles', fileName, as_attachment=True)

@app.route(BASE_URI+'/test_login', methods=['GET', 'POST'])
# @login_required(role="secretary")
def test_login():
    uid = current_user.get_id()
    if uid is not None:
        print("UID: ",uid)
        user = Login.query.filter_by(uid=uid).first()
        result = {"username": user.username, "role": user.role}
        return json.dumps(result)
    else:
        return "unauthorized"

    