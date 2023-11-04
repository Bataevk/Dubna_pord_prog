<<<<<<< HEAD
from config_DB import *
from project.Models.user_models import User
import bcrypt

    # id = Column(Integer, primary_key=True)
    # name = Column(String(100), nullable=False)
    # password = Column(String(100), nullable=False)
    # email = Column(String(100), nullable=True)
    # phonenumber = Column(String(100), nullable=True)
    # telegrm_id = Column(Integer, nullable=True)
    # user_roles = relationship("Role", secondary = user_roles, backref="roles")

def get_session(id: int, deltatime: int):
    return False # Заглушка

def add_session(id):
    pass # Заглушка


def get_hash(password: str):
    # Генерируем соль (salt)
    salt = bcrypt.gensalt()
    
    # Хешируем пароль с солью
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password


def check_user(user: User, password):
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return True
    else:
        return False
    
def check_session(name, password):
    user = get_user(name)
    if check_user(user, password):
        add_session()
        return True
    return False

def check_session(id):
    if (get_session(id, delta_time = 12)):
        return True
=======
from config_DB import *
from project.Models.user_models import User
import bcrypt

    # id = Column(Integer, primary_key=True)
    # name = Column(String(100), nullable=False)
    # password = Column(String(100), nullable=False)
    # email = Column(String(100), nullable=True)
    # phonenumber = Column(String(100), nullable=True)
    # telegrm_id = Column(Integer, nullable=True)
    # user_roles = relationship("Role", secondary = user_roles, backref="roles")

def get_session(id: int, deltatime: int):
    return False # Заглушка

def add_session(id):
    pass # Заглушка 


def get_hash(password: str):
    # Генерируем соль (salt)
    salt = bcrypt.gensalt()
    
    # Хешируем пароль с солью
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password


def check_user(user: User, password):
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return True
    else:
        return False
    
def check_session(name, password):
    user = get_user(name)
    if check_user(user, password):
        add_session()
        return True
    return False

def check_session(id):
    if (get_session(id, delta_time = 12)):
        return True
>>>>>>> 8f47ec9cd1400c9fdf88049bd95bc78dadb00145
    return False