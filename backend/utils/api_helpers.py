import os
import shutil

import zipfile
import yaml
import re

from backend.utils.endpoints import *
from backend.utils.utils import create_id


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


def export_one_dashboard(request_handler, dashboard_id):
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


def get_dashboard_filename(dashboard_id, dashboard_old_name, zip_dir, extracted_folder_name):
    """
    Get the full path to the dashboard file

    @param dashboard_id: The dashboard_id of the dashboard
    @param dashboard_old_name: The original name of the dashboard
    @param zip_dir: The full path to the zip file
    @param extracted_folder_name: The folder within the zip file created from export_one_dashboard()
    @return: The full path of the dashboard file
    """
    dashboard_old_name_parsed = _cleaned_filename(dashboard_old_name)
    d1 = f'{zip_dir}/{extracted_folder_name}/dashboards/'
    d2 = f'{dashboard_old_name_parsed}_{dashboard_id}.yaml'

    dashboard_filename = d1 + d2
    return dashboard_filename


def modify_dataset_and_database(request_handler, zip_dir, dashboard_export, dataset_id):
    """
    Updates the dataset and database folders within the extracted dashboard file
    Replaces the dataset and database files that are located within

    @param request_handler: An initialized APIRequestHandler
    @param zip_dir: the full path to the zip folder where data is stored
    @param dashboard_export: the name of the folder within the zip folder
    @param dataset_id: the id of the chosen dataset
    @return: None
    """
    export_dataset_endpoint = f'api/v1/dataset/export/?q=[{dataset_id}]'
    export_response = request_handler.get_request(export_dataset_endpoint)
    local_path = "zip/dataset.zip"
    with open(local_path, "wb") as f:
        f.write(export_response.content)

    # extract the folder out of the zip file
    with zipfile.ZipFile(local_path) as myzip:
        myzip.extractall(path='./zip')

    dataset_export = myzip.namelist()[0].split('/', 1)[0]

    _replace_subfolder(zip_dir, dataset_export, dashboard_export, 'databases')
    _replace_subfolder(zip_dir, dataset_export, dashboard_export, 'datasets')


def change_dashboard_details(dashboard_filename, dashboard_new_name):
    """
    Change the details of the dashboard file
    Specifically change the dashboard_title, uuid, and slug

    @param dashboard_filename: the name of the dashboard
    @param dashboard_new_name: the new name of the dashboard
    @return: None
    """
    params = [
        ("dashboard_title", dashboard_new_name),
        ("uuid", create_id()),
        # Setting slug to None makes a new dashboard instead of overriding an existing dashboard
        ("slug", None)
    ]
    _set_new_details(dashboard_filename, params)


def change_chart_details(charts, extracted_folder_name, dataset_name, database_name):
    """
    Change the details of all the chart files

    @param charts: A list of all charts containing [chart_id, chart_old_name]
    @param extracted_folder_name: The folder within the zip file created from export_one_dashboard()
    @param dataset_name: the name of the dataset
    @param database_name: the name of the database
    @return: None
    """
    # ============================================================
    # Uncomment out 2 lines when frontend supports renaming charts
    # ============================================================
    for chart in charts:
        chart_id = chart["chart_id"]
        chart_old_name = _cleaned_filename(chart["chart_old_name"])
        # chart_new_name = chart["chart_new_name"]

        dataset_name = _cleaned_filename(dataset_name)
        database_name = _cleaned_filename(database_name)

        dataset_filename = f'zip/{extracted_folder_name}/datasets/{database_name}/{dataset_name}.yaml'

        with open(dataset_filename, 'r') as file:
            dataset_data = yaml.safe_load(file)
        dataset_uuid = dataset_data.get("uuid")

        chart_filename = f'zip/{extracted_folder_name}/charts/{chart_old_name}_{chart_id}.yaml'
        params = [
            ("dataset_uuid", dataset_uuid),
            # Note: Creating new IDs for charts is needed to create a chart with a new dataset
            # However, deleting a dashboard on Superset does not delete its charts
            # This creates an issue where new charts being created are never being deleted
            # Do not know if this is an issue we can fix, or if it is a Superset issue.
            ("uuid", create_id())
            # ("slice_name", chart_new_name)
        ]
        _set_new_details(chart_filename, params)


def update_dashboard_uuids(charts, charts_dir, dashboard_filepath):
    """
    Update the unique ids of all charts in dashboard metadata

    @param charts: A list of all charts containing [chart_id, chart_old_name]
    @param charts_dir: The path to the directory containing all charts
    @param dashboard_filepath: The path to the dashboard yaml file
    @return: None
    """
    # Read the dashboard file
    with open(dashboard_filepath, 'r') as dashboard_file:
        dashboard_data = yaml.safe_load(dashboard_file)

        # Loop over all files in the charts directory
        for chart in charts:
            chart_id = chart['chart_id']
            chart_old_name = _cleaned_filename(chart["chart_old_name"])

            chart_filename = f'{chart_old_name}_{chart_id}.yaml'

            # Read the chart file
            chart_file_path = os.path.join(charts_dir, chart_filename)

            assert chart_file_path.endswith('.yaml')
            assert os.path.isfile(chart_file_path)
            with open(chart_file_path, 'r') as chart_file:
                chart_data = yaml.safe_load(chart_file)

            chart_uuid = chart_data.get('uuid')
            # Update UUID in the dashboard data
            _update_dashboard_uuid(chart_id, chart_uuid, dashboard_data)

            chart_file.close()

    # Write the updated dashboard data back to the dashboard file
    with open(dashboard_filepath, 'w') as dashboard_file:
        yaml.dump(dashboard_data, dashboard_file, default_flow_style=False)


