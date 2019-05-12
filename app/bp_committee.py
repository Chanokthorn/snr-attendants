from app import app, login, login_required, db
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response, Blueprint
import json
from flask_cors import CORS, cross_origin
from app.models import Committee, Personnel, Committee_personnel
from flask_login import current_user
import datetime
from app.utils import eprint, map_row_data_to_object
import uuid

from sqlalchemy.exc import IntegrityError

bp = Blueprint('committee', __name__, url_prefix='/committee')


# @app.route('/committee', methods=['GET'])
# @login_required(role="secretary")
# def get_all_committee():
#     try:
# #         committees = Committee.query.all()
#         committees = db.session.query(Committee_personnel, Committee, Personnel)\
#             .filter(Committee_personnel.c_id == Committee.c_id)\
#             .filter(Committee_personnel.p_id == Personnel.p_id).all()
#         result = []
#         for committee in committees:
#             committee_info = map_row_data_to_object(committee[1])
#             personnel_info = map_row_data_to_object(committee[2])
#             committee_info.update(personnel_info)
#             result.append(committee_info)
        
#         response =  jsonify(result)
#     except(RuntimeError, TypeError, NameError):
#         db.session.rollback()
#         eprint(RuntimeError, TypeError, NameError)
#         response = "error"
# #         response = Response("error")
#     return response

@app.route('/committee', methods=['GET'])
@login_required(role="secretary")
def get_all_committee():
    try:
#         committees = Committee.query.all()
        committees = db.session.query(Committee).all()
        result = []
        for committee in committees:
            committee_info = map_row_data_to_object(committee)
            result.append(committee_info)        
        response =  jsonify(result)
    except(RuntimeError, TypeError, NameError):
        db.session.rollback()
        eprint(RuntimeError, TypeError, NameError)
        response = "error"
#         response = Response("error")
    return response