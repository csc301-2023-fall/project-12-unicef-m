## 1. Summary of your software

### a. One paragraph for the problem & partner (if applicable)

Our primary point of contact for this project is Evan Wheeler (ewheeler@unicef.org).

UNICEF is a multinational organization dedicated to protecting, assisting, and creating environments for children to grow up with the 
resources they need. They make data-driven decisions and support humanitarian efforts worldwide.

Our primary goal is to build a web interface for an existing command line proof-of-concept that clones Apache Superset dashboards. 
Users will have the ability to modify and clone existing dashboards. Additionally, new features, such as a version control that would allow 
for the propagation of changes from the configuration to the parent dashboard to the cloned children and cloning dashboards across Superset 
instances. The current problem is difficulty surrounding the use of the cloning tool and redundant testing for staging and production environments, 
and so with these additions, UNICEF employees will have the tools to quickly and easily visualize any datasource they want. This application 
will allow larger teams to work together on dashboards across the globe, rather than individual users having their own instances on their accounts.

### b. One paragraph introducing any existing software/infrastructure
There are two main existing software that our project intends to build upon. The first is Apache Superset, a powerful open source tool which is 
used to visualize large amounts of data. The second existing piece of software is a proof-of-concept command line cloner, that has the necessary 
functionality to clone Apache Superset dashboards. The current proof-of-concept will need to be modified in order to work with our application. 

## 2. 1-4 paragraph(s) on how you decided to divide the project and why. Ideally, this will be accompanied by a software architecture diagram 
and how each component connects to the others.

We have decided to divide our work into three parts into frontend, backend, and the version control feature which involves initialising the database. 
This general division is common practice because people have different skill sets and learning goals. One of the most important reasons for this is 
so that our code does not overlap and we are able to work strictly within our subteams. We have already discussed making the code decoupled and ready 
to be put together for the following deliverable. The front-end deals with the initial screens, some functionalities, and sets up a template of what it 
needs from the back-end. The back-end will make the necessary API calls to provide the data for the front end to display, as well as work on fixing the 
proof-of-concept and having it work with the front end. The version control feature is a direct use case of the database so we are able to both set up 
Firebase and have an important feature ready.   

![Login](architecture.png)

First, the user initiates the update on the update page. Then, an HTTP request is sent to views, that also tells the webpage to update the view with the 
necessary information. From views.py, that request is sent to api_helpers.py and fetches the information from the superset API. That information is sent 
to app.py, from which our database is updated and the information is sent to dashboard_handler.py and our necessary views are updated in the frontend. 

## 3. One paragraph for part(s) each sub-team is responsible for.

### Nick and Jessica, Frontend team:

The frontend team is responsible for creating a fully functional front end that is ready to connect with the backend. Front end should include every page 
in the user flow chart, excluding the source page . The reason we’ve chosen to omit our source page for now is due to design decisions from our backend 
team, once those have been finalised we will then implement that view. Next steps are to figure out how to fetch data from our backend and update the 
front end accordingly to propagate these changes in the view. Our front end was created using React + Vite and written in Javascript, HTML, CSS, and utilised 
the TailwindCSS CSS framework.The reason for this is that we ran into issues when cloning the project when it was created with the default 
“npx create-react-app <appname>” terminal command then cloning those files. When creating the project with React + Vite, we found no issues post cloning. 

### Andrew and Manya, Backend team:

The backend team is responsible for designing and creating a server that is responsible for connecting the user interface with the proof of concept. 
We used Flask to host the server and built a simple mock-up HTML webpage to simulate the overall capabilities and inputs of the users. For the backend, 
we focused on providing the frontend with the complete list of all dashboards that can be cloned, the charts belonging to the dashboard, and the names of 
the datasets that are available to populate the charts. Our next step is to connect the cloning functionality with all the fields that the user selects. 
However, we have run into two big problems while working on this next step. Firstly, one of our laptops is incapable of running Apache Superset and we are 
waiting for our contact to provide a cloud hosted version of Apache Superset that the entire team can access to test our code. Secondly, we have encountered 
an error running the existing software, due to an incompatibility with the format of the returned object from their API, which has halted our progress with 
the cloning use case. 

### Rohan and Rudy, Database team:

As the database team we are responsible for initializing the real-time, non-relational database, therefore, we decided to use Firebase. We used Flask and 
Firebase to create a schema and create endpoints for the other teams to call. The dashboard version control feature is a direct application of the database 
so we were able to get the main CRUD functionality working and are open to adding more functionality as we receive the actual data from our partners. We have 
created a test suite along with using Postman to check our API calls. The next steps would be to solidify the feature with actual dashboards from UNICEF and 
set up the database to work with the across instance cloning. This may result in a change of schema and impact our version control feature and testing and we 
are prepared to change things as needed.
