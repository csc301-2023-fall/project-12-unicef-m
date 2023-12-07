"""
This file contains all backend endpoints the frontend may call
"""

from flask import Blueprint, request
import json

from backend.utils.dashboard_details_helper import *
from backend.utils.data_helpers import *
from backend.utils.api_request_handler import APIRequestHandler

views = Blueprint('views', __name__)


@views.route('/all-dashboards', methods=['GET'])
def get_all_dashboards():
    """
    Expected Return Format
        [
            {
                "dashboard_id": id,
                "dashboard_name": "name",
                "dashboard_desc": "desc",
                "all_charts": [
                    {
                        "chart_id": chart_id,
                        "chart_name": "name"
                    },
                    {
                        "chart_id": chart_id,
                        "chart_name": "name"
                    },
                    <More Charts related to the dashboard>
                ]
            }

            {
                <More Dashboards>
            }
        ]
    """
    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)
    dashboards = get_dashboards(request_handler)

    dashboard_list = []
    for dashboard in dashboards:
        dashboard_id = dashboard[0]
        dashboard_name = dashboard[1]

        charts = get_charts(request_handler, dashboard_id)

        curr_dashboard_info = {
            "dashboard_id": dashboard_id,
            "dashboard_name": dashboard_name,
            "dashboard_desc": None,
            "all_charts": [{"chart_id": chart_id, "chart_name": chart_name} for chart_id, chart_name in charts]
        }
        dashboard_list.append(curr_dashboard_info)

    return json.dumps(dashboard_list)


@views.route('/all-datasets', methods=['GET'])
def get_all_datasets():
    """
    Expected Return Format
        [
            {
                "dataset_name": "name",
                "database_name": "name"
                "dataset_id": dataset_id,
            },
            {
                <More datasets>
            }
        ]
    """
    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)
    datasets = get_datasets(request_handler)
    dataset_list = []

    for dataset in datasets:
        dataset_name = dataset[0]
        db_name = dataset[1]
        dataset_id = dataset[2]

        curr_dataset_info = {
            "dataset_name": dataset_name,
            "database_name": db_name,
            "dataset_id": dataset_id,
        }

        dataset_list.append(curr_dataset_info)

    return json.dumps(dataset_list)


@views.route('/clone', methods=['POST'])
def clone():
    """
    Expected Return Format
       {
           "dashboard_id":
           "dashboard_old_name":
           "dashboard_new_name":
           "dataset_id":
           "charts": [
                        {
                        chart_id
                        chart_old_name
                        chart_new_name
                        "chart_new_dataset": "covid_vaccines",
                        "database": "examples"
                        }
                   ]
       }
    """
    dashboard_details = get_details(request)

    # Initialized all paths directly to avoid issues with relativity
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
    GRANDPARENT_DIR = os.path.abspath(os.path.join(PARENT_DIR, os.pardir))
    ZIP_DIR = os.path.join(GRANDPARENT_DIR, 'backend/zip')

    # Initialize a request handler which will be used to make any and all requests to Superset API
    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)
    print("request_handler")
    # Change all details within the dashboard files
    dashboard_export_name, zip_directory = modify_details(dashboard_details, request_handler, ZIP_DIR)
    
    # Initialize an API request handler with the instance that will receive the dashboard
    instance_url = dashboard_details.credentials['instance_url']
    username = dashboard_details.credentials['username']
    password = dashboard_details.credentials['password']
    import_request_handler = APIRequestHandler(instance_url, username, password)
    print("reached import")
    # Import the dashboard
    import_new_dashboard(import_request_handler, dashboard_export_name)
    print("finished import")
    # Delete the files in the zip folder that was used as a temporary destination
    # Comment out this function to be able to view the dashboard files
    delete_zip(zip_directory)
    return "Cloning Successful"
