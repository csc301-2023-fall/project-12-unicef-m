'''
To run this test file, run the command: pytest testing_suite.py
'''
import unittest

from backend.routes.dashboard_handler import DashboardHandler
from backend.routes.changes_handler import ChangesHandler
from backend.routes.views2 import *
from backend.utils.api_helpers2 import *
from backend.utils.superset_constants import SUPERSET_PASSWORD, SUPERSET_USERNAME, SUPERSET_INSTANCE_URL
import requests
from flask import app as flask_app
import pytest

# Initialize instances of the handlers
# dashboard_handler = DashboardHandler()
# changes_handler = ChangesHandler()

# Initialize the test client using the pytest fixture
@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def setup():
    # d5 = dashboard_handler.add_dashboard("test_5", "test_5_superset", "template_5", changes_handler)
    # d6 = dashboard_handler.add_dashboard("test_6", "test_6_superset", "template_6", changes_handler)
    # d7 = dashboard_handler.add_dashboard("test_7", "test_7_superset", "template_7", changes_handler)
    # d8 = dashboard_handler.add_dashboard("test_8", "test_8_superset", "template_8", changes_handler)
    pass

def teardown():
    # dashboard_handler.delete_dashboard('test_5') 
    # dashboard_handler.delete_dashboard('test_6')
    # dashboard_handler.delete_dashboard('test_7')
    # dashboard_handler.delete_dashboard('test_8')
    pass


# Basic testing suite for each CRUD operation


class TestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.access_token = get_access_token()

    # Version Control Tests
    def test_add_dashboard(self, client):
        pass

    def test_propagate_changes(self, client):
        pass

    # def test_get_dashboard(self, client):
    #     '''
    #     Testing to see if we can access thd ashboard test_4 froom our database successfully
    #     '''
    #
    #     response = client.get("deliverable-2-12-3-mistr156-mongarud.vercel.app/api/get-dashboard/41012f4e-7b94-4945-a039-02b65c7af1f9")
    #
    #     curr_db = dashboard_handler.get_dashboard("41012f4e-7b94-4945-a039-02b65c7af1f9")
    #
    #     assert curr_db['dashboard_name'] == "test_4"

    def test_delete_dashboard(self, client):
        pass

    # Superset API Call Tests
    def test_valid_get_access_token(self):
        login_data = {
            "username": SUPERSET_USERNAME,
            "password": SUPERSET_PASSWORD,
            "provider": "db"
        }

        response = requests.post(SUPERSET_INSTANCE_URL + ACCESS_TOKEN_ENDPOINT, json=login_data)

        assert response.status_code == 200
        assert 'access_token' in response.json()

    def test_valid_get_csrf_token(self):
        access_token = self.access_token
        headers = {"Authorization": "Bearer " + access_token}

        response = requests.get(SUPERSET_INSTANCE_URL + CSRF_TOKEN_ENDPOINT, headers=headers)

        assert response.status_code == 200
        assert 'result' in response.json()

    def test_valid_response_get_dashboards(self):
        access_token = self.access_token
        headers = {"Authorization": "Bearer " + access_token}

        response = requests.get(SUPERSET_INSTANCE_URL + DASHBOARD_ENDPOINT, headers=headers)

        assert response.status_code == 200
        assert 'result' in response.json()
        if response.json()['result']:
            assert 'id' in response.json()['result'][0]
            assert 'dashboard_title' in response.json()['result'][0]

    def test_valid_get_charts(self):
        access_token = self.access_token
        headers = {"Authorization": "Bearer " + access_token}
        dashboard = get_dashboards(access_token)[0]

        chart_endpoint = f'{SUPERSET_INSTANCE_URL}{DASHBOARD_ENDPOINT}{str(dashboard[0])}/charts'

        response = requests.get(chart_endpoint, headers=headers)

        assert response.status_code == 200
        assert 'result' in response.json()
        if response.json()['result']:
            assert 'id' in response.json()['result'][0]
            assert 'slice_name' in response.json()['result'][0]

    def test_valid_get_datasets(self):
        access_token = self.access_token
        headers = {"Authorization": "Bearer " + access_token}

        response = requests.get(SUPERSET_INSTANCE_URL + DATASET_ENDPOINT, headers=headers)

        assert response.status_code == 200
        assert 'result' in response.json()
        if response.json()['result']:
            assert 'table_name' in response.json()['result'][0]
            assert 'database' in response.json()['result'][0]
            assert 'database_name' in response.json()['result'][0]['database']

    # Backend API Call Tests
    def test_valid_get_all_dashboards(self):
        pass

    def test_valid_get_all_datasets(self):
        pass


if __name__ == "__main__":
    pytest.main()
