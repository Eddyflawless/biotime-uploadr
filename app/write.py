
class Write:
   
    def __init__(self,conn):
        self.conn = conn

    def updateAttendanceTaskParam(self,att_date, skip):

        cursor = self.conn.cursor(dictionary=True)
        sql = "UPDATE cron_tasks set b_skip = '%s' where att_date = '%s' " % (skip, att_date );
        cursor.execute(sql);
        self.conn.commit()

    def createAttendanceTaskParam(self, att_date):
        cursor = self.conn.cursor(dictionary=True)
        sql =  "INSERT into cron_tasks set b_skip = 0, b_limit = 20 , att_date='%s'" % (att_date)
        cursor.execute(sql)
        self.conn.commit()

