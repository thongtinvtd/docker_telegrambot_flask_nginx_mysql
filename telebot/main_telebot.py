
from flask import Flask,request,redirect
from flask import request
from flask import Response

from flaskext.mysql import MySQL

import requests
import json
import re
import lxml.html as html
from flask_sslify import SSLify

from datetime import datetime
from time import sleep
import time

TIME_OFFSET = 30

import config
from config import TOKEN_TL
app, mysql, conn, curs = config.get()

curs = None
conn = None

paraTable = []
list_user_send = config.list_user_send

update_id_readed = 0
mes_start = "'I have already remebered you, if admin alows, I will send alerts to you when the machine has errors'"
mes_status_dis = "Sorry, kamera is not working now !"
mes_help = "I have 4 commands:\n\b\b\b/start : Add you to the alert list.\n   /stop : Delete you from the alert list.\n   /status : Request the status\'s climate camera.\n   /help : About bot\'s command."
mes_stop = "I have already delete you from the alert list, I will not send alerts to you when the machine has errors"
mes_not_permi = "You don't have permission to request kamera information. Please contact admin"
# def write_json(data,filename='status.json'):
#     with open(filename,'w') as f:              #dung thu tuc with open() as tenfile: json.dump() de luu file
#             json.dump(data,f,indent=4,ensure_ascii=False)
#-----------------------------------------------------------------
def check_connect():
    curs1 = curs
    conn1 = conn
    connected = False
    while not connected:
        try:
            conn1 = mysql.connect()
            curs1 = conn1.cursor()
            print("Connect successful!")
            connected = True
        except Exception as e:
            print('Connect MySQL server error, connect again')
            sleep(1)    
    return conn1,curs1
#-----------------------------------------------------------------------

def get_data():
    try:           
        #thu tuc truy cap database mysql lay parameter
        # sql0="select * from climate where id=(select max(id) from climate);"
        sql0="SELECT id,Time_request, \
                TEMPERATURE, \
                HUMIDITY, \
                TEMPERATURE_SET, \
                HUMIDITY_SET, \
                `Profile No.`, \
                `Profile Name`, \
                `Profile Cycles`, \
                `Active Cycles`, \
                `Total Loops`, \
                `Act Loops`, \
                `Segment`, \
                `Active Time`, \
                `Profile Time`, \
                `Total Time`, \
                `Segment Type`, \
                `Segment Total Time`, \
                `Segment Remain Time`, \
                `Status` FROM climate WHERE id=(SELECT MAX(id) FROM climate);"
        conn = mysql.connect()
        curs = conn.cursor()
        curs.execute(sql0)
        #tra ve du lieu
        tempo = curs.fetchone()
    except Exception as e:
        raise(e)
    # curs.close()
    return tempo
#---------------------------------------------------------------------
#luu ten nguoi dung dang ky nhan thong bao loi
def write_user(chat_id,chat_user,permission = str): 
    try:
        sql2 = "SELECT count(*) FROM alert_list WHERE USER_ID={};".format(chat_id)
        conn = mysql.connect()
        curs = conn.cursor()
        curs.execute(sql2)
        rows = curs.fetchone()
        if rows and rows[0] > 0 :
            print("User has already existed !")
        else:
            sql1 = "INSERT INTO alert_list(user_id, user_name, permission) VALUES ({0},\'{1}\',\'{2}\');".format(
                chat_id, chat_user, permission
            )
            print(sql1)
            curs.execute(sql1)
            conn.commit()
    except Exception as e:
        raise(e)

#----------------------------------------------------------------------
def remove_user(chat_id):
    try:
        sql1="DELETE FROM alert_list WHERE USER_ID={};".format(chat_id)
        print(sql1)
        curs.execute(sql1)
        conn.commit()
    except Exception as e:
        raise(e)
#--------------------------------------------------------
def get_updates():
    url = f'https://api.telegram.org/bot{TOKEN_TL}/getUpdates'
    r = requests.post(url)
    r_json = json.loads(r.text)
    if r_json['result'] :
        last_msg = r_json['result'][len(r_json['result'])-1]
        return last_msg
    return ""
#-----------------------------------------------------------------
#check dungs ten lenhj de phan hoi
def parse_message(message):  
    if message :
        chat_id = message['message']['chat']['id']
        txt     = message['message']['text']
        chat_user=message['message']['chat']['first_name']
        update_id = message['update_id'] 
        update_time = message['message']['date']
        pattern=r'/[a-zA-Z]{2,11}'       #taoj pattern de kiem tra lenh dua vao 
        ticker = re.findall(pattern,txt)    

        if ticker:                 # neu lenh dua vao co cau truc thich hop thi cho chuyen tiep lenh ko thi lenh = 'khong co gi'
            command=ticker[0][1:] #cat bo dau '/' 
        else:
            command=''
        
        return update_id, chat_id, chat_user, command, update_time
#--------------------------------------------------------------------
# check time permission
def check_time_permission(chat_id):
    try:
        sql_checktime = "SELECT user_id,expiration FROM alert_list;"
        rows = config.sqlselect(sql_checktime)
        if rows[0]:
            for i in rows:
                print(" i[1] - now :",i[1],datetime.now())
                if chat_id == i[0]:
                    if i[1] > datetime.now() :
                        print(" i[1] - now :",i[1],datetime.now())
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False
    except Exception as e:
        print("Check time permission failed")
