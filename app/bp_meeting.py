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

bp = Blueprint('meeting', __name__, url_prefix='/meeting')

state_new = "NEW"
state_started = "STARTED"
state_ongoing = "ONGOING"
state_ended = "ENDED"

@app.route(BASE_URI + '/meeting', methods=['GET'])
@login_required(role="secretary")
def get_meetings():
    uid = current_user.get_id()
    try:
        meetings = Meeting.query.filter_by(m_secretary = uid).all()
        result = []
        for meeting in meetings:
            result.append(map_row_data_to_object(meeting))
        response = jsonify(result)
#         response = Response(jsonify(result))
    except(RuntimeError, TypeError, NameError):
        db.session.rollback()
        eprint(RuntimeError, TypeError, NameError)
        response = "error"
#         response = Response("error")
    return response

@app.route(BASE_URI + '/meeting/incoming', methods=['GET'])
@login_required(role="secretary")
def get_incoming_meetings():
    uid = current_user.get_id()
#     meetings = db.session.query(Meeting).filter(Meeting.m_secretary==uid).filter(Meeting.m_start_schedule >= datetime.datetime.now()).all()
    meetings = db.session.query(Meeting).filter(Meeting.m_secretary==uid).filter(Meeting.m_state!=state_ended).all()
    result = []
    for meeting in meetings:
        result.append(map_row_data_to_object(meeting))
    response = jsonify(result)
    return response

@app.route(BASE_URI + '/meeting/history', methods=['GET'])
@login_required(role="secretary")
def get_history_meetings():
    uid = current_user.get_id()
#     meetings = db.session.query(Meeting).filter(Meeting.m_secretary==uid).filter(Meeting.m_start_schedule < datetime.datetime.now()).all()
    meetings = db.session.query(Meeting).filter(Meeting.m_secretary==uid).filter(Meeting.m_state==state_ended).all()
    result = []
    for meeting in meetings:
        result.append(map_row_data_to_object(meeting))
    response = jsonify(result)
    return response

@app.route(BASE_URI + '/meeting/all', methods=['GET'])
@login_required(role="admin")
def get_all_meetings():
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


@app.route(BASE_URI + '/meeting/<string:m_title>', methods=['PUT'])
@login_required(role="secretary")
def create_meeting(m_title):
    print("REQUEST FORM: ", request)
    m_id = uuid.uuid4().hex
    uid = current_user.get_id()
    c_id= request.form['c_id']
    m_start_schedule = request.form['m_start_schedule']
    m_end_schedule = request.form['m_end_schedule']
    try:
        m = Meeting(m_id=m_id, m_secretary=uid, m_committee=c_id, m_num_of_attendants=0, m_title=m_title\
                    ,m_start_schedule=m_start_schedule, m_end_schedule=m_end_schedule, m_state=state_new)
        db.session.add(m)
        db.session.commit()
    except(RuntimeError, TypeError, NameError):
        db.session.rollback()
        eprint(RuntimeError, TypeError, NameError)
        return Response
    return "success"

@app.route(BASE_URI + '/meeting/<string:m_id>/init', methods=['POST'])
@login_required(role="secretary")
def update_meeting_init_state(m_id):
    m_starttime = datetime.datetime.now()
    query_m_id = Meeting.query.filter_by(m_id=m_id).first().m_id
    db.session.query(Meeting).filter(Meeting.m_id == query_m_id).update({Meeting.m_state: state_started})
    db.session.commit()
    return "success"

@app.route(BASE_URI + '/meeting/<string:m_id>/start', methods=['POST'])
@login_required(role="secretary")
def update_meeting_starttime(m_id):
    m_starttime = datetime.datetime.now()
    query_m_id = Meeting.query.filter_by(m_id=m_id).first().m_id
    db.session.query(Meeting).filter(Meeting.m_id == query_m_id).update({Meeting.m_starttime: m_starttime, Meeting.m_state: state_ongoing})
    db.session.commit()
    return "success"

@app.route(BASE_URI + '/meeting/<string:m_id>/end', methods=['POST'])
@login_required(role="secretary")
def update_meeting_endtime(m_id):
    m_endtime = datetime.datetime.now()
    query_m_id = Meeting.query.filter_by(m_id=m_id).first().m_id
    db.session.query(Meeting).filter(Meeting.m_id == query_m_id).update({Meeting.m_endtime: m_endtime, Meeting.m_state: state_ended})
    db.session.commit()
    return "success"
    
# @app.route('/meeting/<string:m_title>/endtime', methods=['POST'])
# @login_required(role="secretary")
# def create_meeting(m_title):
    

@app.route(BASE_URI + '/meeting/attend/<string:m_id>', methods=['PUT'])
@login_required(role="secretary")
def add_personnel_to_meeting(m_id):
    p_id= request.form['p_id']
    print("P ID: ", p_id)
    try:
        meeting = Meeting.query.filter_by(m_id=m_id).first()
        personnel = Personnel.query.filter_by(p_id=p_id).first()
#         a_id = uuid.uuid4().hex
        attendance = Attendance(m_id=meeting.m_id, p_id=personnel.p_id, a_chkintime=datetime.datetime.now())
        db.session.add(attendance)
        meeting.m_num_of_attendants += 1
        db.session.commit()
        return "attendance added; m_id: {}; p_id: {}".format(m_id, p_id)
    except IntegrityError:
        db.session.rollback()
        eprint("already exists")
        return "failure"
        
    
@app.route(BASE_URI + '/meeting/<string:m_id>', methods=['GET'])
@login_required(role="secretary")
def get_attendants(m_id):
    try:
        meeting = Meeting.query.filter_by(m_id=m_id).first()
#         attendants = db.session.query(Attendance).filter_by(m_id=m_id).join(Personnel,Attendance.p_id == Personnel.p_id).all()
        attendants = x = db.session.query(Attendance, Personnel)\
            .filter(Attendance.p_id == Personnel.p_id).filter_by(m_id=m_id).all()
        result = []
        for attendant in attendants:
            result.append(map_row_data_to_object(attendant[1]))
        return json.dumps(result)
    except(RuntimeError, TypeError, NameError):
        db.session.rollback()
        eprint(RuntimeError, TypeError, NameError)
        return "failure"
        
    
    
    