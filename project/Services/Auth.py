import Services.config_DB as cfd
from Models.user_models import User
import bcrypt


def get_hash(password: str):
    # Генерируем соль (salt)
    salt = bcrypt.gensalt()
    # Хешируем пароль с солью
    hashed_password = bcrypt.hashpw(bytes(password.encode('utf-8')), salt)
    
    return hashed_password


def check_user(user: User, password):
    try:
        return bcrypt.checkpw( bytes(password.encode('utf-8')), user.password)
    except:
        return False
    
def check_session(name, password, tg_id):
    user = cfd.get_user(name)
    if (not (user is None)) and check_user(user, password):
        cfd.add_auth_log(tg_id)
        return True
    return False

def break_session(tg_id):
    if cfd.get_auth_log(tg_id) is None:
        return False
    cfd.remove_auth_log(tg_id)
    return True

def check_session_by_id(tg_id): # id_user
    flag = cfd.check_auth_log(tg_id, 12)
    if not flag:
        cfd.remove_auth_log(tg_id)
    return flag # Кол-во часов
