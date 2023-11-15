## NOTE TO TA FOR D3:

We have created a video for our D3 submission also linked in the iteration-03-review.md file.

#### Video Link in Docs: https://docs.google.com/document/d/1bYASU4AnV9Rw8COij2wMZFm57ggSoFY9WIWmg3Y8Ekw/edit

Group Number: 12  
Team Name: Red Pandas  

## Partner Intro:
Our primary point of contact for this project is Evan Wheeler (ewheeler@unicef.org). 

UNICEF is a multinational organization dedicated to protecting, assisting, and creating environments for children to grow up with the resources they need. They make data-driven decisions and support humanitarian efforts worldwide. 

## Project Description
We will be building a web interface for the existing command line proof of concept that clones Apache Superset dashboards. Users will have the ability to modify and clone existing dashboards. Additionally, new features, such as a version control that would allow for the propagation of changes from the configuration to the parent dashboard to the cloned children. The current problem is difficulty surrounding the use of the cloning tool and redundant testing for staging and production environments, and so with these additions, UNICEF employees, and other Superset users, will have the tools to quickly and easily visualize whatever data they want. This application will unlock the opportunity for larger teams to work together on dashboards across the globe, rather than individual users having their own instances on their accounts.
   
## Key Features
Our primary feature is a web interface that would allow users to clone a dashboard template and populate it with any compatible datasource. Additional features include a version control system that would allow a user to make changes to a dashboard's configuration and update the cloned dashboards. In addition to being able to clone dashboards within the same instance we plan to implement cloning across superset instances.

Feature Breakdown
* Login Interface and Authentication

The user will be required to specify a URL to their instance of superset, as well as their username and password for authentication.

* View all existing dashboards, charts, and datasets in their instance of Superset

The user will be able to view all the dashboards they have available to clone from in their instance of superset. Upon selecting a dashboard, the user will be able to view all charts and datasets they have available to populate.

* Cloning a Dashboard

The user will be able to choose an existing dashboard as the starting template. Once this dashboard is chosen, the user will be required to select a dataset for each of the existing charts that are part of the template dashboard. The user will be given the option to rename the cloned dashboard and any of the available charts.

* Version control to update all cloned dashboards when prompted to the original dashboard

Upon cloning a dashboard, all changes will be tracked in the database. This will allow users to push those changes onto dashboards that were previously cloned from the original modified dashboard.

## Instructions
### Instructions To Run the App

Follow the link provided below:

https://project12-csc301.onrender.com/

Login to the program using the following credentials:
Superset Instance URL: https://superset-dev.unicef.io/ (User’s Local Instance, we are using the cloud one for test)
Superset Username: admin
Superset Password: UNICEFToronto2023##

On the main screen, the user will be able to select any dashboard to clone. Clicking on one of these dashboards, will take the user to the cloning page.

Here they will have the option to rename their dashboard, view the names of all charts, and select the dataset for each of the charts. Then the user will click on the clone button.

The cloned dashboard will be ready and viewable on superset. The user will then be sent back to the main screen.

### Instructions to Work on the Project

Prior to working on the backend, make sure that you create a virtual environment in the backend folder. To do so, first navigate to the backend directory, and then type the following command:
```
python -m venv venv
(If this does not work try: py -m venv venv)
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
The instructions above are for MacOS/Linux; for Windows, read this article on how to do this: [Python Virtual Environments: A Primer – Real Python](https://realpython.com/python-virtual-environments-a-primer/)

## Development Requirements
We will be using a cloud-based database, Firebase, so no setup is required for the database itself. 

When we have environment variables for our flask backend we will tentatively update the development requirements

## Github Workflow
* We will use GitHub Projects with kanban boards to manage our upcoming tasks
* Issues will be assigned to team members to work on
* All new code will be done on a new separate branch
* Pull requests will be created after significant progress is made to an individual section
* Pull requests will be reviewed by at least one other group member before being merged into develop
* When develop is in a stable state, a pull request will be created to merge develop into main
* Prior to merging into develop/main, our automated Github Actions workflow lets us know if the current branch we’re planning on merging passes all the tests or not, allowing us to make informed decisions

## Deployment Tools
Firstly, we have a Github Actions workflow setup that runs tests for our frontend and backend and lets us know immediately if our latest push/merge to our main or develop branch has issues that need to be addressed ASAP. Secondly, we have automated development set up for Render. Everytime we push changes to our main branch, Render will automatically pull the latest changes and build and deploy it. This automated deployment will ensure that the latest release of ours is available for our partners to use.

## Coding Standards and Guidelines
We aim to keep all new features modular and independent of one another. As we are working with Python, we will stick with snake-case naming conventions, and adhere to all other style conventions with respect to coding in Python. We will keep the code well documented, which includes docstring, comments, intuitive programming, and simple to understand for future developers to expand on our work.

## Licences 
We will be using an MIT licence. UNICEF values contributing to the open source community. Our partner believes that this project will not only be useful for UNICEF, but will also be desired by other companies. Therefore, we have received permission to upload the code on GitHub and share it freely.
