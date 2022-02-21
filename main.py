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

def get_db_con():

    try:

        user=os.getenv("user")
        password=os.getenv("password")
        database=os.getenv("database")
        host=os.getenv("host")
        port=os.getenv("port")
        conn = DBConnector(host,user,password,database,port)

        db_connection = conn.getConnector()

        if db_connection is None:
            raise Error("Connector cannot be undefined")

        db_Info = db_connection.get_server_info()   

        # print("Connected to MySQL Server ", db_Info)

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

def main_init():

    db_connection = None

    try:


        application_id = os.getenv('application_id')
        endpoint = os.getenv('application_endpoint', '')
        endpoint = endpoint.strip()
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')

        conn = get_db_con()

        db_connection = conn.getConnector()
        cursor = db_connection.cursor() 

        read = Read(db_connection)
        write =  Write(db_connection)
        x = datetime.datetime.now()
        
        att_date = x.strftime("%Y-%m-%d")

        task_param_exist = read.getAttendanceTaskParam(att_date)

        if task_param_exist is None:
            write.createAttendanceTaskParam(att_date)

        batch_skip = read.batch_skip

        rows = read.getIClockTransactions(att_date)

        post_data={ 'application_id': application_id }
        attendances=[]

        count=0

        print("att_date", att_date);

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

        post_data['attendances'] = attendances
        
        json_data = json.dumps(post_data)

        if count != 0:

            response = postToServer(endpoint=endpoint,data=json_data,
            client_id=client_id,client_secret=client_secret)

            if response is None:
                return

            if response.status_code != 200:
                return

        
            batch_skip = count + batch_skip;
            print("passed: update cron_task :", batch_skip)    
            write.updateAttendanceTaskParam(att_date, batch_skip);

        print("200 closed---")
       

    except Error as err:
        print("500 closed---")
        xlogger.error(err)
    finally:
        db_connection.close()

      

if __name__ == '__main__':

    dotenv_path = Path('.env')
    load_dotenv(dotenv_path = dotenv_path)

    main_init()
 
