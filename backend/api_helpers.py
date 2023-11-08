import requests
import zipfile

import yaml

from endpoints import DASHBOARD_ENDPOINT, DATASET_ENDPOINT
from superset_constants import SUPERSET_PASSWORD, SUPERSET_USERNAME, SUPERSET_INSTANCE_URL


def get_access_token():
    login_data = {
        "username": SUPERSET_USERNAME,
        "password": SUPERSET_PASSWORD,
        "provider": "db"
    }

    # makes a post request to get access token
    token = requests.post(SUPERSET_INSTANCE_URL + "/api/v1/security/login", json=login_data).json()["access_token"]
    return token


def get_dashboards(token):
    # using the token to get all the dashboards
    headers = {"Authorization": "Bearer " + token}
    dashboards = requests.get(SUPERSET_INSTANCE_URL + DASHBOARD_ENDPOINT, headers=headers).json()

    dashboard_names = []
    for dashboard in dashboards["result"]:
        dashboard_names.append((dashboard["id"], dashboard["dashboard_title"]))
    return dashboard_names


def get_charts(token, dashboard_id):
    headers = {"Authorization": "Bearer " + token}
    charts = requests.get(SUPERSET_INSTANCE_URL + DASHBOARD_ENDPOINT + str(dashboard_id) + '/charts',
                          headers=headers).json()
    chart_names = []
    for chart in charts["result"]:
        chart_names.append(chart["slice_name"])
    return chart_names


def get_charts_with_ID(token, dashboard_id):
    headers = {"Authorization": "Bearer " + token}
    charts = requests.get(SUPERSET_INSTANCE_URL + DASHBOARD_ENDPOINT + str(dashboard_id) + '/charts',
                          headers=headers).json()
    chart_names = []
    for chart in charts["result"]:
        chart_names.append((chart["slice_name"], chart["id"]))
    return chart_names


def get_datasets(token):
    headers = {"Authorization": "Bearer " + token}
    datasets = requests.get(SUPERSET_INSTANCE_URL + DATASET_ENDPOINT, headers=headers).json()
    dataset_names = []
    for dataset in datasets["result"]:
        dataset_names.append(dataset["table_name"])
    return dataset_names


def export_dashboards(token):
    headers = {"Authorization": "Bearer " + token}
    dashboards = requests.get(SUPERSET_INSTANCE_URL + 'api/v1/assets/export', headers=headers)
    local_path = "exported_dashboards.zip"
    with open(local_path, "wb") as f:
        f.write(dashboards.content)


def export_one_dashboard(token, dashboard_id):
    headers = {"Authorization": "Bearer " + token}

    dashboards = requests.get(url=SUPERSET_INSTANCE_URL + 'api/v1/dashboard/export?q=[' + dashboard_id + ']',
                              headers=headers)
    local_path = "exported_one_dashboard.zip"
    with open(local_path, "wb") as f:
        f.write(dashboards.content)

    with zipfile.ZipFile('exported_one_dashboard.zip') as myzip:
        myzip.extractall()
    return myzip.namelist()[0][:32]  # getting the name of extracted folder, change to be dynamic later


def get_dataset_uuid(filename):
    with open(filename, 'r') as file:
        dataset_data = yaml.safe_load(file)
        print(dataset_data["uuid"])
    return dataset_data["uuid"]


def set_chart_dataset(filename, new_dataset, new_name):
    with open(filename, 'r') as file:
        chart_data = yaml.safe_load(file)
        chart_data["dataset_uuid"] = new_dataset
        chart_data["slice_name"] = new_name

    with open(filename, 'w') as file:
        yaml.dump(chart_data, file, sort_keys=False)
