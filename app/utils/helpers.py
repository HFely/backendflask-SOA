import re
from datetime import datetime

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_date(value, format='%Y-%m-%d'):
    if value is None:
        return ""
    return value.strftime(format)