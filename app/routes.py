from app import app, login, login_required
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response
import json
from flask_cors import CORS, cross_origin
from flask_login import current_user, login_user, logout_user
from app.models import Login
from functools import wraps
from . import bp_auth, bp_meeting, bp_recog, bp_committee

app.register_blueprint(bp_auth.bp)
app.register_blueprint(bp_meeting.bp)
app.register_blueprint(bp_recog.bp)
app.register_blueprint(bp_committee.bp)

@app.route('/profiles/<path:fileName>')
def send_js(path):
    print("path: ", path)
    return send_from_directory('profiles', fileName, as_attachment=True)

@app.route('/test_login', methods=['GET', 'POST'])
# @login_required(role="secretary")
def test_login():
    uid = current_user.get_id()
    if uid is not None:
        print("UID: ",uid)
        role = Login.query.filter_by(uid=uid).first().role
        result = {"uid": uid, "role": role}
        return json.dumps(result)
    else:
        return "unauthorized"

    