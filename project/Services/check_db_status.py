import psycopg2 

HOST_DB = 'localhost'
PORT_DB = '5432'
DB_NAME = 'testdb' #Имя БД
USER = 'postgres' #Пользователь который работает с БД (в СУБД)
DB_PASS = '123451515' #Пароль от пользователя






import psycopg2.extras
from datetime import datetime, timezone

def get_all_statuses():
    connect1 = psycopg2.connect(host=HOST_DB, port=PORT_DB, user= USER, password= DB_PASS)
    dict_cur = connect1.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute(f"SELECT * FROM pg_stat_activity")
    tmp = dict_cur.fetchall()
    result = []
    for row in tmp:
        result.append(dict(row))
    return result


def get_status(db_name):
    for db in get_all_statuses():
        if db_name in db['application_name']:
            return db

def how_long_since(datetime_obj):
    t = datetime.now(timezone.utc).replace(microsecond=0)
    datetime_obj = datetime_obj.replace(microsecond=0)
    result = t - datetime_obj
    return result

def is_fine(db_name):
    tmp = get_status(db_name)
    if tmp['state'] != 'idle':
        return tmp['state']
    else:
        return True

def check(db_name):
    tmp = get_status(db_name)
    response = dict()
    response.update({'name':db_name})
    response.update({'uptime':how_long_since(tmp['backend_start'])})
    response.update({'last_query':how_long_since(tmp['query_start'])})
    response.update({'state':tmp['state']})
    return response

def get_last_query(db_name):
    return get_status(db_name)['query']

print(get_last_query('test'))




