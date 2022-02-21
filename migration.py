import sys
import os
from mysql.connector import Error
from dotenv import load_dotenv
from pathlib import Path
from app import db
DBConnector = db.DBConnector

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

        print("Connected to MySQL Server ", db_Info)

        return conn    

    except Error as e:
        raise e


def run_migration():

    db_connection = None

    try:
        conn = get_db_con()

        db_connection = conn.getConnector()
        cursor = db_connection.cursor() 
        """
            Migration 1
        """
        cursor.execute("""

                CREATE TABLE IF NOT EXISTS  `cron_tasks` ( 
                    `id` int(11) NOT NULL,
                    `application_id` varchar(100) NOT NULL,
                    `b_skip` int(11) DEFAULT '0',
                    `b_limit` int(11) DEFAULT NULL,
                    `att_date` date DEFAULT NULL,
                    `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
                    `update_at` datetime DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """)

        cursor.execute("""
            ALTER TABLE `cron_tasks` ADD PRIMARY KEY (`id`);
        """)

        cursor.execute("""
            ALTER TABLE `cron_tasks` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
        """)

        db_connection.commit()
        print("Migration done \n")

    except Exception as e:
        print("Migration failed \n")
        raise e
    finally:
        db_connection.close()

if __name__ == '__main__':
    dotenv_path = Path('.env')
    load_dotenv(dotenv_path = dotenv_path)
    run_migration()