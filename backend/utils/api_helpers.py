import os

import requests
import zipfile
import yaml

from backend.utils.endpoints import *
from backend.utils.superset_constants import SUPERSET_PASSWORD, SUPERSET_USERNAME, SUPERSET_INSTANCE_URL
from backend.utils.utils import create_id


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
    print(SUPERSET_INSTANCE_URL + CSRF_TOKEN_ENDPOINT)
    return requests.get(SUPERSET_INSTANCE_URL + CSRF_TOKEN_ENDPOINT, headers=headers).json()["result"]


def get_dashboards(access_token):
    headers = {"Authorization": "Bearer " + access_token}
    dashboards = requests.get(SUPERSET_INSTANCE_URL + DASHBOARD_ENDPOINT, headers=headers).json()

    parsed_dashboards = []
    for dashboard in dashboards["result"]:
        parsed_dashboards.append((dashboard["id"], dashboard["dashboard_title"]))
    return parsed_dashboards


# ------------------------------ functions to send data to front end ---------------------------------------------------
def get_charts(access_token, dashboard_id):
    headers = {"Authorization": "Bearer " + access_token}
    chart_endpoint = f'{SUPERSET_INSTANCE_URL}{DASHBOARD_ENDPOINT}{str(dashboard_id)}/charts'
    charts = requests.get(chart_endpoint, headers=headers).json()

    parsed_charts = []
    for chart in charts["result"]:
        parsed_charts.append((chart["id"], chart["slice_name"]))
    return parsed_charts


def get_datasets(token):
    headers = {"Authorization": "Bearer " + token}
    datasets = requests.get(SUPERSET_INSTANCE_URL + DATASET_ENDPOINT, headers=headers).json()
    parsed_datasets = []
    for dataset in datasets["result"]:
        parsed_datasets.append((dataset["table_name"], dataset["database"]["database_name"]))
    return parsed_datasets


# ----------------------------------------------------------------------------------------------------------------------
def export_one_dashboard(access_token, dashboard_id):
    headers = {'Authorization': 'Bearer {}'.format(access_token),
               'Content-Type': 'application/json'}

    dashboard_endpoint = f'{SUPERSET_INSTANCE_URL}api/v1/dashboard/export/?q=[{dashboard_id}]'
    dashboards = requests.get(url=dashboard_endpoint, headers=headers)
    # print(dashboards.content)
    local_path = "zip/exported_one_dashboard.zip"
    with open(local_path, "wb") as f:
        f.write(dashboards.content)

    # extract the folder out of the zip file
    with zipfile.ZipFile(local_path) as myzip:
        myzip.extractall(path='./zip')

    print(myzip.namelist()[0][:32])
    # 32 corresponds to len("dashboard_export_) + 15 (15 numbers at the end) to get name of extracted folder
    # make this dynamic, hard coded for now
    return myzip.namelist()[0][:32]


def get_dataset_uuid(filename):
    with open(filename, 'r') as file:
        dataset_data = yaml.safe_load(file)
    return dataset_data["uuid"]


# params is of the format [(key, value)]
def set_new_details(filename, params):
    with open(filename, 'r') as file:
        file_data = yaml.safe_load(file)
        for key, value in params:
            file_data[key] = value
    with open(filename, 'w') as file:
        yaml.dump(file_data, file, sort_keys=False)


def change_chart_details(charts, extracted_folder_name):
    for chart in charts:
        chart_id = chart["chart_id"]
        chart_old_name = chart["chart_old_name"].replace(" ", "_")
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
                file_path = os.path.join(root, file)
                os.remove(file_path)

            for directory in dirs:
                dir_path = os.path.join(root, directory)
                delete_zip(dir_path)
                os.rmdir(dir_path)

    except OSError:
        print("Error occurred while deleting file")
