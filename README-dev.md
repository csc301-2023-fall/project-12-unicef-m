### Instructions to Work on this Project

This file will contain clear, concise, and complete instructions of 
everything that needs to be known about extending our work.

Here is all the functionality of our project as user stories.

### User Stories

1) As a Superset user, I want to be able to login to my account and view all
and select the template dashboards I have available on my Superset instance.
2) As a user, I want to be able to create a copy of any existing dashboard and
automatically have the output imported onto my instance of Superset.
3) As an economist, I want to be able to quickly create a new dashboard
every year, with new yearly data on world GDP, with the same format. In
other words, I want to be able to clone using alternative dataset with the template dashboard
to create a new visualization with the same format.
4) As a UNICEF employee, we have many employees and naturally each employee
may have their own version of Superset running on their desktop.
I want to be able to send the cloned dashboard to my employee's
instance of Superset so that they could access the visualization from
their account.
6) As a user, I want to be able to know when changes were made onto dashboard
and propagate these changes onto any dashboards cloned from the template.

### Key Technical Components & Modules

#### .github/workflows/github-actions.yml

A github-actions.yml exists to for automatic deployment when changes are pushed to main.

#### backend/

routes/views.py

- This file contains all the backend endpoints that are called from the 
frontend. These endpoints provide all the functionality that exists.

utils/api_request_handler.py

- This file contains an APIRequestHandler object that is used to make
all requests to Superset's API

/utils/api_helpers.py

- This file contains all the functions that make a call to Superset's API

/utils/dashboard_details.py & /utils/dashboard_details_helper.py

- These files contains all the information needed to make a clone as
well as all the code to clean the data from the frontend, should the input format be changed

/utils/data_helpers.py

- These files contain all the functions that edit the yaml files obtained
from exporting the template dashboard

The important functionality works in these main files. More detailed instructions
can be found in the documentation within these files.

#### frontend/

/src/pages/login_page.jsx

- This file contains code to get Superset URL, username, and password from user. Then navigate to dashboards page if credentials valid.

/src/pages/dashboards.jsx
- This file contains axio calls to retrieve the dashboards and display them. This file also contains code that enables search.

/src/pages/final_clone.jsx
- This file contains code that use axios fetch information such as lists of charts the users can rename from the desired dataset, and maps the dataset to this dashboard. Here we also give users the option of cross instance cloning.

/src/pages/pages.css

- This page contains all the styling code for the page components.

/src/main.jsx

- This file specifies the path to access each page.

### Initial Setup

Prior to working on the backend, make sure that you create a virtual environment in the backend folder. To do so, first navigate to the backend directory, and then type the following command:
```
python -m venv venv
py -m venv venv (If the first does not work)
```
Once the venv folder has been created, activate the environment:
```
(MacOS) source venv/bin/activate
(Windows) .\venv\Scripts\activate
(if errors occur try switching from \ to / and vice-versa)
```
If the folder contains a requirements.txt, install all required (Python) libraries using the requirements.txt after you've created the venv. 
```
pip install -r requirements.txt
```
Before pushing, ensure that if you've downloaded new libraries, you create a new requirements.txt by running the command:
```
pip freeze > requirements.txt
```

Everything should now be set up to begin development

### Deployment 

RUDY WRITE WHATEVER NEEDS TO GO HERE

### Next Steps

The current completed project is ready for general use.
However, there are a few changes that must be made first.

To view an exported dashboard, you could comment out the delete_zip function
located in backend/routes/views.py - clone(). The exported dashboard will
be viewable within the backend/zip folder. This may be useful when making 
edits to the exported data (e.g. Implementing Renaming Charts)

#### Login Credentials

Currently, the login variables are hard-coded in an .env file 
located within the backend folder. (An file called .env.example) specifies
how to state variables such as SUPERSET INSTANCE URL, SUPERSET USERNAME, 
and SUPERSET PASSWORD. However, changes must be made in the frontend
and backend to accept credentials and use these credentials to make the
initial batch of Superset API calls to export a dashboard.


Changes will need to be made in the following files:

- backend/routes/views.py
- frontend/src/pages/login_page.jsx

Note: The product is remains functional locally with hard-coded
credentials with an .env file in the backend folder.

#### Renaming Charts

Currently, the frontend supports renaming charts, but the changes
have not been made to the backend files. Supporting this feature will
include making changes the "slice name" attribute located in each 
individual chart file, as well as, the dashboard file. The individual chart
files already have code to do this but commented out, however, code
must be created to change the "slice name" within the dashboard file

Changes will need to be made in the following files

- backend/utils/data_helpers.py

#### Across Instance Cloning

Do note that across instance cloning does not support local instances of
superset if ran through render. As the online version of this program
does not have superset on it's local host. Changes may need to be made
to accomodate this fact.