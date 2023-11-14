import firebase_admin
from firebase_admin import db, credentials 

# Configuring Firebase 

def initialize_firebase() -> None:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://version-control-3b864-default-rtdb.firebaseio.com/"})