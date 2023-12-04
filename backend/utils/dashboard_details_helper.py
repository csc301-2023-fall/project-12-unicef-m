"""
This file takes a json request and creates a DashboardDetail object
"""
from backend.utils.dashboard_details import DashboardDetails


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
