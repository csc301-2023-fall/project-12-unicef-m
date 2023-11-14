from flask import Flask, redirect, request, jsonify, session, url_for
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv
import requests

# Load environment variables

# load_dotenv()

# from .firebase_config import initialize_firebase

app = Flask(__name__)
CORS(app)
# initialize_firebase()

# from .routes.vc import vc
from backend.routes.views import views

# app.register_blueprint(vc, url_prefix='/vc')
app.register_blueprint(views, url_prefix='/view')

# GitHub Authorizaiton, setting up with OAuth 2.0

"""
Overall flow and information for front-end will 
be explained in Discord 
"""
# This information needs to set up through the organizations GitHub in GitHub itself:

# CLIENT_ID = environ.get()
# CLIENT_SECRET = environ.get()
# SECRET_KEY = environ.get()

# GitHub OAuth endpoints:

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API = "https://api.github.com/user"

@app.route("/login/github", methods=['GET'])
def login():
    
    # We redirect to GitHub for authorization
    scope = "user:email"
    return redirect(f"{GITHUB_AUTH_URL}?client_id={CLIENT_ID}&scope={scope}")


@app.route("/login/github/callback", methods=['GET'])
def callback():
    code = requests.args.get('code')
    
    if code is None:
        return jsonify({'Error': 'Authorization code not found'})

    token_response = requests.post(
        GITHUB_TOKEN_URL,
        headers={'Accept': 'application/json'},
        data={'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'code': code}
    )
    
    if token_response.status_code != 200:
        return jsonify({'Error': 'Invalid response from GitHub token exchange'}), 400
    
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    
    if access_token is None:
        return jsonify({'Error': 'Access token not found'}), 400
    
    # Fetch the user's information
    
    user_response = requests.get(
        GITHUB_USER_API,
        headers={'Authorization': f'token {access_token}'}
    )
    
    if user_response.status_code != 200:
        return jsonify({'Error': 'Failed to fetch user information from GitHub'}), 400
    
    user_json = user_response.json()
    
    # TODO potentially add user to database
    # The code for this would go here, or we can add them to the current session:
    session['github_user'] = user_json # test this out
    
    # Redirect to the frontend from here
    frontend_url = None # environ.get()
    return redirect(frontend_url)
    
    
@app.route("/logout", methods=['GET'])
def logout():
    session.pop('github_user', None)
    return jsonify({'Message': "Logged Out"}), 200
    # or use session.clear()


# Added a sample dashboard to Firebase:

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
