from flask import Flask
from .firebase_config import initialize_firebase

app = Flask(__name__)
initialize_firebase()

from .routes.vc import vc
from .routes.views import views

app.register_blueprint(vc, url_prefix='/vc')
app.register_blueprint(views, url_prefix='/view')

# GitHub Authorizaiton, set up auth 0





# Added a sample dashboard to firebase:


# def create_sample_dashboard():
#     d1 = dashboard_handler.add_dashboard("test_1", "test_1_superset", "template_1", changes_handler)
#     d2 = dashboard_handler.add_dashboard("test_2", "test_2_superset", "template_2", changes_handler)
#     d3 = dashboard_handler.add_dashboard("test_3", "test_3_superset", "template_3", changes_handler)
#     d4 = dashboard_handler.add_dashboard("test_4", "test_4_superset", "template_4", changes_handler)

#     dashboard_handler._make_clone_forcefully(d1, d2)
#     dashboard_handler._make_clone_forcefully(d1, d3)
#     dashboard_handler._make_clone_forcefully(d2, d4)

#     dashboard_handler.update_dashboard(d1, changes_handler, template="template_1_v2")
#     dashboard_handler.propogate_changes(d1, changes_handler)
    

# def delete_all_in_database():
#     dashboard_handler._delete_all_dashboards()
#     changes_handler._delete_all_changes()


# if __name__ == "__main__":
#     delete_all_in_database()
#     create_sample_dashboard()