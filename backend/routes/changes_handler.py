from firebase_admin import db
from backend.utils.utils import create_id, get_datetime

class ChangesHandler:
    
    def __init__(self):
        self.root = db.reference()


    def add_changes(self, new_template):
        '''
        Function for creating a new change document.
        '''
        change_id = create_id()
        creation_time = get_datetime()
        template = new_template

        change = {
            "change_id": change_id,      
            "timestamp": creation_time,      
            "template": template        
        }

        # Add change to database 
        self.root.child('changes').child(change_id).set(change)
        
        return change_id
    

    def get_change(self, change_id):
        '''
        Function for retrieving a particular change.  
        '''
        reference = self.root.child('changes').child(change_id)
        change = reference.get()
        
        if not change:
            return None
        
        return change 

    
    def _delete_all_changes(self):
        """
        Private function for deleting all changes in the database
        """
        dashboards_ref = self.root.child('changes') 
        dashboards_ref.delete()
    