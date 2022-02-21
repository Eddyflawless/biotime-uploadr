from mysql import connector
from mysql.connector import Error

from app.logger import Logger
xlogger = Logger.getInstance().getLogger()

class DBConnector:
    
    def __init__(self,host,user,password,database,port):
        self.status = 0
        try:

            db_connection =  connector.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                database=database,
                raise_on_warnings=True
            )
            self.connector = db_connection

        except Exception as e:
            xlogger.error(e)
            raise e

    def getConnector(self):
        return self.connector