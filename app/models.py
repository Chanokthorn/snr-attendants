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

class Meeting(db.Model):
    m_id = db.Column(db.String(45), primary_key=True)
    m_num_of_attendants = db.Column(db.Integer, index=False, unique=False)
    m_starttime = db.Column(db.DateTime, index=False, unique=False)
    m_endtime = db.Column(db.DateTime, index=False, unique=False)
    m_committee = db.Column(db.String(45), index=False, unique=False)
    m_secretary = db.Column(db.Integer, index=False, unique=False)