import logging
import datetime

class Logger:
    
    _instance = None
    _logging = None
    
    def __init(self):
        raise RuntimeError('Call getInstance() instead')

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        x = datetime.datetime.now()
        date = x.strftime("%Y-%m-%d")
        logging.basicConfig(filename=f'logs/Xenos-{date}-app.log', filemode='a', format='%(asctime)s -  (process)d - %(levelname)s - %(message)s')
        cls._logging = logging
        return cls._instance

    def getLogger(cls):
        return cls._logging


logger = Logger()

