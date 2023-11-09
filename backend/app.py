from flask import Flask, request, jsonify
from firebase_config import initialize_firebase
from utils import create_id, get_datetime
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


@app.route('/')
def for_ta():
    html_string = """
        <h1>TA, Please Read Below: </h1>
        <h4>* Please note that this HTML page is only being rendered for the purposes of Deliverable 2 *</h4>
        <p>This is our submission. For the time being, it is currently hosted on: <br /> deliverable-2-12-3-mistr156-mongarud.vercel.app <br /></p>
        <p>The data currently on Firebase is the following: </p>
        <pre>
    {
        "changes": {
            "22ea6ef9-a20a-4dbf-ba5f-f7b4462ea16d": {
            "change_id": "22ea6ef9-a20a-4dbf-ba5f-f7b4462ea16d",
            "template": "template_3"
            },
            "4948dbc3-c511-43a2-9975-795d4cb826b0": {
            "change_id": "4948dbc3-c511-43a2-9975-795d4cb826b0",
            "template": "template_4"
            },
            "6ef05aba-bea3-4a14-94c2-106753ac586b": {
            "change_id": "6ef05aba-bea3-4a14-94c2-106753ac586b",
            "template": "template_2"
            },
            "7007f5bb-f2d6-4ca8-b64d-66b793abb82c": {
            "change_id": "7007f5bb-f2d6-4ca8-b64d-66b793abb82c",
            "template": "template_1"
            },
            "c7d94b41-a17f-4bac-9015-480cb239a100": {
            "change_id": "c7d94b41-a17f-4bac-9015-480cb239a100",
            "template": "template_1_v2"
            }
        },
        "dashboards": {
            "0507c4cc-3831-4742-9b9f-364143ca1080": {
            "changes": [
                "6ef05aba-bea3-4a14-94c2-106753ac586b"
            ],
            "clones": [
                "41012f4e-7b94-4945-a039-02b65c7af1f9"
            ],
            "dashboard_id": "0507c4cc-3831-4742-9b9f-364143ca1080",
            "dashboard_name": "test_2",
            "incoming_changes": "c7d94b41-a17f-4bac-9015-480cb239a100",
            "parent_id": "9a92545f-79ef-4470-a8a5-e3139352dc74",
            "superset_id": "test_2_superset",
            "template": "template_2"
            },
            "41012f4e-7b94-4945-a039-02b65c7af1f9": {
            "changes": [
                "4948dbc3-c511-43a2-9975-795d4cb826b0"
            ],
            "clones": "-1",
            "dashboard_id": "41012f4e-7b94-4945-a039-02b65c7af1f9",
            "dashboard_name": "test_4",
            "incoming_changes": "c7d94b41-a17f-4bac-9015-480cb239a100",
            "parent_id": "0507c4cc-3831-4742-9b9f-364143ca1080",
            "superset_id": "test_4_superset",
            "template": "template_4"
            },
            "82a2010a-d13d-4b55-a95e-07a324aba1df": {
            "changes": [
                "22ea6ef9-a20a-4dbf-ba5f-f7b4462ea16d"
            ],
            "clones": "-1",
            "dashboard_id": "82a2010a-d13d-4b55-a95e-07a324aba1df",
            "dashboard_name": "test_3",
            "incoming_changes": "c7d94b41-a17f-4bac-9015-480cb239a100",
            "parent_id": "9a92545f-79ef-4470-a8a5-e3139352dc74",
            "superset_id": "test_3_superset",
            "template": "template_3"
            },
            "9a92545f-79ef-4470-a8a5-e3139352dc74": {
            "changes": [
                "7007f5bb-f2d6-4ca8-b64d-66b793abb82c",
                "c7d94b41-a17f-4bac-9015-480cb239a100"
            ],
            "clones": [
                "0507c4cc-3831-4742-9b9f-364143ca1080",
                "82a2010a-d13d-4b55-a95e-07a324aba1df"
            ],
            "dashboard_id": "9a92545f-79ef-4470-a8a5-e3139352dc74",
            "dashboard_name": "test_1",
            "superset_id": "test_1_superset",
            "template": "template_1_v2"
            }
        }
    }</pre>

    <p>As shown above, we currently have 4 dashboard - "test_1", "test_2", "test_3", "test_4" (these are dashboard names), and
    "test_1" has clones "test_2" and "test_3", and "test_2" has clone "test_4".</p>
    <p>Please view app.py within our repository to see the available endpoints.</p>
    <p>Pleaase use Postman to make the relevant GET/POST requests to manipulate the data stored on Firebase.</p>
    """

    return html_string


# get dashboard, pass 'dashboard-id' as query parameter
@app.route('/api/get-dashboard/<dashboard_id>', methods=["GET"])
def get_dashboard(dashboard_id):
    # dashboard_id = request.args.get('dashboard-id')
    print(dashboard_id)
    dashboard = dashboard_handler.get_dashboard(dashboard_id)
    if dashboard:
        return jsonify(dashboard), 200
    else:
        return jsonify({'error': 'Dashboard Not Found'}), 404
    

# add dashboard, put in query parameters the following:
# dashboard_name: name of dashboard, 
# superset_id: superset_id of dashboard, 
# template: template of dashboard
# eg: /api/add-dashboard/?dashboard-name='<name>'&superset-id='<id>'&template='<template>'
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


# pass in parameters dashboard-id and template
# eg /api/update-dashboard/?dashboard-id='<id>'&template='<template>'
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