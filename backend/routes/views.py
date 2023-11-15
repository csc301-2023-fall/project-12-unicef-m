from flask import Blueprint, request
from backend.utils.api_helpers import *
import json
import os

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
    access_token = get_access_token()
    dashboards = get_dashboards(access_token)

    dashboard_list = []

    for dashboard in dashboards:
        dashboard_id = dashboard[0]
        dashboard_name = dashboard[1]

        charts = get_charts(access_token, dashboard_id)

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
    access_token = get_access_token()
    datasets = get_datasets(access_token)
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

    access_token = get_access_token()
    extracted_folder_name = export_one_dashboard(access_token, dashboard_id)

    dashboard_old_name_parsed = dashboard_old_name.replace(" ", "_")
    dashboard_filename = f'zip/{extracted_folder_name}/dashboards/{dashboard_old_name_parsed}_{dashboard_id}.yaml'

    set_new_details(dashboard_filename, [("dashboard_title", dashboard_new_name), ("uuid", create_id())])
    change_chart_details(charts, extracted_folder_name)
    update_dashboard_uuids(charts, f'zip/{extracted_folder_name}/charts/', dashboard_filename)

    csrf_token = get_csrf_token(access_token)
    import_new_dashboard(access_token, csrf_token, extracted_folder_name)

    delete_zip("zip/")
    return "Cloning Successful"
