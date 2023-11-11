from flask import Blueprint, request
from backend.utils.api_helpers2 import *
import json
import os
views2 = Blueprint('views2', __name__)


@views2.route('/all-dashboards', methods=['GET'])
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

    print(dashboard_list)

    return json.dumps(dashboard_list)


@views2.route('/all-datasets', methods=['GET'])
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



@views2.route('/export--one-dashboard', methods=['POST'])
def one_dashboard():
    access_token = get_access_token()
    print(access_token)

    dashboard_id = 8
    extracted_folder_name = export_one_dashboard(access_token, dashboard_id)
    print(extracted_folder_name)



@views2.route('/clone', methods=['POST'])
def clone():
    dashboard_id = request.form.get("dashboard_id")
    dashboard_old_name = request.form.get("dashboard_old_name")
    dashboard_new_name = request.form.get("dashboard_new_name")
    charts = request.form.get("charts")

    access_token = get_access_token()
    extracted_folder_name = export_one_dashboard(access_token, dashboard_id)

    dashboard_old_name_parsed = dashboard_old_name.replace(" ", "_")
    dashboard_filename = f'zip/{extracted_folder_name}/dashboards/{dashboard_old_name_parsed}_{dashboard_id}.yaml'

    set_new_details(dashboard_filename, [("dashboard_title", dashboard_new_name)])

    change_chart_details(charts, extracted_folder_name)

    csrf_token = get_csrf_token(access_token)
    import_new_dashboard(access_token, csrf_token, extracted_folder_name)

    # set the path to the zip folder
    # path = "filepath to the zip folder"
    # delete_zip(path)


def delete_zip(path):
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)

            for directory in dirs:
                dir_path = os.path.join(root, directory)
                delete_zip(dir_path)
                os.rmdir(dir_path)

    except OSError:
        print("Error occurred while deleting file")


def change_chart_details(charts, extracted_folder_name):
    for chart in charts:
        chart_id = chart[0]
        chart_old_name = chart[1].replace(" ", "_")
        chart_new_name = chart[2]
        chart_new_dataset = chart[3]
        database = chart[4].replace(" ", "_")

        dataset_filename = f'{extracted_folder_name}/datasets/{database}/{chart_new_dataset}.yaml'
        dataset_uuid = get_dataset_uuid(dataset_filename)

        chart_filename = f'{extracted_folder_name}/charts/{chart_old_name}_{chart_id}.yaml'
        params = [
            ("dataset_uuid", dataset_uuid),
            ("slice_name", chart_new_name)
        ]
        set_new_details(chart_filename, params)
