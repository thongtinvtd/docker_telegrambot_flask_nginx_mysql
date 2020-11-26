from flask import Flask,request
from flaskext.mysql import MySQL
from flask_sslify import SSLify
import requests
import time
from time import sleep


TOKEN_TL = '1184469265:AAGgnSA0T1z3_PLNWMLu9LpB1fu6dCeNjyY'


app = Flask(__name__) 
# sslify = SSLify(app)

app.config['MYSQL_DATABASE_HOST']='mysql'
app.config['MYSQL_DATABASE_PORT']= 3306
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='a123456'
app.config['MYSQL_DATABASE_DB']='data_bot'
# app.config['MYSQL_DATABASE_CHARSET']='utf-8'
app.secret_key='asdf123qwywetyrtysdf'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
curs = conn.cursor()
print("Connect successful!")

list_user_send = ['admin', 'Yes']
def get():
    return app, mysql, conn, curs

def send_message(chat_id,text=' '):
    url = f'https://api.telegram.org/bot{TOKEN_TL}/sendMessage'
    payload = {'chat_id':chat_id,'text':text}
    r = requests.post(url,json=payload)
    return r

def list_chat_id(set_user):
    try:
        str_user = ''
        for i in set_user:
            str_user += '"{}",'.format(i)
        str_user = str_user[:-1]
        
        sql3 = "SELECT user_id FROM alert_list WHERE permission IN ({});".format(str_user)
        rows = sqlselect(sql3)
        listchatid = []
        # rows = (('1029731812',), ('251290036',), ('1343733841',), ('325253745',))
        # using function for to get the element
        if rows and rows[0] != 0:
            for i in rows :
                listchatid.append(i[0])  
        print (listchatid)       
        return listchatid
    except Exception as e:
        raise(e)

def send_many_message(list_user_type = [], mess='') : 
    # app, mysql, conn, curs = get()

    listchatid = list_chat_id(list_user_type)
    listchatid_sended = []
    for chat_id in listchatid:
        send_message(chat_id, mess) #--> gui message cho ng dung
        listchatid_sended.append(chat_id)
        sleep(0.1)
    print(listchatid_sended)

def get_time_para():
    # app, mysql, conn, curs = get()
    sql0 = "SELECT * FROM para_manager WHERE parameter in ('Time_cycle', 'Time_req') ;"
    conn = mysql.connect()
    curs = conn.cursor()
    curs.execute(sql0)
    rows = curs.fetchall()
    if len(rows) > 0:
        # time between two circles
        TIME_CYCLE = rows[0][3]
        # time between two requests to web server kamera 
        TIME_REQ   = rows[1][3]
    return TIME_CYCLE,TIME_REQ

def sqlselect(sql=str):
    # app, mysql, conn, curs = get()
    try:
        conn = mysql.connect()
        curs = conn.cursor()
        curs.execute(sql)
        rows = curs.fetchall()
        print(rows)
        return rows
    except Exception as e:
        print("Error: ",sql)
# convert format time and status in the values from kamera
def convSec2HMS(secondVar):
    # if int(secondVar) is int :
    if secondVar:
        h = (int(float(secondVar) // 3600))
        m = int(float(secondVar)) - h*3600
        m = m // 60
        s = int(float(secondVar)) - h*3600 - m * 60
        timeStr = str(h) + 'h  ' + str(m) + 'm  ' + str(s) + 's '
        return timeStr
    else:
        return 'Error 1'

def getProgStatus(val_Status):
    status_str = ''
    try:
        pgst = int(val_Status[3:],16)
    except Exception as e:
        return 'Error!'
    if pgst & 1 :
        status_str = 'running'
    if pgst & 2 :
        status_str = 'paused'
    if pgst & 4 :
        status_str = 'waiting'
    if pgst & 16 :
        status_str = 'waiting to start'
    return status_str

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#----------------------get status bot -------------------
def getStatusBot():
    try:
        sql_dis = "SELECT status FROM admin_manager WHERE user_name = 'admin' ;"
        rows_status = sqlselect(sql_dis)
        if rows_status :
            if rows_status[0][0]:
                return True
            else:
                return False
    except Exception as e:
        print("Get status failed")
