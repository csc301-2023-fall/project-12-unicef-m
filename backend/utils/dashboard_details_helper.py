"""
This file takes a json request and creates a DashboardDetail object
"""

from backend.utils.dashboard_details import DashboardDetails
from backend.utils.superset_constants import SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD


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
    dataset_name = request.json.get("dataset_name")
    database_name = request.json.get("database_name")
    charts = request.json.get("charts")

    credentials = {
        "instance_url": SUPERSET_INSTANCE_URL,
        "username": SUPERSET_USERNAME,
        "password": SUPERSET_PASSWORD
    }
    # If this field exists, assume that all 3 fields exist.
    # These new credentials will be used for importing the dashboard (Across Instance Cloning)
    if request.json.get("superset_url") is not None:
        credentials = {
            "instance_url": request.json.get("superset_url"),
            "username": request.json.get("superset_username"),
            "password": request.json.get("superset_password")
        }

    return DashboardDetails(dashboard_id=dashboard_id, dashboard_old_name=old_name, dashboard_new_name=new_name,
                            dataset_id=dataset_id, dataset_name=dataset_name, database_name=database_name,
                            charts=charts, credentials=credentials)
