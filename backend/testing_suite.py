'''
To run this test file, run the command: pytest testing_suite.py
'''

from backend.utils.superset_constants import *
from backend.utils.api_helpers import *
from backend.utils.api_request_handler import APIRequestHandler
from backend.app import app as flask_app
import pytest
import unittest

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
        cls.request_handler = APIRequestHandler(SUPERSET_INSTANCE_URL, SUPERSET_USERNAME, SUPERSET_PASSWORD)

    # def test_add_dashboard(self, client):
    #     pass
    #
    # def test_propagate_changes(self, client):
    #     pass

    # def test_get_dashboard(self, client):
    #     '''
    #     Testing to see if we can access th dashboard test_4 from our database successfully
    #     '''
    #
    #     response = client.get("deliverable-2-12-3-mistr156-mongarud.vercel.app/api/get-dashboard/41012f4e-7b94-4945-a039-02b65c7af1f9")
    #
    #     curr_db = dashboard_handler.get_dashboard("41012f4e-7b94-4945-a039-02b65c7af1f9")
    #
    #     assert curr_db['dashboard_name'] == "test_4"

    # def test_delete_dashboard(self, client):
    #     pass

    # Superset API Call Tests
    def test_valid_get_access_token(self):
        login_data = {
            "username": SUPERSET_USERNAME,
            "password": SUPERSET_PASSWORD,
            "provider": "db"
        }

        response = self.request_handler.post_request(ACCESS_TOKEN_ENDPOINT, json=login_data)
        assert response.status_code == 200
        assert 'access_token' in response.json()

    def test_valid_get_csrf_token(self):
        response = self.request_handler.get_request(CSRF_TOKEN_ENDPOINT)

        assert response.status_code == 200
        assert 'result' in response.json()

    def test_valid_response_get_dashboards(self):
        response = self.request_handler.get_request(DASHBOARD_ENDPOINT)

        assert response.status_code == 200
        assert 'result' in response.json()
        if response.json()['result']:
            assert 'id' in response.json()['result'][0]
            assert 'dashboard_title' in response.json()['result'][0]

    def test_valid_get_charts(self):
        dashboard = get_dashboards(self.request_handler)[0]

        chart_endpoint = f'{DASHBOARD_ENDPOINT}{str(dashboard[0])}/charts'
        response = self.request_handler.get_request(chart_endpoint)

        assert response.status_code == 200
        assert 'result' in response.json()
        if response.json()['result']:
            assert 'id' in response.json()['result'][0]
            assert 'slice_name' in response.json()['result'][0]

    def test_valid_get_datasets(self):
        response = self.request_handler.get_request(DATASET_ENDPOINT)

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