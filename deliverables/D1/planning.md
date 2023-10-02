# Red Pandas, Team 12

## Product Details
 
#### Q1: What is the product?

 > Short (1 - 2 min' read)
 * Start with a single sentence, high-level description of the product.
 * Be clear - Describe the problem you are solving in simple terms.
 * Specify if you have a partner and who they are.
 * Be concrete. For example:
    * What are you planning to build? Is it a website, mobile app, browser extension, command-line app, etc.?      
    * When describing the problem/need, give concrete examples of common use cases.
    * Assume your the reader knows nothing about the partner or the problem domain and provide the necessary context. 
 * Focus on *what* your product does, and avoid discussing *how* you're going to implement it.      
   For example: This is not the time or the place to talk about which programming language and/or framework you are planning to use.
 * **Feel free (and very much encouraged) to include useful diagrams, mock-ups and/or links**.


#### Q2: Who are your target users?

  > Short (1 - 2 min' read max)
 * Be specific (e.g. a 'a third-year university student studying Computer Science' and not 'a student')
 * **Feel free to use personas. You can create your personas as part of this Markdown file, or add a link to an external site (for example, [Xtensio](https://xtensio.com/user-persona/)).**

#### Q3: Why would your users choose your product? What are they using today to solve their problem/need?

> Short (1 - 2 min' read max)
 * We want you to "connect the dots" for us - Why does your product (as described in your answer to Q1) fits the needs of your users (as described in your answer to Q2)?
 * Explain the benefits of your product explicitly & clearly. For example:
    * Save users time (how and how much?)
    * Allow users to discover new information (which information? And, why couldn't they discover it before?)
    * Provide users with more accurate and/or informative data (what kind of data? Why is it useful to them?)
    * Does this application exist in another form? If so, how does your differ and provide value to the users?
    * How does this align with your partner's organization's values/mission/mandate?

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

Describe the different roles on the team and the responsibilities associated with each role. 
 * Roles should reflect the structure of your team and be appropriate for your project. One person may have multiple roles.  
 * Add role(s) to your Team-[Team_Number]-[Team_Name].csv file on the main folder.
 * At least one person must be identified as the dedicated partner liaison. They need to have great organization and communication skills.
 * Everyone must contribute to code. Students who don't contribute to code enough will receive a lower mark at the end of the term.

List each team member and:
 * A description of their role(s) and responsibilities including the components they'll work on and non-software related work
 * Why did you choose them to take that role? Specify if they are interested in learning that part, experienced in it, or any other reasons. Do no make things up. This part is not graded but may be reviewed later.


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
