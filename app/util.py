import datetime

def isValidDate(date_value, date_format="%Y-%m-%d"):
    if date_value is None:
        raise ValueError("Attendance date cannot be None")

    date_value = str(date_value)
    try:
        datetime.datetime.strptime(date_value,date_format)
    except ValueError: 
        raise ValueError(f"Incorrect data format, should be {date_format}")    

