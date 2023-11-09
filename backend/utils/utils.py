import uuid
import datetime

# This file will store commonly used operations

def create_id():
    return str(uuid.uuid4())

def get_datetime():
    datetime.datetime.now()
