# Red Pandas, Team 12

## Product Details
 
#### Q1: What is the product?

We will be building a web interface for the existing command line proof of concept that clones Apache Superset dashboards. Users will have the ability to modify and clone existing dashboards. The partner is UNICEF and this product will help the teams internally modify and clone their dashboards to make data-driven decisions. At a high level, the problem is not being able to easily clone as right now, we have to do redundent testing and there is no web interface for teams.  

![Login](loginScreen.jpg)
![Login](dashboards.png)
![Login](dashboard_customization.jpg)
![Login](sources.png)

#### Q2: Who are your target users?

The tool we build will be used internally by UNICEF personnel who work in different countries. However, the tool will also be accessible to anyone who is working with Apache Superset dashboards. The project is aimed for people who have varying levels of expertise, and may not be well versed in Apache Superset. The goal is to create an intuitive interface for ease of use for our entire target users.

#### Q3: Why would your users choose your product? What are they using today to solve their problem/need?

Currently, the proof of concept only works on a single instance of Apache Superset. This is problematic because when dashboards are cloned in different environments, for example staging and production, the dashboard must be recreated in production anyways. This means that the dashboard must be tested again in production, defeating the purpose of the staging environment. 

Secondly, the current proof of concept is a simple command line program. This is not very accessible for people who are not experienced in superset, so our web app will be more intuitive to use and allow for easier visualisation of data, regardless of a person’s given proficiency with superset. Additionally, it allows for smaller teams to do the cloning, we plan on expanding on this feature with a web application to allow use for larger teams. Evan has also mentioned that over a hundred different UNICEF offices utilise this tool. Due to the breadth at which it is used, there is a need to design it such that all offices can use the application to the same general level of proficiency.

Third, as we have discussed with Evan, he has put forward the need for such a program to be open source so that it can be copied and modified for a user’s given purposes.

#### Q4: What are the user stories that make up the Minumum Viable Product (MVP)?

User Story 1: As a data analyst at UNICEF, I have many datasets. I would like to see the available dashboards that can be cloned with the other viable data sources I can use as the new datasource for the clone. 

Acceptance Criteria 1: Having multiple screens for available dashboards and viable data sources respectively. Being able to sort datasets in the view according to different features of the data and/or country and having clear indications of whether a dataset is viable with and reasons to why it is not viable.  

User Story 2: As a large team of data analysts, we would like to make use of the dashboard cloning capabilities to deploy ~130 copies for each country’s datasource.

Acceptance Criteria 2: Have a lightweight web interface that can support multiple users, user’s information is saved, a potential for group accounts that can allow for multiple users making edits as long as conflicts are limited.

User Story 3: As an open-source developer using Apache Superset, I would like to contribute to this project by increasing the scalability and improving the web application.

Acceptance Criteria 3: Web application has a test suite that runs each time new features are added/deployed, test suites that can be expanded upon as more features are added, have well-written and easily to follow documentation and instructions within the code, Read.me file, and the repository itself. Additionally,  regarding documentation, providing more visual examples of what the user should be met with when interacting with the application. 

User Story 4: As a developer responsible for deploying Apache Superset instances, I want to be able to clone dashboards across Superset instances so that I do not have to retest a dashboard in the production environment once it's passed all its tests in the staging environment. 

Acceptance Criteria 4: Given the user provides the correct details for accessing two Superset instances A and B, when the user clones a dashboard from one Superset instance A to Superset instance B, an exact replica of the dashboard should successfully appear within Superset instance B.

User Story 5: As a developer, I would want to customise the dataset features such as its name and add notes. I would also like to see new changes, especially since I work within a team.

Acceptance Criteria 5: Having screens prior and post cloning to edit names, adding notes, and the ability to link the dataset to another user. Having an option to view recent cloning, changes, or history to track activity. 


#### Q5: Have you decided on how you will build it? Share what you know now or tell us the options you are considering.

For our frontend, we have decided to use React.js with JavaScript. We will style our React app with TailwindCSS, which will allow us to speed up our development process since it allows us to use pre-built CSS classes for styling, allowing us to focus more on the actual functionality than the design. 

For our backend, we have decided to use Flask and Python. We originally wanted to use Node.js to gain experience with the MERN stack. However, the current proof of concept is built with Python scripts, so keeping our backend as Python will make it easier to integrate our code with the existing code. We will also be using FlaskAppBuilder since Apache Superset is also built using it. 

