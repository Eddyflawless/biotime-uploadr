
from app.util import isValidDate

class Write:
   
    def __init__(self,conn):
        if conn is None:
            raise TypeError("Connection object cannot be None")
        self.conn = conn

    def updateAttendanceTaskParam(self,att_date, skip):

        try:
            isValidDate(att_date)    
            cursor = self.conn.cursor(dictionary=True)

            sql = "UPDATE cron_tasks set b_skip = '%s' where att_date = '%s' " % (skip, att_date );
            cursor.execute(sql);
            self.conn.commit()
            return True

        except Error as e:
            raise e    


    def createAttendanceTaskParam(self, att_date=None):
        try:

            #check att_date format is a valid date    
            isValidDate(att_date)    

            cursor = self.conn.cursor(dictionary=True)
            sql =  "INSERT into cron_tasks set b_skip = 0, b_limit = 20 , att_date='%s'" % (att_date)
            cursor.execute(sql)
            self.conn.commit()
            return True

        except Error as e:
            raise e



