from app import app, login, login_required, db
from flask import Flask, render_template, request, redirect, url_for, Response, send_from_directory, Response, Blueprint
import json
from flask_cors import CORS, cross_origin
from app.models import Meeting, Personnel, Committee, Login, Attendance
from flask_login import current_user
import time
from app.utils import eprint, base64_to_image_file, map_row_data_to_object

import random

#####
# from app.FaceRecognition.FindFaceInImage import process_this_frame,add_new_person
#####

bp = Blueprint('recog', __name__, url_prefix='/recog')

@app.route('/recog/personnel/<string:p_id>', methods=['PUT'])
@login_required(role="secretary")
def add_personnel(p_id):
    print(request.form)
    image64 = request.form['image']
    image = base64_to_image_file(image64)
    print("SHAPE: ", image.shape)
    return "success"

@app.route('/recog/personnel', methods=['POST'])
@login_required(role="secretary")
def detect_personnel():
    image64 = request.form['image']
    image = base64_to_image_file(image64)
    #####
#     return json.dumps(process_this_frame(image))
    #####
    
    ##############MOCK##############
    p_id = None
    r = random.randint(0,100)
    result = "NOT_FOUND"
    if r < 50:
        p_id = None
    else:
        if r<60:
            p_id = '123'
        elif r<70:
            p_id = '143'
        elif r<80:
            p_id = '151'
        elif r<90:
            p_id = 'john'
    ##############MOCK##############
    if p_id is not None:
        personnel = Personnel.query.filter_by(p_id=p_id).first()
        result = map_row_data_to_object(personnel)
    
    return json.dumps(result)
    
