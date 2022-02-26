import unittest
from app import db, read, write, api
from app.util import isValidDate
import main
from dotenv import load_dotenv

from main import getEnv, getAttendanceDate
from pathlib import Path
load_dotenv(dotenv_path = Path('.env'))

class TestApi(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://some-endpoint"
        self.api = api.Api(self.base_url)

    def test_construct_uri_with_no_base_url(self):
        endpoint = f"{self.base_url}"
        _api = api.Api()
        self.assertEqual(_api.construct_uri(endpoint),self.base_url)
       
    def test_construct_uri(self):
        endpoint = "post"
        expected_str = f"{self.base_url}/{endpoint}"
        self.assertEqual(self.api.construct_uri(endpoint),expected_str)
        
    @unittest.expectedFailure 
    def test_post_request(self):
        pass

class TestLogger(unittest.TestCase):
    def setUp(self):
        pass

class TestUtil(unittest.TestCase): 
    def setUp(self):
        pass

    def test_is_valid_date_returns_error_on_none(self):
        with self.assertRaises(ValueError):
            isValidDate(None)

    def test_is_valid_date_returns_error_on_invalid_date(self):
        with self.assertRaises(ValueError):
            isValidDate("2015-01")
        
    def test_is_valid_date_passes_on_valid_date(self):
        isValidDate("2015-01-01")


class TestDb(unittest.TestCase):

    def setUp(self):
        user,password,database,host,port = getEnv()
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

        conn = db.DBConnector(host,user,password,database,port)
        self.conn = conn.getConnector()

    @unittest.skip("demonstrating skipping")
    def testadd1(self):
        self.assertEquals(add(4,5),9)    

    def test_if_conn_is_none(self):
        user,password,database,host,port = getEnv()
        conn = db.DBConnector(host,user,password,database,port)
        host,user,password,database,port = "","","","",""
        with self.assertRaises(Exception):
            conn = db.DBConnector(host,user,password,database,port)
           

    def test_if_conn_is_not_none(self):
       # self.assert
        conn = db.DBConnector(self.host,self.user,self.password,self.database,self.port)
        self.assertIsNotNone(conn) 


class TestWrite(unittest.TestCase):
    def setUp(self):
        user,password,database,host,port = getEnv()
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

        conn = db.DBConnector(host,user,password,database,port)
        self.conn = conn.getConnector()

    def test_write_raises_error(self):
        with self.assertRaises(TypeError) as d:
            write.Write(None)
    
    def test_write_doesnot_raise_error(self):
        write.Write(self.conn)

    def test_write_doesnot_raise_error(self):
        writer_db = write.Write(self.conn)
        # write_db.createAttendanceTaskParam()


class TestRead(unittest.TestCase):
    def setUp(self):
        user,password,database,host,port = getEnv()
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

        conn = db.DBConnector(host,user,password,database,port)
        self.conn = conn.getConnector()

    def test_read_raises_error(self):
        with self.assertRaises(TypeError):
            read.Read(None)  

    def test_read_doesnot_raise_error(self):
        read.Read(self.conn)     
        

class TestMigration(unittest.TestCase):
    def setUp(self):
        pass


class TestMain(unittest.TestCase):    
    def setUp(self):
        #insert record into table based on current date (if it doesnot exist)
        user,password,database,host,port = getEnv()
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

        conn = db.DBConnector(host,user,password,database,port)
        self.conn = conn.getConnector()

        # self.att_date = getAttendanceDate()
        # print(f"test: att_date {att_date}")
        # #createAttendanceTaskParam
        # writer_db = write.Write(self.conn)

    def test_main(self):
        main.main_init()


if __name__ == '__main__':

    unittest.main()