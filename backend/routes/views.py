from flask import Blueprint, request
import json
import os

from backend.utils.api_helpers import *
from backend.utils.api_request_handler import APIRequestHandler
from backend.utils.superset_constants import SUPERSET_PASSWORD, SUPERSET_USERNAME, SUPERSET_INSTANCE_URL
from backend.utils.utils import create_id

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

        curr_dataset_info = {
            "dataset_name": dataset_name,
            "database_name": db_name
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
           "charts": [
                        [
                        chart_id
                        chart_old_name
                        # chart_new_name
                        chart_new_dataset
                        database
                        ]
                   ]
       }
    """
    dashboard_id = request.json.get("dashboard_id")
    dashboard_old_name = request.json.get("dashboard_old_name")
    dashboard_new_name = request.json.get("dashboard_new_name")
    charts = request.json.get("charts")

    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
    GRANDPARENT_DIR = os.path.abspath(os.path.join(PARENT_DIR, os.pardir))
    dir_of_interest = os.path.join(GRANDPARENT_DIR, 'backend/zip')

    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)

    extracted_folder_name = export_one_dashboard(request_handler, dashboard_id)
    dashboard_filename = get_dashboard_filename(dashboard_id, dashboard_old_name,
                                                dir_of_interest, extracted_folder_name)

    set_new_details(dashboard_filename, [("dashboard_title", dashboard_new_name), ("uuid", create_id())])
    change_chart_details(charts, extracted_folder_name)
    update_dashboard_uuids(charts, f'{dir_of_interest}/{extracted_folder_name}/charts/', dashboard_filename)

    import_new_dashboard(request_handler, extracted_folder_name)

    delete_zip(f"{dir_of_interest}/")
    return "Cloning Successful"
