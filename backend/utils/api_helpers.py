"""
This file will be used for any operations related to Superset API
"""

import os
import zipfile
from backend.utils.endpoints import *


def get_dashboards(request_handler):
    """
    Return all dashboards within the SUPERSET_INSTANCE_URL in the APIRequestHandler

    @param request_handler: An initialized APIRequestHandler
    @return: A list of [dashboard_ids: int, dashboard_title: str]
    """
    dashboard_response = request_handler.get_request(DASHBOARD_ENDPOINT)
    dashboards = dashboard_response.json()

    parsed_dashboards = []
    for dashboard in dashboards.get("result"):
        parsed_dashboards.append((dashboard["id"], dashboard["dashboard_title"]))
    return parsed_dashboards


def get_charts(request_handler, dashboard_id):
    """
    Return all charts related to the specified dashboard id
    within the SUPERSET_INSTANCE_URL in the APIRequestHandler

    @param request_handler: An initialized APIRequestHandler
    @param dashboard_id: An integer representing a dashboard within SUPERSET_INSTANCE_URL
    @return: A list of [chart_id: int, slice_name: str]
    """
    chart_endpoint = f'{DASHBOARD_ENDPOINT}{str(dashboard_id)}/charts'

    chart_response = request_handler.get_request(chart_endpoint)
    charts = chart_response.json()

    parsed_charts = []
    for chart in charts.get("result"):
        parsed_charts.append((chart["id"], chart["slice_name"]))
    return parsed_charts


def get_datasets(request_handler):
    """
    Return all datasets within the SUPERSET_INSTANCE_URL in the APIRequestHandler

    @param request_handler: An initialized APIRequestHandler
    @return: A list of [table_name: int, database_name: str]
    """
    dataset_response = request_handler.get_request(DATASET_ENDPOINT)
    datasets = dataset_response.json()

    parsed_datasets = []
    for dataset in datasets.get("result"):
        parsed_datasets.append((dataset["table_name"], dataset["database"]["database_name"], dataset["id"]))
    return parsed_datasets


def export_old_dashboard(request_handler, dashboard_id):
    """
    Export an existing dashboard from SUPERSET_INSTANCE_URL with dashboard_id into zip folder

    @param request_handler: An initialized APIRequestHandler
    @param dashboard_id: An integer representing a dashboard within SUPERSET_INSTANCE_URL
    @return: Returns the folder name with the dashboards information (within the zip folder)
    """
    export_dashboard_endpoint = f'{EXPORT_ENDPOINT}?q=[{dashboard_id}]'
    export_response = request_handler.get_request(export_dashboard_endpoint)

    local_path = "zip/dashboard.zip"
    with open(local_path, "wb") as f:
        f.write(export_response.content)

    # extract the folder out of the zip file
    with zipfile.ZipFile(local_path) as myzip:
        myzip.extractall(path='./zip')

    dashboard_export_name = myzip.namelist()[0].split('/', 1)[0]

    return dashboard_export_name


def import_new_dashboard(request_handler, filename):
    """
    Import the new dashboard to SUPERSET_INSTANCE_URL

    @param request_handler: An initialized APIRequestHandler
    @param filename: The filename of the zip file containing the dashboard info
    @param zip_directory: the directory of the zip folder
    @return: None
    """
    with zipfile.ZipFile(f'zip/{filename}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        _zipdir(f'zip/{filename}', zipf)

    files = [('formData', (f'zip/{filename}.zip', open(f'zip/{filename}.zip', 'rb'), 'application/zip'))]

    request_handler.post_request(IMPORT_ENDPOINT, files=files)


def _zipdir(path, ziph):
    """
    Zip a folder

    @param path: the folder to zip
    @param ziph: the zipfile handle
    @return: None
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))
