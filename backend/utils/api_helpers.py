import os

import requests
import zipfile
import yaml

import re

from backend.utils.endpoints import *
from backend.utils.superset_constants import SUPERSET_PASSWORD, SUPERSET_USERNAME, SUPERSET_INSTANCE_URL
from backend.utils.utils import create_id


def get_dashboards(request_handler):
    dashboard_response = request_handler.get_request(DASHBOARD_ENDPOINT)
    dashboards = dashboard_response.json()

    parsed_dashboards = []
    for dashboard in dashboards.get("result"):
        parsed_dashboards.append((dashboard["id"], dashboard["dashboard_title"]))
    return parsed_dashboards


def get_charts(request_handler, dashboard_id):
    chart_endpoint = f'{DASHBOARD_ENDPOINT}{str(dashboard_id)}/charts'

    chart_response = request_handler.get_request(chart_endpoint)
    charts = chart_response.json()

    parsed_charts = []
    for chart in charts.get("result"):
        parsed_charts.append((chart["id"], chart["slice_name"]))
    return parsed_charts


def get_datasets(request_handler):
    dataset_response = request_handler.get_request(DATASET_ENDPOINT)
    datasets = dataset_response.json()

    parsed_datasets = []
    for dataset in datasets.get("result"):
        parsed_datasets.append((dataset["table_name"], dataset["database"]["database_name"]))
    return parsed_datasets


def export_one_dashboard(request_handler, dashboard_id):
    export_dashboard_endpoint = f'{EXPORT_ENDPOINT}?q=[{dashboard_id}]'
    export_response = request_handler.get_request(export_dashboard_endpoint)

    local_path = "zip/exported_one_dashboard.zip"
    with open(local_path, "wb") as f:
        f.write(export_response.content)

    # extract the folder out of the zip file
    with zipfile.ZipFile(local_path) as myzip:
        myzip.extractall(path='./zip')

    # 32 corresponds to len("dashboard_export_) + 15 (15 numbers at the end) to get name of extracted folder
    # make this dynamic, hard coded for now
    return myzip.namelist()[0][:32]


def get_dashboard_filename(dashboard_old_name, dir_of_interest, extracted_folder_name, dashboard_id):
    dashboard_old_name_parsed = dashboard_old_name.replace(" ", "_")
    dashboard_filename = f'{dir_of_interest}/{extracted_folder_name}/dashboards/{dashboard_old_name_parsed}_{dashboard_id}.yaml'
    return dashboard_filename


def set_new_details(filename, params):
    # params is of the format [(key, value)]
    with open(filename, 'r') as file:
        file_data = yaml.safe_load(file)
        for key, value in params:
            file_data[key] = value
    with open(filename, 'w') as file:
        yaml.dump(file_data, file, sort_keys=False)


def change_chart_details(charts, extracted_folder_name):
    for chart in charts:
        chart_id = chart["chart_id"]
        chart_clean_name = _remove_non_alphanumeric_except_spaces(chart["chart_old_name"])
        chart_old_name = chart_clean_name.replace(" ", "_")
        # chart_new_name = chart[2]
        chart_new_dataset = chart["chart_new_dataset"]
        database = chart["database"].replace(" ", "_")

        dataset_filename = f'zip/{extracted_folder_name}/datasets/{database}/{chart_new_dataset}.yaml'
        dataset_uuid = _get_dataset_uuid(dataset_filename)

        chart_filename = f'zip/{extracted_folder_name}/charts/{chart_old_name}_{chart_id}.yaml'
        params = [
            ("dataset_uuid", dataset_uuid),
            ("uuid", create_id())
            # ("slice_name", chart_new_name)
        ]
        set_new_details(chart_filename, params)


def update_dashboard_uuids(charts, charts_dir, dashboard_filepath):
    # Read the dashboard file
    with open(dashboard_filepath, 'r') as dashboard_file:
        dashboard_data = yaml.safe_load(dashboard_file)

        # Loop over all files in the charts directory
        for i in range(len(charts)):
            chart_id = charts[i]['chart_id']
            chart_clean_name = _remove_non_alphanumeric_except_spaces(charts[i]["chart_old_name"])
            chart_prefix = chart_clean_name.replace(" ", "_")
            chart_filename = f'{chart_prefix}_{chart_id}.yaml'

            # Read the chart file
            chart_file_path = os.path.join(charts_dir, chart_filename)

            assert chart_file_path.endswith('.yaml')
            assert os.path.isfile(chart_file_path)
            with open(chart_file_path, 'r') as chart_file:
                chart_data = yaml.safe_load(chart_file)

            chart_uuid = chart_data.get('uuid')
            # Update UUID in the dashboard data
            _update_uuid(chart_id, chart_uuid, dashboard_data)

            chart_file.close()

    # Write the updated dashboard data back to the dashboard file
    with open(dashboard_filepath, 'w') as dashboard_file:
        yaml.dump(dashboard_data, dashboard_file, default_flow_style=False)


def import_new_dashboard(request_handler, filename):
    with zipfile.ZipFile(f'{filename}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        _zipdir(f'zip/{filename}', zipf)

    files = [('formData', (f'{filename}.zip', open(f'{filename}.zip', 'rb'), 'application/zip'))]

    request_handler.post_request(IMPORT_ENDPOINT, files=files)

    return "Imported"


def delete_zip(path):
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file != '.dummy':
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

            for directory in dirs:
                dir_path = os.path.join(root, directory)
                delete_zip(dir_path)
                os.rmdir(dir_path)

    except OSError:
        print("Error occurred while deleting file")


def _get_dataset_uuid(filename):
    with open(filename, 'r') as file:
        dataset_data = yaml.safe_load(file)
    return dataset_data["uuid"]


def _remove_non_alphanumeric_except_spaces(input_string):
    return re.sub(r'[^a-zA-Z0-9\s]', '', input_string)


def _update_uuid(chart_id, chart_uuid, dashboard_data):
    for _, chart_info in dashboard_data.get('position', {}).items():
        if 'type' in chart_info:
            if chart_info.get('type') == 'CHART':
                meta = chart_info.get('meta', {})
                # Check if slice name matches
                if meta.get('chartId') == chart_id:
                    # Update the UUID
                    meta['uuid'] = chart_uuid
                    break


def _zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


# --------------------------------------- Temporary Until Refactoring is complete -----------------------
def get_access_token():
    login_data = {
        "username": SUPERSET_USERNAME,
        "password": SUPERSET_PASSWORD,
        "provider": "db"
    }

    # makes a post request to get access token
    return requests.post(SUPERSET_INSTANCE_URL + ACCESS_TOKEN_ENDPOINT, json=login_data).json()["access_token"]


def get_csrf_token(access_token):
    headers = {"Authorization": "Bearer " + access_token}
    return requests.get(SUPERSET_INSTANCE_URL + CSRF_TOKEN_ENDPOINT, headers=headers).json()["result"]
