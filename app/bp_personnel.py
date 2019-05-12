from app import app, login, login_required, db
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

@app.route('/personnel', methods=['GET'])
@login_required(role="admin")
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