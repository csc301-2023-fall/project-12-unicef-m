from flask import Blueprint, request
import json

from backend.utils.api_helpers import *
from backend.utils.api_request_handler import APIRequestHandler
from backend.utils.superset_constants import SUPERSET_PASSWORD, SUPERSET_USERNAME, SUPERSET_INSTANCE_URL
from backend.utils.utils import create_id
from backend.utils.dashboard_details import DashboardDetails

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
    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)
    dashboards = get_dashboards(request_handler)

    dashboard_list = []
    for dashboard in dashboards:
        dashboard_id = dashboard[0]
        dashboard_name = dashboard[1]

        charts = get_charts(request_handler, dashboard_id)

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
                "dataset_id": dataset_id,
            },
            {
                <More datasets>
            }
        ]
    """
    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)
    datasets = get_datasets(request_handler)
    dataset_list = []

    for dataset in datasets:
        dataset_name = dataset[0]
        db_name = dataset[1]
        dataset_id = dataset[2]

        curr_dataset_info = {
            "dataset_name": dataset_name,
            "database_name": db_name,
            "dataset_id": dataset_id,
        }

        dataset_list.append(curr_dataset_info)

    return json.dumps(dataset_list)


@views.route('/clone', methods=['POST'])
def clone():
    """
    Expected Return Format
       {
           "dashboard_id":
           "dashboard_old_name":
           "dashboard_new_name":
           "dataset_id":
           "charts": [
                        {
                        chart_id
                        chart_old_name
                        chart_new_name
                        "chart_new_dataset": "covid_vaccines",
                        "database": "examples"
                        }
                   ]
       }
    """
    dashboard_details = get_details(request)
    dashboard_export_name, zip_directory, request_handler = modify_details(dashboard_details)

    import_new_dashboard(request_handler, dashboard_export_name)
    breakpoint()
    delete_zip(f"{zip_directory}/")

    return "Cloning Successful"


@views.route('/across-instance-clone', methods=['POST'])
def across_instances():
    dashboard_details = get_details(request)
    dashboard_export_name, zip_directory, _ = modify_details(dashboard_details)

    second_superset_instance_url = request.json.get("second_instance_url")
    second_superset_username = request.json.get("second_instance_username")
    second_superset_password = request.json.get("second_instance_password")

    new_request_handler = APIRequestHandler(second_superset_instance_url, second_superset_username,
                                            second_superset_password)

    import_new_dashboard(new_request_handler, dashboard_export_name)

    delete_zip(f"{zip_directory}/")

    return "Across instance Cloning Successful"


def get_details(request):
    """
    Takes in a HTTP Request Object and modifies the dashboards files to update it with new datasets

    @param request: the HTTP request (POST request)
    @return: Returns a DashboardDetails object with all fields initialized
    """
    dashboard_id = request.json.get("dashboard_id")
    old_name = request.json.get("dashboard_old_name")
    new_name = request.json.get("dashboard_new_name")
    dataset_id = request.json.get("dataset_id")

    charts_temp = request.json.get("charts")

    # =======================================================================================
    # Due to the current way our frontend was set up, each chart is associated with a dataset
    # However, as only one dataset need to be specified, this chunk of code will change.
    # Must make necessary changes to the frontend prior to changing this code.
    # =======================================================================================
    if charts_temp[0] is not None:
        dataset_name = charts_temp[0].get("chart_new_dataset")
        database_name = charts_temp[0].get("database")
    else:
        dataset_name = None
        database_name = None

    charts = []
    for chart in charts_temp:
        chart_detail = {
            "chart_id": chart.get("chart_id"),
            "chart_old_name": chart.get("chart_old_name"),
            "chart_new_name": chart.get("chart_new_name")
        }
        charts.append(chart_detail)
    # =======================================================================================

    return DashboardDetails(dashboard_id=dashboard_id, dashboard_old_name=old_name, dashboard_new_name=new_name,
                            dataset_id=dataset_id, dataset_name=dataset_name, database_name=database_name,
                            charts=charts)


def modify_details(data_object):
    """
    Takes in a HTTP Request Object and modifies the dashboards files to update it with new datasets

    @param data_object: a DashboardDetails object with all relevant fields initialized
    @return: Returns a list with the folder name with the dashboards information (within the zip folder),
             and the file path of the zip folder, and the request handler
    """
    # Retrieve all info
    dashboard_id = data_object.dashboard_id
    dashboard_old_name = data_object.dashboard_old_name
    dashboard_new_name = data_object.dashboard_new_name
    dataset_id = data_object.dataset_id
    dataset_name = data_object.dataset_name
    database_name = data_object.database_name
    charts = data_object.charts

    # Initialized all paths directly to avoid issues with relativity
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.join(FILE_DIR, os.pardir)
    GRANDPARENT_DIR = os.path.abspath(os.path.join(PARENT_DIR, os.pardir))
    ZIP_DIR = os.path.join(GRANDPARENT_DIR, 'backend/zip')

    # Initialize a request handler which will be used to make any and all requests to Superset API
    request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)

    # Get the files relating to the template dashboard
    dashboard_export_name = export_one_dashboard(request_handler, dashboard_id)
    dashboard_filename = get_dashboard_filename(dashboard_id, dashboard_old_name,
                                                ZIP_DIR, dashboard_export_name)

    # Swap out the old dataset and database with the chosen ones
    modify_dataset_and_database(request_handler, ZIP_DIR, dashboard_export_name, dataset_id)

    # At this point, we have a folder zip/dashboard_export_name
    # We must change all the details within the files that the user specified to change
    # 1) Change names that are referenced in each file
    change_dashboard_details(dashboard_filename, dashboard_new_name)
    change_chart_details(charts, dashboard_export_name, dataset_name, database_name)

    # 2) Change uuids that are referenced in each file
    update_dashboard_uuids(charts, f'{ZIP_DIR}/{dashboard_export_name}/charts/', dashboard_filename)
    update_chart_uuids(f'{ZIP_DIR}/{dashboard_export_name}/', dataset_name, database_name)
    update_dataset_uuids(f'{ZIP_DIR}/{dashboard_export_name}/', dataset_name, database_name)

    return dashboard_export_name, ZIP_DIR, request_handler
