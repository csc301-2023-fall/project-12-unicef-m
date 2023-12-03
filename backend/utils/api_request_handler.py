import requests
from backend.utils.endpoints import *


class APIRequestHandler:
    def __init__(self, superset_instance_url, superset_username, superset_password):
        self.session = requests.Session()
        self.superset_instance_url = superset_instance_url
        self.superset_username = superset_username
        self.superset_password = superset_password
        self.headers_auth = self._get_headers()

    def _get_headers(self):
        if self.superset_instance_url is None:
            raise SystemExit("Superset Instance URL must be defined")

        if self.superset_username is None:
            raise SystemExit("Superset username must be defined")

        if self.superset_password is None:
            raise SystemExit("Superset password must be defined")

        access_token = self._get_access_token()

        headers = {"Authorization": "Bearer " + access_token}
        csrf_token = self._get_csrf_token(headers)

        headers['X-CSRFToken'] = csrf_token
        headers['accept'] = 'application/json'
        headers['Referer'] = self.superset_instance_url

        return headers

    def _get_access_token(self):
        login_data = {
            "username": self.superset_username,
            "password": self.superset_password,
            "provider": "db"
        }

        login_response = self.session.post(self.superset_instance_url + ACCESS_TOKEN_ENDPOINT, json=login_data)
        access_token = login_response.json().get("access_token")
        if not access_token:
            raise SystemExit("Could not retrieve access_token. Please check your superset username and password")

        return access_token

    def _get_csrf_token(self, headers):
        csrf_response = self.session.get(self.superset_instance_url + CSRF_TOKEN_ENDPOINT, headers=headers)
        csrf_token = csrf_response.json().get("result")
        if not csrf_token:
            raise SystemExit("Could not retrieve csrf_token. Please check your superset username and password")

        return csrf_token

    def _execute_http_method(self, http_method, endpoint, **kwargs):
        response = None
        try:
            response = http_method(self.superset_instance_url + endpoint, headers=self.headers_auth, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            raise SystemExit(f"\nHTTP Error: '{err}'\n" + f"Response: {response.text}")

    def post_request(self, endpoint, **kwargs):
        return self._execute_http_method(self.session.post, endpoint, **kwargs)

    def get_request(self, endpoint, **kwargs):
        return self._execute_http_method(self.session.get, endpoint, **kwargs)

    def put_request(self, endpoint, **kwargs):
        return self._execute_http_method(self.session.put, endpoint, **kwargs)