#-------------------------------------------------------------------
chat_id_admin = config.list_chat_id(['admin'])

while 1:
    sleep(0.5)
    # check status bot
    if config.getStatusBot():
        var_status = True
    else:
        var_status = False
    print("getstatusbot : ", var_status)
    # check connect
    conn,curs = check_connect()
    last_msg = get_updates()
    if parse_message(last_msg) :
        update_id, chat_id, chat_user, command, update_time = parse_message(last_msg)  #tra ve chat_id va lenh sau khi nhan duoc chuoi json
        chat_id = str(chat_id)
        #check time : neu thoi gian nhan tin nhan va thoi gian thuc te khong bang nhau thi khong gui tin nua
        # kiem tra so giay tu 01-01-1970 tu telegram va he thong
        ticks = round(time.time())  
        if (ticks - update_time)  < TIME_OFFSET : 
            if update_id != update_id_readed :
                # neu message da doc roi thi ko lam gi ca
                update_id_readed = update_id

                print(chat_id, chat_user, command)
                list_commands=('start','stop','help','status','quit')
                
                if  command not in list_commands:
                    config.send_message(chat_id,'Wrong command')
                    # return Response('ok',status=200)

                elif command == 'start':
                    write_user(chat_id,chat_user,'No')
                    if var_status: # if bot disable send other message
                        mes_send = mes_start
                    else:
                        mes_send = mes_status_dis

                    config.send_message(chat_id,mes_send)
                    #message to admin to ask to add an user to list people, these  will receive notification
                    mess_admin = '  There is a person, who wants to receive \
notification from the climate camera.\n - User_name : {} \n - Id : {}.'\
.format(chat_user,  chat_id ) 
                    if len(chat_id_admin) > 0 :
                        config.send_many_message(chat_id_admin, mess_admin)
                    # return Response('ok',status=200)

                elif command == 'status':
                    # check user has permission or no
                    list_permission = config.list_chat_id(list_user_send)
                    # check time permission
                    if (chat_id in list_permission) and check_time_permission(chat_id):
                        # request list value will on the message
                        l_varReq = []
                        sql0 = 'SELECT parameter,on_messager FROM para_manager;'
                        rows0 = config.sqlselect(sql0)
                        if len(rows0) > 0:
                            for i in rows0:
                                if i[1] == 'Yes':
                                    l_varReq.append(i[0])

                        # using list para to request values
                        paraTable.clear()
                        sql2 = "SELECT `{}` FROM climate WHERE ID = (SELECT MAX(id) FROM climate);".format("`,`".join(l_varReq))
                        rows2 = config.sqlselect(sql2)

                        varPara = ''
                        if len(rows2) > 0:
                            for i in range(len(rows2[0])) :
                                varPara = rows2[0][i]
                                # add symbol to temperature and humidity
                                if l_varReq[i][:11] == 'Temperature':
                                    varPara = str(varPara) + ' *C'
                                if l_varReq[i][:8] == 'Humidity':
                                    varPara = str(varPara) + ' %'
                                # convert time values
                                if l_varReq[i][-4:] == 'Time':
                                    varPara = config.convSec2HMS(varPara)
                                # get status from camera
                                if l_varReq[i] == 'Status':
                                    varPara = config.getProgStatus(varPara)
                                paraTable.append(
                                    [l_varReq[i], varPara]
                                ) 
                            
                        # messager to user
                        text_mess1 = "This is parameters at the last time I checked kamera: \n\
  - Number of checked : {} times \n\
  - Time checked : {} \n".format(paraTable[0][1], paraTable[1][1])   
                        text_mess2 = ''
                        # remove the first two parameters 
                        del paraTable[0:2] 
                        for i in paraTable :
                            text_mess2 += '  - {} : {} \n'.format(i[0], i[1])

                        mes_status_bot = text_mess1 + text_mess2
                        
                        # config.send_message(chat_id, mes_status_bot )
                    else:
                        mes_status_bot = mes_not_permi
                        # config.send_message(chat_id,mes_status_bot)
                    if var_status: # if bot disable send other message
                        mes_send = mes_status_bot
                    else:
                        mes_send = mes_status_dis
                    config.send_message(chat_id,mes_send)
                # handle command stop
                elif command == 'stop':
                    remove_user(chat_id)
                    if var_status: # if bot disable send other message
                        mes_send = mes_stop
                    else:
                        mes_send = mes_status_dis
                    config.send_message( chat_id, mes_stop)
                    
                # handle command help
                elif command == 'help':
                    if var_status: # if bot disable send other message
                        mes_send = mes_help
                    else:
                        mes_send = mes_status_dis
                    config.send_message(chat_id, mes_send)
                    # return Response('ok', status=200)
                elif command == 'quit':
                    config.send_message(chat_id,"Deleting the warning ...")
                    req = requests.get("http://192.168.3.105/simpac/warning/c3k_warn.plc?tag_value=1&tag_name=HMI.MS_QuitAll")
                    if req.status_code == 200:
                        config.send_message(chat_id,'I deleted the warning ! \nNow camera do not have any error warning.')
                    sleep(0.1)
if __name__ == "__main__":
    app.run(debug=True)
#     # main()
