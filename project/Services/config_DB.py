from sqlalchemy import create_engine
from project.Models.user_models import User
from project.Models.user_models import Base
from sqlalchemy.orm import Session

def init_config():
    global engine
    engine = create_engine("sqlite:///config.db")
    Base.metadata.create_all(bind=engine)
def get_user(login,password):
    with Session(autoflush=False, bind=engine) as db:
        db.query(User).filter(User.name == login and User.password == password)
def add_user(user:User):
   with Session(autoflush=False, bind=engine) as db:
       db.add(user)
       db.commit()     
