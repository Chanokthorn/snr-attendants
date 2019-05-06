import mysql.connector
from utils import eprint

db = mysql.connector.connect(
  host="snr-attendance.cs1xewchsmfa.ap-northeast-1.rds.amazonaws.com",
  user="root",
  passwd="gearnggearng",
  database="snr_attendance"
)

mycursor = db.cursor()

class Login:
    
    def __init__(self):
        pass
    
    def add_user(self, uid, password):
        sql = "INSERT INTO login (uid, password) VALUES (%s, %s)"
        val = (uid, password)
        try:
            mycursor.execute(sql, val)
            db.commit()
            return "added user {} to database".format(uid)
        except(RuntimeError, TypeError, NameError):
            printe(RuntimeError)

class Personnel:
    
    def __init__(self):
        pass
    
    def add_personnel(self, p_id, p_title, p_firstname, 
                      p_lastname, p_phone=None, p_email=None, p_note=None):
        sql = "INSERT INTO personnel (p_id, p_title, p_firstname,\
        p_lastname, p_phone, p_email, p_note) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (p_id, p_title, p_firstname, p_lastname, p_phone, p_email, p_note)
        try:
            mycursor.execute(sql, val)
            db.commit()
            return "added user {} to database".format(p_id)
        except(RuntimeError, TypeError, NameError):
            printe(RuntimeError)
            

class Committee:
    
    def __init__(self):
        pass
    
    def add_committee(self, c_id, c_title, c_effective_date, c_end_date):
        sql = "INSERT INTO committee (c_id, c_title, c_effective_date,\
        c_end_date) VALUES (%s, %s, %s, %s)"
        print(sql)
        val = (c_id, c_title, c_effective_date, c_end_date)
        try:
            mycursor.execute(sql, val)
            db.commit()
            return "added committee {} to database".format(c_id)
        except(RuntimeError, TypeError, NameError):
            printe(RuntimeError)
        
class Committee_personnel:
    
    def __init__(self):
        pass
    
    def add_committee_personnel(self, c_id, p_id):
        sql = "INSERT INTO committee_personnel VALUES (%(c_id)s, %(p_id)s)"
        val = { 'c_id': c_id, 'p_id': p_id }
        try:
            mycursor.execute(sql, val)
            db.commit()
            return "added pair {}, {} to database".format(c_id, p_id)
        except(RuntimeError, TypeError, NameError):
            printe(RuntimeError)
            
class Meeting:
    
    def __init__(self):
        pass
    
    def add_meeting(self, m_id, m_datetime, m_num_of_attendants, m_starttime,
                    m_endtime, m_committee, m_secretary):
        sql = "INSERT INTO meeting VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (m_id, m_datetime, m_num_of_attendants, m_starttime,
                    m_endtime, m_committee, m_secretary)
        try:
            mycursor.execute(sql, val)
            db.commit()
            return "added meeting {} to database".format(m_id)
        except(RuntimeError, TypeError, NameError):
            printe(RuntimeError)