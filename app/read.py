
from pprint import pprint

class Read:

    def __init__(self,conn):
        self.conn = conn
        if conn is None:
            raise TypeError("Connection object cannot be None")
        self.batch_size = 20
        self.batch_skip = 0

    def getAttendanceTaskParam(self,att_date):

        try:

            cursor = self.conn.cursor(dictionary=True)
            limit = self.batch_size
            skip = self.batch_skip

            sql = "Select * from cron_tasks where att_date = '%s' limit 1" % (att_date)
            cursor.execute(sql)
            record = cursor.fetchone()

            if record:
                self.batch_size = record['b_limit']
                self.batch_skip = record['b_skip']    

            return record           

        except Exception as e:
            print(e)
            raise e 
    

    def getIClockTransactions(self, att_date):
        try:

            cursor = self.conn.cursor(dictionary=True)
            self.getAttendanceTaskParam(att_date)

            limit = self.batch_size;
            skip = self.batch_skip;
    
            sql = "Select * from iclock_transaction where date(punch_time) = '%s' limit %s,%s " % (att_date, skip, limit);
            cursor.execute(sql)
            return cursor.fetchall()

        except Exception as e:
            print(e)
            raise e
     