import psycopg2 
from datetime import datetime, timedelta
import json



class Analizyr():
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.connect = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password) #Устанавливаем соединение с нужным сервером
        self.cursor = self.connect.cursor() #Курсор - для запросов

    #Деструктор;
    def __del__(self):
        self.cursor.close() #Закрываем курсор
        self.connect.commit() #Фиксируем изменения
        self.connect.close() #Закрываем соединени с сервером

    def get_data_name_into(self):
        '''Частичная выборка из pg_stat_activity для проверки state'''
        self.cursor.execute(f"""SELECT datid, datname, pid, usename, wait_event_type, wait_event, state FROM pg_stat_activity 
                            WHERE usename = '{self.user}' AND datname is not null;""")
        rez = []
        response = self.cursor.fetchone()
        while response != None:
            rez.append(response)
            response = self.cursor.fetchone()
        return rez

    def get_database_info(self):
        '''Частичная выборка из pg_stat_database для проверки время выполнения запросов, сессий, время выполнения транзакций'''
        self.cursor.execute("""SELECT datid, datname, deadlocks, active_time, idle_in_transaction_time, sessions FROM pg_stat_database 
                                WHERE datname is not null; 
                            """)
        rez = []
        response = self.cursor.fetchone()
        while response != None:
            rez.append(response)
            response = self.cursor.fetchone()
        return rez

    def all_stat_activity(self, pid): #по pid выбирает строку
        '''Полная статистика таблицы pg_stat_activity для данного соединения с бд, по заданному pid'''
        self.cursor.execute(f"SELECT * FROM pg_stat_activity WHERE pid = {pid};")
        return self.cursor.fetchone()

    def prnt_all_stat_activity(self, pid):
        columns = ['datid', 'datname', 'pid', 'leader_pid', 'usesysid', 'usename', 'application_name', 'client_addr', 'client_hostname', 
                   'client_port', 'backend_start', 'xact_start', 'query_start', 'state_change', 
                   'wait_event_type', 'wait_event', 'state', 'backend_xid', 'backend_xmin', 'query_id', 'query', 'backend_type']
        response = self.all_stat_activity(pid)
        rez = ""
        for i in range(len(response)):
            rez += columns[i] + " " + str(response[i]) + "\n"
        return rez

    def all_stat_database(self, oid): #По oid выбирает строку
        '''Полная статистика таблицы pg_stat_database для данного соединения с бд'''
        self.cursor.execute(f"SELECT * FROM pg_stat_database WHERE datid = {oid};")
        return self.cursor.fetchone()

    def prnt_all_stat_database(self, oid):
        columns = [
          'datid', 'datname', 'numbackends', 'xact_commit','xact_rollback','blks_read','blks_hit','tup_returned','tup_fetched','tup_inserted','tup_updated','tup_deleted',
          'conflicts','temp_files',
          'temp_bytes', 'deadlocks', 'checksum_failures', 'checksum_last_failure','blk_read_time','blk_write_time','session_time','active_time','idle_in_transaction_time','sessions ',
          'sessions_abandoned','sessions_fatal','sessions_killed','stats_reset'
        ]
        response = self.all_stat_database(oid)
        rez = ""
        for i in range(len(response)):
            rez += columns[i] + " " + str(response[i]) + "\n"
        return rez


    def stat_activity(self, pid):
        '''Выборка из таблицы pg_stat_activity'''
        self.cursor.execute(f"""SELECT datid, datname, pid, usename, application_name, client_port, backend_start, xact_start, query_start, state_change, 
                                wait_event_type, wait_event, state, query, backend_type  
                                FROM pg_stat_activity WHERE pid = {pid};
                            """)
        return self.cursor.fetchone()

    def stat_database(self, oid):
        '''Выборка из таблицы pg_stat_database'''
        self.cursor.execute(f"""SELECT datid, datname, numbackends, xact_commit, xact_rollback, conflicts, deadlocks, session_time, active_time, 
                                idle_in_transaction_time, sessions, stats_reset FROM pg_stat_database 
                                WHERE datid = {oid};
                            """)
        return self.cursor.fetchone() 

    def delete_procces(self,pid): #Отключение процесса по pid
        self.cursor.execute(f"SELECT pg_terminate_backend({pid});")
        self.connect.commit()
        return self.cursor.fetchone()

    def delete_session(self, pid):
        self.cursor.execute(f"SELECT pg_cancel_backend({pid});")
        self.connect.commit()
        return self.cursor.fetchone()

    def get_all_session(self):
        '''Получаем продолжительность всех сессий'''
        self.cursor.execute(f"SELECT datid, datname, pid, backend_start FROM pg_stat_activity WHERE datname is not null;")
        res = []
        response = self.cursor.fetchone()
        while response != None:
            res.append(response)
            response = self.cursor.fetchone()
        return res #Двумерный массив
    
    def get_long_session(self):
        '''Время начала сессии'''
        res = []
        response = self.get_all_session()
        for item in response:
            time = item[3].strftime('%Y-%m-%d %H:%M:%S')
            temp = [item[0], item[1], item[2], time]
            res.append(temp)
        return res

    def get_cnt_session(self):
        '''Получения количества активных сессий'''
        self.cursor.execute("SELECT datid, datname, numbackends FROM pg_stat_database WHERE datname is not null;")
        res = []
        response = self.cursor.fetchone()
        while response != None:
            res.append(response)
            response = self.cursor.fetchone()
        return res #Двумерный массив

    def get_stat_session(self):
        '''Получение состояния сессий'''
        self.cursor.execute("SELECT datid, datname, pid, wait_event_type FROM pg_stat_activity WHERE datname is not null;")
        res = []
        response = self.cursor.fetchone()
        while response != None:
            res.append(response)
            response = self.cursor.fetchone()
        return res #Двумерный массив

    def get_wait_types(self):
        '''Получение ссылок на справку с wait_event'''
        with open('/Services/wait_types.json', encoding="utf-8") as json_file:
            data = json.load(json_file)
            #if(type in data):
            #    return data[type]
            return data
