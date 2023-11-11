import requests
import zipfile
import yaml

from backend.utils.endpoints import *
from backend.utils.superset_constants import SUPERSET_PASSWORD, SUPERSET_USERNAME, SUPERSET_INSTANCE_URL


def get_access_token():
    login_data = {
        "username": SUPERSET_USERNAME,
        "password": SUPERSET_PASSWORD,
        "provider": "db"
    }

    # makes a post request to get access token

    # token = requests.post(SUPERSET_INSTANCE_URL + ACCESS_TOKEN_ENDPOINT, json=login_data)
    return requests.post(SUPERSET_INSTANCE_URL + ACCESS_TOKEN_ENDPOINT, json=login_data).json()["access_token"]


def get_csrf_token(access_token):
    headers = {"Authorization": "Bearer " + access_token}
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
    chart_endpoint = f'{SUPERSET_INSTANCE_URL}{DASHBOARD_ENDPOINT}{str(dashboard_id)}/charts/'
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
    # headers = {"Authorization": "Bearer " + access_token}
    headers = {'Authorization': 'Bearer {}'.format(access_token),
               'Content-Type': 'application/json'}
    print(headers)

    dashboard_endpoint = f'{SUPERSET_INSTANCE_URL}api/v1/dashboard/export/?q=[{dashboard_id}]'
    print(dashboard_endpoint)
    dashboards = requests.get(url=dashboard_endpoint, headers=headers)
    print(dashboards.content)
    local_path = "exported_one_dashboard.zip"
    with open(local_path, "wb") as f:
        f.write(dashboards.content)

    # extract the folder out of the zip file
    with zipfile.ZipFile(local_path) as myzip:
        myzip.extractall()

    # 36 corresponds to len("zip/dashboard_export_) + 15 (15 numbers at the end) to get name of extracted folder
    # make this dynamic, hard coded for now
    return myzip.namelist()[0][:36]


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


def import_new_dashboard(access_token, csrf_token, filename):
    zipfile.ZipFile(filename, mode='w')
    data = {
        "formData": filename,
        "override": False
    }
    headers = {
        "Authorization": "Bearer " + access_token,
        "X-CSRFToken": csrf_token
    }
    requests.post(url=SUPERSET_INSTANCE_URL + IMPORT_ENDPOINT, data=data, headers=headers)