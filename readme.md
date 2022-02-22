# run application
/usr/local/bin/python3.9 python

# install
pip install -r requirements.txt

# cron settings
* * * * * cd /path-to-your-project && /usr/local/bin/python3.9 main.py  >> /dev/null 2>&1

# run test (single file)
python3 -m -v unittest tests/test.py

# run test suite (all)
python3 -m unittest discover

