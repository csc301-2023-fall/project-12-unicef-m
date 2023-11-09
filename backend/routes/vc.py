from flask import Blueprint, request, jsonify
from backend.routes.dashboard_handler import DashboardHandler
from backend.routes.changes_handler import ChangesHandler

vc = Blueprint('vc', __name__)
dashboard_handler = DashboardHandler()
changes_handler = ChangesHandler()

# Current JSON for dashboard schema:
    
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

@vc.route('/')
def hello_world():
    return("<p> hello world </p>")


"""
Get a dashboard, pass 'dashboard-id' as query parameter
"""
@vc.route('/api/get-dashboard/<dashboard_id>', methods=["GET"])
def get_dashboard(dashboard_id):
    # dashboard_id = request.args.get('dashboard-id')
    print(dashboard_id)
    dashboard = dashboard_handler.get_dashboard(dashboard_id)
    if dashboard:
        return jsonify(dashboard), 200
    else:
        return jsonify({'error': 'Dashboard Not Found'}), 404
    

"""
Add a dashboard, put in query parameters the following:
dashboard_name: name of dashboard, 
superset_id: superset_id of dashboard, 
template: template of dashboard
eg: /api/add-dashboard/?dashboard-name='<name>'&superset-id='<id>'&template='<template>'
"""
@vc.route('/api/add-dashboard/', methods=["POST"])
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


"""
Get the full history of changes for a dashboard, pass 'dashboard-id' as query parameter
"""
@vc.route('/api/full-history/<dashboard_id>', methods=["GET"])
def get_full_history(dashboard_id):
    changes = dashboard_handler.get_full_history(dashboard_id) # changes are in chronological order - i.e. oldest change first
    res = {}

    for change in changes:
        curr_change = changes_handler.get_change(change)
        res[curr_change['timestamp']] = curr_change['template']

    return jsonify(res), 200


"""
Pass in parameters dashboard-id and template
eg /api/update-dashboard/?dashboard-id='<id>'&template='<template>'
"""
@vc.route('/api/update-dashboard/', methods=["POST"])
def update_dashboard():
    dashboard_id = request.args.get('dashboard_id', None)

    if not dashboard_id:
        return jsonify({'error': 'incorrect dashboard_id'}), 422
    
    template = request.args.get('template', None)

    if not template:
        return jsonify({'error': 'template parameter missing'}), 422
    
    dashboard_handler.update_dashboard(dashboard_id, changes_handler, template=template)
    return jsonify({'message': "success"}), 200



@vc.route('/api/propagate-changes/<dashboard_id>', methods=["POST"])
def propagate_changes(dashboard_id):
    dashboard_handler.propogate_changes(dashboard_id, changes_handler)

    return jsonify({'Message': "Success"}), 200



@vc.route('/api/accept-incoming-changes/<dashboard_id>', methods=["POST"])
def accept_incoming_changes(dashboard_id):
    dashboard_handler.accept_incoming_change(dashboard_id, changes_handler)
    
    return jsonify({'Message': "Success"}), 200


# TODO Test
# Make this actually connect properly propogate -> accept
"""
Endpoint for displaying incoming change
"""
@vc.route('/api/get-incoming-change/<dashboard_id>', methods=["GET"])
def get_incoming_changes(dashboard_id):
    dashboard_handler.check_for_incoming_change(dashboard_id, changes_handler)
    #message = boolean
    return jsonify({'Message': True}), 200 #change True to message
 
 
"""
Endpoint to get dashboard time, desc., name of change_id
"""
@vc.route('/api/get-incoming-change/<dashboard_id>', methods=["GET"])
def get_dashboard_information(dashboard_id):
    pass