def update_chart_uuids(dashboard_export_dir, dataset_name, database_name):
    """
    Update the unique id of the dataset on each of the chart.yaml files

    @param dashboard_export_dir: The full path to the exported dashboard
    @param dataset_name: The name of the dataset
    @param database_name: The name of the database
    @return: None
    """
    dataset_name = _cleaned_filename(dataset_name)
    database_name = _cleaned_filename(database_name)
    dataset_filepath = f'{dashboard_export_dir}datasets/{database_name}/{dataset_name}.yaml'

    with open(dataset_filepath, 'r') as dataset_file:
        dataset_data = yaml.safe_load(dataset_file)
        dataset_uuid = dataset_data.get('uuid')

    charts_filepath = f'{dashboard_export_dir}charts/'
    for root, _, files in os.walk(charts_filepath):
        for filename in files:
            chart_filepath = os.path.join(root, filename)
            _update_chart_uuid(chart_filepath, dataset_uuid)


def update_dataset_uuids(dashboard_export_dir, dataset_name, database_name):
    """
    Update the database_uuid in the dataset.yaml file

    @param dashboard_export_dir: The full path to the exported dashboard
    @param dataset_name: The name of the dataset
    @param database_name: The name of the database
    @return: None
    """
    database_name = _cleaned_filename(database_name)
    database_filepath = f'{dashboard_export_dir}databases/{database_name}.yaml'

    with open(database_filepath, 'r') as database_file:
        database_data = yaml.safe_load(database_file)
        database_uuid = database_data.get('uuid')

    dataset_name = _cleaned_filename(dataset_name)
    dataset_filepath = f'{dashboard_export_dir}datasets/{database_name}/{dataset_name}.yaml'

    with open(dataset_filepath, 'r') as dataset_file:
        dataset_data = yaml.safe_load(dataset_file)
        dataset_data['database_uuid'] = database_uuid


def import_new_dashboard(request_handler, filename):
    """
    Import the new dashboard to SUPERSET_INSTANCE_URL

    @param request_handler: An initialized APIRequestHandler
    @param filename: The filename of the zip file containing the dashboard info
    @return: None
    """
    with zipfile.ZipFile(f'zip/{filename}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        _zipdir(f'zip/{filename}', zipf)

    files = [('formData', (f'zip/{filename}.zip', open(f'zip/{filename}.zip', 'rb'), 'application/zip'))]

    request_handler.post_request(IMPORT_ENDPOINT, files=files)

    return "Imported"


def delete_zip(path):
    """
    Delete all files (except .dummy) within the zip folder used to store temporary files

    @param path: The full path to the zip folder
    @return: None
    """
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


def _replace_subfolder(filepath, source, destination, subfolder_name):
    """
    Replace the subfolder in destination with the one in source looking at the filepath

    @param filepath: path to the subfolder
    @param source: (Usage - new dataset folder)
    @param destination: (Usage - old dashboard folder)
    @param subfolder_name: (Usage - dataset/dashboard folders)
    """
    source_subfolder = os.path.join(source, subfolder_name)
    destination_subfolder = os.path.join(destination, subfolder_name)

    # Remove the existing destination subfolder
    if os.path.exists(f'{filepath}/{destination_subfolder}'):
        shutil.rmtree(f'{filepath}/{destination_subfolder}')

    shutil.copytree(f'{filepath}/{source_subfolder}', f'{filepath}/{destination_subfolder}')


def _set_new_details(filename, details):
    """
    Set new details for parameters that are not nested

    @param filename: The filename of the new dashboard
    @param details: A list containing new_dashboard_name and dashboard_uuid in the format [(key, value)]
    @return: None
    """
    with open(filename, 'r') as file:
        file_data = yaml.safe_load(file)
        for key, value in details:
            file_data[key] = value
    with open(filename, 'w') as file:
        yaml.dump(file_data, file, sort_keys=False)


def _cleaned_filename(input_string):
    """
    Return the input_string as Superset would name it

    @param input_string: the string to filter
    @return: the input string, without non-filename characters, replaced spaces with underscores, and remove leading _
    """
    only_file_char =  re.sub(r'[^a-zA-Z0-9\s\-_]', '', input_string)
    no_spaces = only_file_char.replace(" ", "_").lstrip('_')
    return no_spaces


def _update_dashboard_uuid(chart_id, chart_uuid, dashboard_data):
    """
    Update the chart uuid within dashboard_data

    @param chart_id: the id of the chart
    @param chart_uuid: the new uuid
    @param dashboard_data: the data within the dashboard.yaml file
    @return: None
    """
    for _, chart_info in dashboard_data.get('position', {}).items():
        if 'type' in chart_info:
            if chart_info.get('type') == 'CHART':
                meta = chart_info.get('meta', {})
                # Check if slice name matches
                if meta.get('chartId') == chart_id:
                    # Update the UUID
                    meta['uuid'] = chart_uuid
                    break


def _update_chart_uuid(chart_filepath, new_dataset_uuid):
    """
    Update the dataset uuid within chart

    @param chart_filepath: the filepath to the chart file
    @param new_dataset_uuid: the new dataset uuid
    @return: None
    """
    with open(chart_filepath, 'r') as chart_file:
        chart_data = yaml.safe_load(chart_file)

        chart_data['dataset_uuid'] = new_dataset_uuid

    with open(chart_filepath, 'w') as chart_file:
        yaml.dump(chart_data, chart_file, default_flow_style=False)


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
