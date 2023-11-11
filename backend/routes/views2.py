from flask import Blueprint, request
from backend.utils.api_helpers2 import *
import json
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
    print("reached clone function")
    dashboard_id = request.form.get("dashboard_id")
    print(dashboard_id)
    dashboard_old_name = request.form.get("dashboard_old_name")
    print(dashboard_old_name)
    dashboard_new_name = request.form.get("dashboard_new_name")
    print(dashboard_new_name)
    charts = request.form.get("charts")
    print(charts)

    access_token = get_access_token()
    print(access_token)
    extracted_folder_name = export_one_dashboard(access_token, dashboard_id)
    print("6")

    dashboard_filename = f'dashboards/{dashboard_old_name}_{dashboard_id}.yaml'
    print("7")
    set_new_details(dashboard_filename, [("dashboard_title", dashboard_new_name)])
    print("8")

    change_chart_details(charts, extracted_folder_name)
    print("9")

    csrf_token = get_csrf_token(access_token)
    print("10")
    import_new_dashboard(access_token, csrf_token, extracted_folder_name)
    print("11")

    # TODO: delete everything in "zip" folder


def change_chart_details(charts, extracted_folder_name):
    for chart in charts:
        chart_id = chart[0]
        chart_old_name = chart[1]
        chart_new_name = chart[2]
        chart_new_dataset = chart[3]
        database = chart[4]

        dataset_filename = f'{extracted_folder_name}/datasets/{database}/{chart_new_dataset}.yaml'
        dataset_uuid = get_dataset_uuid(dataset_filename)

        chart_filename = f'{extracted_folder_name}/charts/{chart_old_name}_{chart_id}.yaml'
        params = [
            ("dataset_uuid", dataset_uuid),
            ("slice_name", chart_new_name)
        ]
        set_new_details(chart_filename, params)
