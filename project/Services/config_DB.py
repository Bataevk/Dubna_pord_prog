from sqlalchemy import create_engine
from Models.user_models import User
from Models.user_models import Base
from sqlalchemy.orm import Session

def init_config():
    global engine
    engine = create_engine("sqlite:///config.db")
    Base.metadata.create_all(bind=engine)
def get_user(login):
    with Session(autoflush=False, bind=engine) as db:
        return db.query(User).filter(User.name == login).first()
def add_user(user:User):
   with Session(autoflush=False, bind=engine) as db:
       if get_user(user.name) is None:
        db.add(user)
        db.commit()     
def remove_user(user:User):
   with Session(autoflush = False, bind=engine) as db:
       if get_user(user.name) is not None:
        db.add(user)
        db.commit() 

