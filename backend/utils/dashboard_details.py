"""
A class for DashboardDetails which will store any information related to cloning from the frontend POST request
"""

class DashboardDetails:
    def __init__(self, dashboard_id, dashboard_old_name, dashboard_new_name,
                 dataset_id, dataset_name, database_name, charts, credentials):
        """
        An DashboardDetails object that defined the information needed to create a clone

        @param dashboard_id: the ID superset assigned to the template dashboard
        @param dashboard_old_name: the name of the template dashboard
        @param dashboard_new_name: the name the user wants the dashboard to have
        @param dataset_id: the ID superset assigned to the chosen dataset
        @param dataset_name: the name of the dataset
        @param database_name: the name of the database the dataset comes from
        @param charts: a list of list where each sublist contains the [chart_id, chart_old_name]
        @param credentials: a dictionary of Superset Instance URL, Superset Username, Superset Password
        """
        self.dashboard_id = dashboard_id
        self.dashboard_old_name = dashboard_old_name
        self.dashboard_new_name = dashboard_new_name
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.database_name = database_name
        self.charts = charts
        self.credentials = credentials
