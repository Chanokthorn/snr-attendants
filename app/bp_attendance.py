from app import app, login, login_required, db
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response, Blueprint
from flask_cors import CORS, cross_origin
from app.models import Meeting, Personnel, Committee, Login, Attendance
from flask_login import current_user
import time
from app.utils import eprint
import uuid

bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@app.route('/attendance/', methods=['GET'])
@login_required(role="secretary")
def get_attendants()


# @app.route('/meeting/<string:m_id>/<string:p_id>', methods=['PUT'])
# @login_required(role="secretary")
# def add_personnel_to_meeting(m_id, p_id):
#     meeting = Meeting.query.filter_by(m_id=m_id).first()
#     personnel = Personnel.query.filter_by(p_id=p_id).first()
#     a_id = uuid.uuid4().hex
#     attendance = Attendance(a_id=a_id, m_id=m_id, p_id=p_id, a_chkintime=time.time())
#     db.session.add(attendance)
#     meeting.m_num_of_attendants += 1
#     db.session.commit()
#     return "success"