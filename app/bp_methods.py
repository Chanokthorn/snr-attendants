from app import app, login, login_required, db
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response, Blueprint
from flask_cors import CORS, cross_origin
from app.models import Meeting, Personnel, Committee, Login, Attendance
from flask_login import current_user
import time
from app.utils import eprint, map_row_data_to_object
import uuid

bp = Blueprint('methods', __name__, url_prefix='/methods')

@app.route('/meeting', methods=['GET'])
@login_required(role="secretary")
def get_meetings():
    uid = current_user.get_id()
    try:
        meetings = Meeting.query.filter_by(m_secretary = uid).all()
        result = []
        for meeting in meetings:
            result.append(meeting.m_id)
            response = jsonify(result)
#         response = Response(jsonify(result))
    except(RuntimeError, TypeError, NameError):
        db.session.rollback()
        eprint(RuntimeError, TypeError, NameError)
        response = "error"
#         response = Response("error")
    return response

@app.route('/meeting/all' methods=['GET'])
@login_required(role="admin")
def get_meetings():
    uid = current_user.get_id()
    try:
        meetings = Meeting.query.all()
        result = []
        for meeting in meetings:
            result.append(map_row_data_to_object(meeting))
        return json.dumps(result)
    except(RuntimeError, TypeError, NameError):
        eprint(RuntimeError, TypeError, NameError)
        return "failure"


@app.route('/meeting/<string:m_id>', methods=['PUT'])
@login_required(role="secretary")
def create_meeting(m_id):
    print("REQUEST FORM: ", request)
    uid = current_user.get_id()
    c_id= request.form['c_id']
    try:
        m = Meeting(m_id=m_id, m_num_of_attendants=0, m_starttime=time.time(), m_committee=c_id, m_secretary=uid)
        db.session.add(m)
        db.session.commit()
    except(RuntimeError, TypeError, NameError):
        db.session.rollback()
        eprint(RuntimeError, TypeError, NameError)
        return Response
    return "success"

@app.route('/meeting/<string:m_id>', methods=['POST'])
@login_required(role="secretary")
def add_personnel_to_meeting(m_id):
    p_id= request.form['p_id']
    print("P ID: ", p_id)
    try:
        meeting = Meeting.query.filter_by(m_id=m_id).first()
        personnel = Personnel.query.filter_by(p_id=p_id).first()
        a_id = uuid.uuid4().hex
        attendance = Attendance(a_id=a_id, m_id=meeting.m_id, p_id=personnel.p_id, a_chkintime=time.time())
        db.session.add(attendance)
        meeting.m_num_of_attendants += 1
        db.session.commit()
        return "attendance added; m_id: {}; p_id: {}".format(m_id, p_id)
    except(RuntimeError, TypeError, NameError):
        db.session.rollback()
        eprint(RuntimeError, TypeError, NameError)
        return "failure"
    
@app.route('/meeting/<string:m_id>', methods=['GET'])
@login_required(role="secretary")
def get_attendants(m_id):
    meeting = Meeting.query.filter_by(m_id=m_id).first()
    attendants = db.session.query(Attendance).filter_by(m_id=m_id).join(Personnel,Attendance.p_id == Personnel.p_id).all()
    result = []
    for attendant in attendants:
        result.append(map_row_data_to_object(attendant))
        
    
    
    