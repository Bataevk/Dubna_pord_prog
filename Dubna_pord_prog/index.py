import psycopg2 

HOST_DB = 'localhost'
PORT_DB = '5432'
DB_NAME = 'testdb' #Имя БД
USER = 'postgres' #Пользователь который работает с БД (в СУБД)
DB_PASS = '123451515' #Пароль от пользователя

connect1 = psycopg2.connect(host=HOST_DB, port=PORT_DB, dbname = DB_NAME , user= USER, password= DB_PASS)
curs1 = connect1.cursor()

def print_columns():
    curs1.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = 'pg_stat_activity'")
    all_col = curs1.fetchall() #Колонки
    curs1.execute(f"SELECT * FROM pg_stat_activity")
    all_row = curs1.fetchall() #Строки
    rez = []
    for row in all_row:
        temp = ""
        for i in range(len(row)):
            temp += all_col[i][0] + " = " + str(row[i]) + "\n"   
        rez.append(temp)
    return rez
