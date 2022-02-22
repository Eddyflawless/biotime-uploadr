import sys
import os
from mysql.connector import Error
from pprint import pprint
import json
import requests
import base64
import datetime
from dotenv import load_dotenv
from pathlib import Path
from app import db, read, write, api, logger
DBConnector = db.DBConnector
Read = read.Read
Write = write.Write
Api = api.Api

xlogger = logger.Logger.getInstance().getLogger()

db_connection = None

def getEnv():
    user=os.getenv("user")
    password=os.getenv("password")
    database=os.getenv("database")
    host=os.getenv("host")
    port=os.getenv("port")
    return user,password,database,host,port
    
def getServerCredentials():

    # application_id = os.getenv('application_id')
    endpoint = os.getenv('application_endpoint', '').strip()
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')

    return endpoint,client_id,client_secret

def getRead():
    return Read(db_connection)

def getWrite():
    return Write(db_connection)

def get_db_con():

    try:

        user,password,database,host,port = getEnv()

        conn = DBConnector(host,user,password,database,port)

        db_connection = conn.getConnector()

        if db_connection is None:
            raise Error("Connector cannot be undefined")

        db_Info = db_connection.get_server_info()   

        print("Connected to MySQL Server ", db_Info)

        return conn    

    except Error as e:
        xlogger.error(e)
        raise e


def postToServer(endpoint,data,client_id="",client_secret=""):

    try:

        auth_string = client_id + ":" + client_secret
        auth_64_bytes = base64.b64encode(auth_string.encode("utf-8"))
        auth_64_bytes = str(auth_64_bytes)

        headers = {"Content-Type": "application/json; charset=utf-8",   "Authorization": "Basic " + auth_64_bytes }
        api_post = Api()
        response = api_post.post(endpoint,data=data, headers=headers)
        return response

    except requests.exceptions.RequestException as e:
        xlogger.error(e)
        return None
    except Exception as e:
        xlogger.error(e)
        return None

def submitAttendance(json_data):

    endpoint, client_id, client_secret = getServerCredentials()
    
    response = postToServer(endpoint=endpoint,data=json_data,
    client_id=client_id,client_secret=client_secret)

    if response is None:
        return False

    if response.status_code != 200:
        return False

    return True    


def updateAttendanceTaskParam(att_date,count):
    print("passed: update cron_task :", batch_skip)    

    batch_skip = read.batch_skip
    batch_skip = count + batch_skip;
    write.updateAttendanceTaskParam(att_date, batch_skip);


def getAttendanceDate():
    x = datetime.datetime.now()      
    return  x.strftime("%Y-%m-%d")
    

def getAttendances(rows):
    attendances = []
    count = 0

    for recordset in rows:

        punch_time = recordset['punch_time'].strftime('%Y-%m-%d %H:%M:%S')
        attendances.append(
            { 
                'punch_time': punch_time,
                'punch_state' : recordset['punch_state'],
                'emp_code' : recordset['emp_code'],
                'source' :  recordset['source'],
                'machine_id' : recordset['terminal_sn'],
                'temperature': recordset['temperature']
            }
        )
        count = count + 1

    return attendances, count    

def main_init():

    global db_connection

    try:

        conn = get_db_con()

        if conn is None:
            raise TypeError("connection cannot be null")

        db_connection = conn.getConnector()

        read = getRead()
        write = getWrite()

        att_date = getAttendanceDate()

        task_param_exist = read.getAttendanceTaskParam(att_date)

        if task_param_exist is None:
            write.createAttendanceTaskParam(att_date)

        rows = read.getIClockTransactions(att_date)

        post_data={ 'application_id': os.getenv('application_id') }

        print("att_date", att_date);

        attendances, count = getAttendances(rows)

        post_data['attendances'] = attendances
        
        json_data = json.dumps(post_data)

        if count != 0:

            if submitAttendance(json_data):
                updateAttendanceTaskParam(att_date,count)

        print("200 closed---")
       
    except Error as err:
        print("500 closed---")
        xlogger.error(err)
    finally:
        db_connection.close()

      

if __name__ == '__main__':

    load_dotenv(dotenv_path = Path('.env'))
    main_init()
 
