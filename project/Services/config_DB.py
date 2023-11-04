import time
from datetime import datetime
from sqlalchemy import DateTime, create_engine
from Models.user_models import Role, User, DbConnection, Auth_log
from Models.user_models import Base
from sqlalchemy.orm import Session

def init_config():
    global engine
    engine = create_engine("sqlite:///config.db")
    Base.metadata.create_all(bind=engine)
def get_user(login):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(User).filter(User.name == login).first()

def get_user_by_id(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(User).filter(User.telegrm_id == tg_id).first()
    
def add_user(user:User):
   with Session(autoflush=False, bind=engine) as db:
       if get_user(user.name) is None:
        db.add(user)
        db.commit() 
        return True
       return False   
def remove_user(user:User):
   with Session(autoflush = False, bind=engine) as db:
       if get_user(user.name) is not None:
        db.add(user)
        db.commit() 

def get_role(id):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Role).filter(Role.id == id).first()
def add_role(role:Role):
   with Session(autoflush=False, bind=engine) as db:
       if get_user(role.id) is None:
        db.add(role)
        db.commit()     
def remove_role(role: Role):
   with Session(autoflush = False, bind=engine) as db:
       if get_user(role.id) is not None:
        db.add(role)
        db.commit() 

def get_dbconnection(id):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(DbConnection).filter(DbConnection.id == id).first()
def add_dbconnection(dbconnection : DbConnection):
   with Session(autoflush=False, bind=engine) as db:
       if get_user(dbconnection.id) is None:
        db.add(dbconnection)
        db.commit()     
def remove_dbconnection(dbconnection : DbConnection):
   with Session(autoflush = False, bind=engine) as db:
       if get_user(dbconnection.id) is not None:
        db.add(dbconnection)
        db.commit() 


def get_auth_log(id):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(Auth_log).filter(Auth_log.user_id == id).first()
    
def add_auth_log(id : int):
   with Session(autoflush=False, bind=engine) as db:
        if get_auth_log(id) is None:
            db.add(
                Auth_log(user_id = id, date_time = datetime.now())
               )
            db.commit()

def check_auth_log(id, deltatime):
    session = get_auth_log(id)
    if session is None:
       return False
    current_time = datetime.now()
    return (current_time - session.date_time).total_seconds() / 3600 <= deltatime


def remove_auth_log(id: int):
   with Session(autoflush = False, bind=engine) as db:
       auth_log = get_auth_log(id)
       if auth_log is not None:
        db.delete(auth_log)
        db.commit() 


def update_auth_log(auth_log : Auth_log, dateTime : DateTime):
   with Session(autoflush = False, bind=engine) as db:
      log = get_auth_log(auth_log.user_id)
      if log is not None:
         log.date_time = dateTime
         db.commit()