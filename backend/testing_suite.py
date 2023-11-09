'''
To run this test file, run the command: pytest testing_suite.py
'''

from dashboard_handler import DashboardHandler
from changes_handler import ChangesHandler
from app import app as flask_app
import pytest

# Initialize instances of the handlers

dashboard_handler = DashboardHandler()
changes_handler = ChangesHandler()

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


class TestSuite:

    def test_add_dashboard(self, client):
        pass
        

    def test_propogate_changes(self, client):
        pass


    def test_get_dashboard(self, client):
        '''
        Testing to see if we can access thd ashboard test_4 froom our database successfully       
        '''
        
        response = client.get("deliverable-2-12-3-mistr156-mongarud.vercel.app/api/get-dashboard/41012f4e-7b94-4945-a039-02b65c7af1f9")

        curr_db = dashboard_handler.get_dashboard("41012f4e-7b94-4945-a039-02b65c7af1f9")

        assert curr_db['dashboard_name'] == "test_4"


    def test_delete_dashboard(self, client):
        pass


if __name__ == "__main__":
    pytest.main()