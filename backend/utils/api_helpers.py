import os

import requests
import zipfile
import yaml

import re

from backend.utils.api_request_handler import APIRequestHandler
from backend.utils.endpoints import *
from backend.utils.superset_constants import SUPERSET_PASSWORD, SUPERSET_USERNAME, SUPERSET_INSTANCE_URL
from backend.utils.utils import create_id


def get_dashboards():
    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)
    dashboard_response = request_handler.get_request(DASHBOARD_ENDPOINT)
    dashboards = dashboard_response.json()

    parsed_dashboards = []
    for dashboard in dashboards.get("result"):
        parsed_dashboards.append((dashboard["id"], dashboard["dashboard_title"]))
    return parsed_dashboards


def get_charts(dashboard_id):
    chart_endpoint = f'{SUPERSET_INSTANCE_URL}{DASHBOARD_ENDPOINT}{str(dashboard_id)}/charts'

    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)
    chart_response = request_handler.get_request(chart_endpoint)
    charts = chart_response.json()

    parsed_charts = []
    for chart in charts.get("result"):
        parsed_charts.append((chart["id"], chart["slice_name"]))
    return parsed_charts


def get_datasets():
    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)
    dataset_response = request_handler.get_request(DATASET_ENDPOINT)
    datasets = dataset_response.json()

    parsed_datasets = []
    for dataset in datasets.get("result"):
        parsed_datasets.append((dataset["table_name"], dataset["database"]["database_name"]))
    return parsed_datasets


def export_one_dashboard(access_token, dashboard_id):
    headers = {'Authorization': 'Bearer {}'.format(access_token),
               'Content-Type': 'application/json'}

    dashboard_endpoint = f'{SUPERSET_INSTANCE_URL}api/v1/dashboard/export/?q=[{dashboard_id}]'
    dashboards = requests.get(url=dashboard_endpoint, headers=headers)

    local_path = "zip/exported_one_dashboard.zip"
    with open(local_path, "wb") as f:
        f.write(dashboards.content)

    # extract the folder out of the zip file
    with zipfile.ZipFile(local_path) as myzip:
        myzip.extractall(path='./zip')

    # 32 corresponds to len("dashboard_export_) + 15 (15 numbers at the end) to get name of extracted folder
    # make this dynamic, hard coded for now
    return myzip.namelist()[0][:32]


def get_dataset_uuid(filename):
    with open(filename, 'r') as file:
        dataset_data = yaml.safe_load(file)
    return dataset_data["uuid"]


def change_chart_details(charts, extracted_folder_name):
    for chart in charts:
        chart_id = chart["chart_id"]
        temp = remove_non_alphanumeric_except_spaces(chart["chart_old_name"])
        chart_old_name = temp.replace(" ", "_")
        # chart_new_name = chart[2]
        chart_new_dataset = chart["chart_new_dataset"]
        database = chart["database"].replace(" ", "_")

        dataset_filename = f'zip/{extracted_folder_name}/datasets/{database}/{chart_new_dataset}.yaml'
        dataset_uuid = get_dataset_uuid(dataset_filename)

        chart_filename = f'zip/{extracted_folder_name}/charts/{chart_old_name}_{chart_id}.yaml'
        params = [
            ("dataset_uuid", dataset_uuid),
            ("uuid", create_id())
            # ("slice_name", chart_new_name)
        ]
        set_new_details(chart_filename, params)


def remove_non_alphanumeric_except_spaces(input_string):
    return re.sub(r'[^a-zA-Z0-9\s]', '', input_string)


# params is of the format [(key, value)]
def set_new_details(filename, params):
    with open(filename, 'r') as file:
        file_data = yaml.safe_load(file)
        for key, value in params:
            file_data[key] = value
    with open(filename, 'w') as file:
        yaml.dump(file_data, file, sort_keys=False)


def update_dashboard_uuids(charts, charts_dir, dashboard_filepath):
    # Read the dashboard file
    with open(dashboard_filepath, 'r') as dashboard_file:
        dashboard_data = yaml.safe_load(dashboard_file)

        # Loop over all files in the charts directory
        for i in range(len(charts)):
            chart_id = charts[i]['chart_id']
            temp = remove_non_alphanumeric_except_spaces(charts[i]["chart_old_name"])
            chart_prefix = temp.replace(" ", "_")
            chart_filename = f'{chart_prefix}_{chart_id}.yaml'

            # Read the chart file
            chart_file_path = os.path.join(charts_dir, chart_filename)

            if not os.path.isfile(chart_file_path):
                breakpoint()
            assert chart_file_path.endswith('.yaml')
            assert os.path.isfile(chart_file_path)
            with open(chart_file_path, 'r') as chart_file:
                chart_data = yaml.safe_load(chart_file)

            chart_uuid = chart_data.get('uuid')
            # Update UUID in the dashboard data
            update_uuid(chart_id, chart_uuid, dashboard_data)

            chart_file.close()

    # Write the updated dashboard data back to the dashboard file
    with open(dashboard_filepath, 'w') as dashboard_file:
        yaml.dump(dashboard_data, dashboard_file, default_flow_style=False)


def update_uuid(chart_id, chart_uuid, dashboard_data):
    for _, chart_info in dashboard_data.get('position', {}).items():
        if 'type' in chart_info:
            if chart_info.get('type') == 'CHART':
                meta = chart_info.get('meta', {})
                # Check if slice name matches
                if meta.get('chartId') == chart_id:
                    # Update the UUID
                    meta['uuid'] = chart_uuid
                    break


def import_new_dashboard(access_token, csrf_token, filename):
    with zipfile.ZipFile(f'{filename}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(f'zip/{filename}', zipf)

    login_data = {
        "username": SUPERSET_USERNAME,
        "password": SUPERSET_PASSWORD,
        "provider": "db"
    }
    headers = {"Authorization": "Bearer " + access_token}
    files = [('formData', (f'{filename}.zip', open(f'{filename}.zip', 'rb'), 'application/zip'))]

    session = requests.Session()
    access_token = session.post(SUPERSET_INSTANCE_URL + ACCESS_TOKEN_ENDPOINT, json=login_data).json()["access_token"]
    csrf_token = session.get(SUPERSET_INSTANCE_URL + CSRF_TOKEN_ENDPOINT, headers=headers).json()["result"]

    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'X-CSRFToken': csrf_token,
    }

    response = session.post(SUPERSET_INSTANCE_URL + IMPORT_ENDPOINT, headers=headers, files=files)

    return "Imported"


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


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
