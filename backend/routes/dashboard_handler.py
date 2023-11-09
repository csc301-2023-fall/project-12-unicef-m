from firebase_admin import db
from backend.utils.utils import create_id, get_datetime

# This file will do the bulk of the database and version control work

class DashboardHandler:
    
    def __init__(self):
        self.root = db.reference()


    def add_dashboard(self, dashboard_name, superset_id, template, changesHandlerInstance):
        '''
        Function that handles creating/adding dashboards to Firebase.
        '''
        dashboard_id = create_id()
        parent_id = None
        creation_time = get_datetime()

        changes = [changesHandlerInstance.add_changes(template)] 
        clones = "-1"

        new_db = {
            "dashboard_name": dashboard_name,
            "superset_id": superset_id,
            "dashboard_id": dashboard_id,
            "template": template,
            "parent_id": parent_id,
            "creation_time": creation_time,
            "clones": clones,
            "changes": changes,
            "incoming_change": None
        }

        self.root.child('dashboards').child(dashboard_id).set(new_db)
        return dashboard_id


    def get_dashboard(self, dashboard_id):
        '''
        Function that retrieves the dashboard with <dashboard_id> from Firebase.
        '''
        reference = self.root.child('dashboards').child(dashboard_id)
        dashboard = reference.get()
        
        if not dashboard:
            return None
        
        return dashboard 
    

    def _get_dashboard_ref(self, dashboard_id):
        '''
        Private function that retrives a reference to the dashboard with <dashboard_id>
        so that it can be modified in other functions.
        '''
        return self.root.child('dashboards').child(dashboard_id)
    

    def _make_clone_forcefully(self, parent_dashboard_id, clone_dashboard_id):
        '''
        Private function that forcefully adds "cloning" relationships between exiting 
        dashboards for testing purposes.
        '''
        parent_ref = self._get_dashboard_ref(parent_dashboard_id)
        parent_dashboard = self.get_dashboard(parent_dashboard_id)
        clone_ref = self._get_dashboard_ref(clone_dashboard_id)

        new_clones =  None 
        curr_clones = parent_dashboard['clones']

        if curr_clones == '-1':
            new_clones = [clone_dashboard_id]
        else:
            new_clones = curr_clones.copy()
            new_clones.append(clone_dashboard_id)

        print(new_clones)

        parent_ref.update({
            "clones": new_clones
        })

        clone_ref.update({
            'parent_id': parent_dashboard_id
        })
    
    
    def find_parent(self, dashboard_id, original: bool = False):
        '''
        Function that returns the parent which the input dashboard is a clone of.
        '''
        curr_db = self.get_dashboard(dashboard_id)

        if not original:
            if curr_db['parent_id']:
                return self.get_dashboard(curr_db['parent_id'])

        while curr_db["parent_id"]:
            curr_db = self.get_dashboard(curr_db["parent_id"])

        return curr_db

    
    def get_full_history(self, dashboard_id):
        '''
        Function that returns the history of all changes of the dashboard.
        '''
        curr_db = self.get_dashboard(dashboard_id)
        return curr_db["changes"]

    
    def update_dashboard(self, dashboard_id, changesHandlerInstance, template = None, incoming_changes = None):
        '''
        Function used to update information for a particular dashboard.
        '''
        dashboard_ref = self._get_dashboard_ref(dashboard_id) 
        dashboard = self.get_dashboard(dashboard_id)

        if not dashboard_ref:
            return None

        if template:
            curr_changes, new_change = dashboard['changes'], changesHandlerInstance.add_changes(template)
            new_changes = curr_changes.copy()
            new_changes.append(new_change)
            dashboard_ref.update({
                'template': template,
                'changes': new_changes
            })
        
        if incoming_changes:
            dashboard_ref.update({
                'incoming_changes': incoming_changes
            })
 
    
    def propogate_changes(self, dashboard_id, changesHandlerInstance): 
        '''
        Function to propagate changes from a dashboard to all of its children.
        '''
        curr_dashboard = self.get_dashboard(dashboard_id)
        curr_change = curr_dashboard['changes'][-1]
        stack = [x for x in curr_dashboard['clones']] # x = clone_dashboard_id
        visited = set()

        while stack:
            curr_id = stack.pop()

            if curr_id in visited or curr_id == '-1':
                continue

            visited.add(curr_id)
            
            self.add_incoming_change(curr_id, curr_change)
            # self.update_dashboard(curr_id, changesHandlerInstance, incoming_changes=curr_change)

            curr_db = self.get_dashboard(curr_id)
            if curr_db['clones'] != '-1':
                stack.extend(curr_db['clones'])
                
                
    def add_incoming_change(self, dashboard_id, change_id):
        curr_dashboard = self.get_dashboard(dashboard_id)
        curr_dashboard['incoming_change'] = change_id
        
    
    def accept_incoming_change(self, dashboard_id, changesHandlerInstance):
        '''
        Function to make a particular dashboard accept incoming changes.
        '''
        curr_dashboard = self.get_dashboard(dashboard_id)
        new_template = curr_dashboard['incoming_change']

        if new_template:
            self.update_dashboard(dashboard_id, changesHandlerInstance, incoming_changes=new_template)
    
    
    def check_for_incoming_change(self, dashboard_id):
        """
        Function to check if there is an incoming change.
        """
        curr_dashboard = self.get_dashboard(dashboard_id)
        return curr_dashboard['incoming_change']
    
    
    def get_dashboard_information(self, dashboard_id):
        """
        Function to check if there is an incoming change.
        """
        curr_dashboard = self.get_dashboard(dashboard_id)
        
      
    def delete_dashboard(self, dashboard_id):
        '''
        Function to delete a particular dashboard.
        '''
        dashboard_ref = self.root.child('dashboards').child(dashboard_id)
        dashboard_ref.delete()


    def _delete_all_dashboards(self):
        '''
        Private function to delete all dashboards in Firebase.
        '''
        dashboards_ref = self.root.child('dashboards') 
        dashboards_ref.delete()