Group Number: 12  
Team Name: Red Pandas  

## Partner Intro:
Our primary point of contact for this project is Evan Wheeler (ewheeler@unicef.org). 

UNICEF is a multinational organization dedicated to protecting, assisting, and creating environments for children to grow up with the resources they need. They make data-driven decisions and support humanitarian efforts worldwide. 

## Project Description
We will be building a web interface for the existing command line proof of concept that clones Apache Superset dashboards. Users will have the ability to modify and clone existing dashboards. Additionally, new features, such as a version control that would allow for the propagation of changes from the configuration to the parent dashboard to the cloned children and cloning dashboards across Superset instances. The current problem is difficulty surrounding the use of the cloning tool and redundant testing for staging and production environments, and so with these additions, UNICEF employees will have the tools to quickly and easily visualize any datasource they want. This application will allow larger teams to work together on dashboards across the globe, rather than individual users having their own instances on their accounts.
   
## Key Features
Our primary feature is a web interface that would allow users to clone a dashboard template and populate it with any compatible datasource. Additional features include a version control system that would allow a user to make changes to a dashboard's configuration and update the cloned dashboards. In addition to being able to clone dashboards within the same instance we plan to implement cloning across superset instances.

Feature Breakdown
* Login System (Interface)
* Cloning a dashboard (Interface)
* Setting a new viable datasource for a dashboard (Interface)
* Cloning dashboards across superset instances
* Version control to update all cloned dashboards when prompted to the original dashboard

## Instructions
Users will need to clone this Github repository since this application is not hosted online. 

Login System (Interface):
Users are pre-created since this is an internal tool since the tool uses a person's Superset account. This is where users will start. 

Cloning a dashboard (Interface):
Information will be included later.

Setting a new viable datasource for a dashboard (Interface):
Information will be included later.

Cloning dashboards across superset instances:
Information will be included later.

Version control to update all cloned dashboards when prompted to the original dashboard:
Information will be included later.

## Development Requirements
We will be using a cloud-based database, Firebase, so no setup is required for the database itself. 

When we have environment variables for our flask backend we will tentatively update the development requirements

## Deployment and Github Workflow
* We will use GitHub Projects with kanban boards to manage our upcoming tasks and assign them to team members
* All new code will be done on a new seperate branch
* Issues will be assigned to team members
* Pull requests will be made after significant progress is made to an individual section
* Prior to merging the branches to main, they will be reviewed by at least two other group members
* We have done this workflow in CSC207 and it was successful in the completion of that project
  
- DEPLOYMENT TOOLS TBD

## Coding Standards and Guidelines
We aim to keep all new features modular and independant of one another. As we are working with Python, we will stick with snake-case naming convention, and adhere to all other style conventions with respect to coding in Python. We will keep the code well documented and simple to understand for future developers to expand our codebase.

## Licences 
UNICEF values contributing to the open source community. Our partner believes that this project will not only be useful for UNICEF, but will also be desired by other companies. Therefore, we have received permission to upload the code on github and share it freely.
