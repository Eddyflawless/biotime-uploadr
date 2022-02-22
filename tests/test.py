import unittest


class TestApi(unittest.TestCase):

    def test_construct_uri(self):
        self.assertEqual(5,15)
        
    def test_post_request(self):
        pass    

class TestLogger(unittest.TestCase):
    pass

class TestDbRead(unittest.TestCase):
    pass

class TestDbWrite(unittest.TestCase):
    pass

class TestMigration(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()