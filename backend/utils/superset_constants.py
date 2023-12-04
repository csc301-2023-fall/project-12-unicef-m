"""
Defining constants for SUPERSET variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

# May change these variables to reference the login values instead of the values in the .env file
SUPERSET_INSTANCE_URL = os.environ.get('SUPERSET_INSTANCE_URL')
SUPERSET_USERNAME = os.environ.get('SUPERSET_USERNAME')
SUPERSET_PASSWORD = os.environ.get('SUPERSET_PASSWORD')
