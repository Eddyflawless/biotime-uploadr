# run application
/usr/local/bin/python3.9 python

# install
pip install -r requirements.txt

# cron settings
* * * * * cd /path-to-your-project && /usr/local/bin/python3.9 main.py  >> /dev/null 2>&1


