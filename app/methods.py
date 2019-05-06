from app import app, login, login_required, db
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory, Response, Blueprint
from flask_cors import CORS, cross_origin
from app.models import Meeting, Personnel, Committee, Login, Attendance
from flask_login import current_user
import time
from app.utils import eprint
import uuid

bp = Blueprint('methods', __name__, url_prefix='/methods')

@app.route('/meeting/<string:m_id>', methods=['PUT'])
@login_required(role="secretary")
def create_meeting(m_id):
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

@app.route('/meeting/<string:m_id>/<string:p_id>', methods=['PUT'])
@login_required(role="secretary")
def add_personnel_to_meeting(m_id, p_id):
    meeting = Meeting.query.filter_by(m_id=m_id).first()
    personnel = Personnel.query.filter_by(p_id=p_id).first()
    a_id = uuid.uuid4().hex
    attendance = Attendance(a_id=a_id, m_id=m_id, p_id=p_id, a_chkintime=time.time())
    db.session.add(attendance)
    meeting.m_num_of_attendants += 1
    db.session.commit()
    return "success"
    
    
    
    
    