from app import app, login, login_required, db, BASE_URI
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response, Blueprint
import json
from flask_cors import CORS, cross_origin
from app.models import Meeting, Personnel, Committee, Login, Attendance
from flask_login import current_user
import datetime
from app.utils import eprint, map_row_data_to_object
import uuid

from sqlalchemy.exc import IntegrityError

bp = Blueprint('personnel', __name__, url_prefix='/personnel')

@app.route(BASE_URI + '/personnel', methods=['GET'])
@login_required()
def get_personnels():
    try:
        personnels = db.session.query(Personnel).all()
        result = []
        for personnel in personnels:
            result.append(map_row_data_to_object(personnel))
        response = jsonify(result)
        
    except(RuntimeError, TypeError, NameError):
        db.session.rollback()
        eprint(RuntimeError, TypeError, NameError)
        response = "error"
    return response

@app.route(BASE_URI + '/personnel', methods=['POST'])
@login_required(role="admin")
def create_personnel():
    try:
        print("REQUEST FORM: ", request.form)
        p_id = uuid.uuid4().hex
        p_title = request.form['p_title']
        p_firstname = request.form['p_firstname']
        p_lastname = request.form['p_lastname']
        p_phone = request.form['p_phone']
        p_email = request.form['p_email']
        p_note = request.form['p_note']
        personnel = Personnel(p_id=p_id,p_title=p_title,p_firstname=p_firstname,\
            p_lastname=p_lastname,p_phone=p_phone,p_email=p_email,p_note=p_note )
        db.session.add(personnel)
        db.session.commit()
        personnel_send_back = map_row_data_to_object(personnel)
        response = jsonify(personnel_send_back)
    except IntegrityError:
        db.session.rollback()
        eprint("already exists")
        response = "failure"
    return response