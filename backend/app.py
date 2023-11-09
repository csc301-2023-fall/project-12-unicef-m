from flask import Flask, request, jsonify
from firebase_config import initialize_firebase
from dashboard_handler import DashboardHandler
from changes_handler import ChangesHandler

# This file will handle HTTP requests and responses

# Current JSON for dahsboard schema:
    
# {
#   "dashboard_name": "string",     # Name of dashboard
#   "superset_id": "integer",       # Superset ID of the dashboard
#   "dashboard_id": "string",       # Unique DID we create for a dashboard; using strings for UUIDs
#   "template": "string",           # The actual content of the dashboard in JSON format
#   "parent_id": "string",          # 'null' if none, else unique DID
#   "creation_time": "string",      # The creation timestamp of the dashboard?
#   "clones": ["string"]            # List of (dashboard) IDs of children/clones of current dashboard  - each has same schema as this.
#   "incoming_change": "string"     # most recent change_ID
#   "changes": ["string"]           # List of change_IDs, each change represents change to dashboard, in chronological order
# }

# Current JSON for changes schema:

# {
#   "change_id": "string",      # Unique ID for this change and again, string for UUID
#   "timestamp": "string",      # When this change was made
#   "template": "string"        # The content of the dashboard after this change
# }

app = Flask(__name__)
initialize_firebase()
dashboard_handler = DashboardHandler()
changes_handler = ChangesHandler()

"""
get dashboard, pass 'dashboard-id' as query parameter
"""
@app.route('/api/get-dashboard/<dashboard_id>', methods=["GET"])
def get_dashboard(dashboard_id):
    # dashboard_id = request.args.get('dashboard-id')
    print(dashboard_id)
    dashboard = dashboard_handler.get_dashboard(dashboard_id)
    if dashboard:
        return jsonify(dashboard), 200
    else:
        return jsonify({'error': 'Dashboard Not Found'}), 404
    
"""
add dashboard, put in query parameters the following:
dashboard_name: name of dashboard, 
superset_id: superset_id of dashboard, 
template: template of dashboard
eg: /api/add-dashboard/?dashboard-name='<name>'&superset-id='<id>'&template='<template>'
"""
@app.route('/api/add-dashboard/', methods=["POST"])
def add_dashboard():
    dashboard_name = request.args.get('dashboard-id', None)
    superset_id = request.args.get('superset-id', None)
    template = request.args.get('template', None)

    if not(dashboard_name, superset_id, template): 
        return jsonify({'error': "Missing parameters"}), 422
    
    new_db_id = dashboard_handler.add_dashboard(dashboard_name, superset_id, template, changes_handler)

    return jsonify({
        'new_db_id': new_db_id
    }), 200


@app.route('/api/full-history/<dashboard_id>', methods=["GET"])
def get_full_history(dashboard_id):
    changes = dashboard_handler.get_full_history(dashboard_id) # changes are in chronological order - i.e. oldest change first
    res = {}

    for change in changes:
        curr_change = changes_handler.get_change(change)
        res[curr_change['timestamp']] = curr_change['template']

    return jsonify(res), 200

"""
pass in parameters dashboard-id and template
eg /api/update-dashboard/?dashboard-id='<id>'&template='<template>'
"""
@app.route('/api/update-dashboard/', methods=["POST"])
def update_dashboard():
    dashboard_id = request.args.get('dashboard_id', None)

    if not dashboard_id:
        return jsonify({'error': 'incorrect dashboard_id'}), 422
    
    template = request.args.get('template', None)

    if not template:
        return jsonify({'error': 'template parameter missing'}), 422
    
    dashboard_handler.update_dashboard(dashboard_id, changes_handler, template=template)
    return jsonify({'message': "success"}), 200


@app.route('/api/propagate-changes/<dashboard_id>', methods=["POST"])
def propagate_changes(dashboard_id):
    dashboard_handler.propogate_changes(dashboard_id, changes_handler)

    return jsonify({'Message': "Success"}), 200


@app.route('/api/accept-incoming-changes/<dashboard_id>', methods=["POST"])
def accept_incoming_changes(dashboard_id):
    dashboard_handler.accept_incoming_change(dashboard_id, changes_handler)
    
    return jsonify({'Message': "Success"}), 200


# TODO Test
# Make this actually connect properly propogate -> accept
"""
Endpoint for displaying incoming change
"""
@app.route('/api/get-incoming-change/<dashboard_id>', methods=["GET"])
def get_incoming_changes(dashboard_id):
    dashboard_handler.check_for_incoming_change(dashboard_id, changes_handler)
    #message = boolean
    return jsonify({'Message': True}), 200 #change True to message
 
 

"""
Endpoint to get dashboard time, desc., name of change_id
"""
@app.route('/api/get-incoming-change/<dashboard_id>', methods=["GET"])
def get_dashboard_information(dashboard_id):
    pass


# GitHub Authorizaiton, set up auth 0





# Added a sample dashboard to firebase:


def create_sample_dashboard():
    d1 = dashboard_handler.add_dashboard("test_1", "test_1_superset", "template_1", changes_handler)
    d2 = dashboard_handler.add_dashboard("test_2", "test_2_superset", "template_2", changes_handler)
    d3 = dashboard_handler.add_dashboard("test_3", "test_3_superset", "template_3", changes_handler)
    d4 = dashboard_handler.add_dashboard("test_4", "test_4_superset", "template_4", changes_handler)

    dashboard_handler._make_clone_forcefully(d1, d2)
    dashboard_handler._make_clone_forcefully(d1, d3)
    dashboard_handler._make_clone_forcefully(d2, d4)

    dashboard_handler.update_dashboard(d1, changes_handler, template="template_1_v2")
    dashboard_handler.propogate_changes(d1, changes_handler)
    

def delete_all_in_database():
    dashboard_handler._delete_all_dashboards()
    changes_handler._delete_all_changes()


if __name__ == "__main__":
    delete_all_in_database()
    create_sample_dashboard()