We will be using the Apache Superset APIs in the backend, to do the bulk of the work, such as cloning the dashboards and replacing their data sources.

Our liaison has communicated to us that it is acceptable for us to not deploy the product anywhere; rather, he is comfortable with this being hosted locally on a computer.


----
## Intellectual Property Confidentiality Agreement 
> Note this section is **not marked** but must be completed briefly if you have a partner. If you have any questions, please ask on Piazza.
>  
**By default, you own any work that you do as part of your coursework.** However, some partners may want you to keep the project confidential after the course is complete. As part of your first deliverable, you should discuss and agree upon an option with your partner. Examples include:
1. You can share the software and the code freely with anyone with or without a license, regardless of domain, for any use.
2. You can upload the code to GitHub or other similar publicly available domains.
3. You will only share the code under an open-source license with the partner but agree to not distribute it in any way to any other entity or individual. 
4. You will share the code under an open-source license and distribute it as you wish but only the partner can access the system deployed during the course.
5. You will only reference the work you did in your resume, interviews, etc. You agree to not share the code or software in any capacity with anyone unless your partner has agreed to it.

**Your partner cannot ask you to sign any legal agreements or documents pertaining to non-disclosure, confidentiality, IP ownership, etc.**

UNICEF values contributing to the open source community. Our partner believes that this project will not only be useful for UNICEF, but will also be desired by other companies. Therefore, we have received permission to upload the code on github and share it freely. This corresponds to option 1. 

----

## Teamwork Details

#### Q6: Have you met with your team?

Do a team-building activity in-person or online. This can be playing an online game, meeting for bubble tea, lunch, or any other activity you all enjoy.
* Get to know each other on a more personal level.
* Provide a few sentences on what you did and share a picture or other evidence of your team building activity.
* Share at least three fun facts from members of you team (total not 3 for each member).


#### Q7: What are the roles & responsibilities on the team?

Rudy: Backend, dedicated partner liaison. I have done some back end node.js and would like to learn more about using Flask.

Rohan: Front end + some backend. Aside from the prerequisite courses, I have not had exposure to devlopement so I would like to work on some aspects of each use case if possible, for an optimal leanring experience. 

Jessica: Front end + some Backend

Manya: Backend

Nick: Front end + some Backend

Andrew: Backend


#### Q8: How will you work as a team?

As a team, we are planning to have weekly meetings online on Thursdays to discuss that week’s objectives, what progress has been made since the last meeting, any challenges, and coding sessions/reviews. We also have a discord server set up and a Google Docs document set up for each deliverable/project component so the work can be more active throughout the week.

We have had two meetings with our partner. 

As an overview of our first meeting we were introduced to the problem domain and the current proof-of-concept which is a command-line application that aims to solve the dashboard cloning problem for UNICEF employees. We were invited to the repository and asked to explore it and generate questions and concerns. Evan was lenient with what technologies we use for the web application, but the current POC is made with Python, Flask, and Flash App-Builder. We also discussed the IP concerns, which there are none, we are free to share the code since it is open source. We also discussed the future meeting schedules with Evan, which for now will be on the more “random” side due to his travel schedule. He mentioned that in mid-October he will be able to have a more concrete schedule and involve more of the engineers who worked on the product to help guide us as well. 

  
#### Q9: How will you organize your team?

For schedules we have a When2Meet set up and we will use the assignments as a rough timestamp to guide our development milestones. We will use the github project as a task board, and rank the TODO list to prioritise tasks. Overall we will discuss these details in the weekly meetings as well as update each other in the discord group chat.

#### Q10: What are the rules regarding how your team works?

Our team plans to meet online at least twice a week, once during the tutorial time and again on Thursday evenings. Our primary mode of communication will be our Discord channel. 

Our partner has a packed schedule until mid-October, so he will update a spreadsheet with his availability. We will use this to book meetings with him. After mid-October, he will have a more structured schedule, so we will be able to set up a consistent time to meet.

If a team member is not contributing, we will first attempt to understand why they are not responding as often. If it is due to stress, we will support them by helping them catch up on their work and taking on some of their tasks while they catch up. We will also encourage everyone to communicate when they are feeling stressed so that the other team members can be prepared.

 
**Collaboration: (Share your responses to Q8 & Q9 from A1)**
 * How are people held accountable for attending meetings, completing action items? Is there a moderator or process?
 * How will you address the issue if one person doesn't contribute or is not responsive? 
