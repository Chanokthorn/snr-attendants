from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    print("loaded id: ", id)
    print("queried id: ", Login.query.get(id))
    return Login.query.get(id)

class Login(UserMixin,db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), index=True, unique=True)
    role = db.Column(db.String(45), index=True, unique=False)
    password_hash = db.Column(db.String(128))
    
    def get_role(self):
        return self.role
    
    def get_id(self):
        return str(self.uid).encode("utf-8").decode("utf-8") 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.uid)

class Committee(db.Model):
    c_id = db.Column(db.String(45), primary_key=True)
    c_title = db.Column(db.String(45), index=False, unique=False)
    c_effective_date = db.Column(db.DateTime, index=False, unique=False)
    c_end_date = db.Column(db.DateTime, index=False, unique=False)
    
class Personnel(db.Model):
    p_id = db.Column(db.String(45), primary_key=True)
    p_title = db.Column(db.String(45), index=False, unique=False)
    p_firstname= db.Column(db.String(45), index=False, unique=False)
    p_lastname = db.Column(db.String(45), index=False, unique=False)
    p_phone = db.Column(db.String(45), index=False, unique=False)
    p_email = db.Column(db.String(45), index=False, unique=False)
    p_note = db.Column(db.String(45), index=False, unique=False)
    
class Committee_personnel(db.Model):
    c_id = db.Column(db.String(45), primary_key=True)
    p_id = db.Column(db.String(45), primary_key=True)
    
class Meeting(db.Model):
    m_id = db.Column(db.String(45), primary_key=True)
    m_num_of_attendants = db.Column(db.Integer, index=False, unique=False)
    m_starttime = db.Column(db.DateTime, index=False, unique=False)
    m_endtime = db.Column(db.DateTime, index=False, unique=False)
    m_committee = db.Column(db.String(45), index=False, unique=False)
    m_secretary = db.Column(db.Integer, index=False, unique=False)
    m_title = db.Column(db.String(45), index=False, unique=False)
    m_start_schedule = db.Column(db.DateTime, index=False, unique=False)
    m_end_schedule = db.Column(db.DateTime, index=False, unique=False)
    m_state = db.Column(db.DateTime, index=False, unique=False)
    
class Attendance(db.Model):
#     a_id = db.Column(db.String(45), primary_key=True)
    m_id = db.Column(db.String(45), primary_key=True)
    p_id = db.Column(db.String(45), primary_key=True)
    a_chkintime = db.Column(db.DateTime, index=False, unique=False)