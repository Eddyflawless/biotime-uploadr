# run application
/usr/local/bin/python3.9 python

# install
pip install -r requirements.txt

# run migrations
python3 migration.py

# cron settings
* * * * * cd /path-to-your-project && /usr/local/bin/python3.9 main.py  >> /dev/null 2>&1

# run test suite (all)
python3 -m unittest discover

# run test (single file)
chmod +x run.sh && ./run.sh

