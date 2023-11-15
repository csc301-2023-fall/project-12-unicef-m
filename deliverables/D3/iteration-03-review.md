# Team 12, Red Pandas

## NOTE TO TA FOR D3:

We have created a video for our D3 submission.

#### Video Link:

https://docs.google.com/document/d/15DNbcaayjMLIahSCqLSsfEdc5vjFLFGZHfgA4R6nAxw/edit?usp=sharing

## Review & Retrospect

 * When: November 1 and 8
 * Where: Online

## Process - Reflection

#### Q1. What worked well

Our group was able to connect the various pieces created by each subteam together. Specifically, we allowed the frontend and backend to communicate to send and retrieve the data needed to have an MVP. 

With the feedback that our partners gave us, we were able to make improvements to our program. Firstly, we improved our frontend to be more accessible to all users and redesigned each page with more components. This includes everything we have listed in the frontend feedback section, which is conforming to WCAG AA guidelines and UNICEF colour schemes. The front-end now works seamlessly with the backend and has been tested. Also, as mentioned in the tutorial prior to reading week, the initial proof-of-concept we relied on was not working due to many changes to Superset and the code being hard-coded to handle JSON only. We discussed remaking the POC entirely with our partner and spent a majority of our time working on fixing it. We were able to make significant progress towards remaking the POC. Our files and folders are structured and documented very clearly so that the UNICEF team can use and add upon it with ease.

With regards to our process changes, we have ensured that pull requests must be reviewed and accepted by at least one other individual. This ensures that we are writing functional code and that multiple individuals understand the changes that are occurring as we progress through this project. Additionally, we have created two environments, specifically, a main and development branch, with additions such as adding in authorization and version control code being sub-branches of development and pushed in as significant changes are made. Once we complete POC code, this change will allow us to ensure that there is always a functional deployed product using the main branch, which will not be affected by our changes pushed into the develop branch.

#### Q2. What did not work well

As mentioned, the POC had to be completely remade and our initial goals of adding functionality into learning how to fix the issues. This task turned out to be much harder than anticipated. A majority of the functions have been completed, as of November 12, and our manual tests (running the logic by hand, rather than through code) have been working. However, we continue to run into issues with writing post requests to create a dashboard on Superset.

As part of our feedback for Deliverable 2, we have ensured that we keep more documentation of the changes occurring throughout the project. We have been actively creating documented branches and pushing them into our development environment once significant progress has been made to a particular functionality.

#### Q3(a). Planned changes

As mentioned in Questions 1 and 2 we are continuing with the same process as it has worked well.

We will continue to meet as a group at least once a week, with additional meetings between members whenever there is a discussion to be had. Secondly, we will continue our current workflow of creating separate branches for different features and merging them into our development branch once significant progress has been made. Currently, subsets of team members are working together in a call on different branches or to debug code. This has worked really well and has made our process significantly more efficient so we will continue to arrange calls between duos or trios to have multiple views and have others explain different parts of the code to each other. Additionally, we need to learn new things, like new APIs, or have not been a part of the separate calls between calls between a subset of a team. Therefore, we will continue to document our code and keep other members updated in our Discord channel.

#### Q3(b). Integration & Next steps

All of the code was decoupled from the start so there were little to no merge conflicts. All we had to do was edit some files to combine them, such as our endpoints, environment variables, and testing suites. We found the split into subteams helpful because it helped us break down a large project into smaller components. 

## Product - Review

#### Q4. How was your product demo?

### Frontend Demo

Summary:

Showed login page
Showed cloning pages
Showed version control features
Explained next steps of the development of the frontend website

Feedback:

We should continue to make our user interface’s more accessible and add in the new features. Some important accessibility features to keep in mind are font size, contrast between background and text, and to provide proper navigational features to allow users to go to any feasible page as they please. To improve on this, we will refer and adhere to the WCAG Level AA guidelines as instructed by our partner.

To improve our user interface for the target audience that is UNICEF, we will strictly utilise the official UNICEF colour schemes. As we have been provided a link (https://unicef.github.io/design-system/), it will be a simple but visually appealing change for our partners at UNICEF.

### Backend Demo

Summary:

Showed interactions between Superset and frontend
Showed key features including renaming dashboards, charts, and selecting datasets
Explained main challenges arising due to incompatibility errors between the POC and the Superset API

Feedback:

Project needs to shift focus now as a useful program is more important than additional features. Therefore, it will be our task to correct and remake the POC to the best of our ability and create a functional program that UNICEF employees and other Superset users can take advantage of. As part of our goal for D3, we will be combing through the POC, identifying the incomplete and error prone code and replacing it completely.

Due to the size of the list of dashboards, charts, and datasets, our initial usage of a dropdown menu, created on our mockup frontend, will be insufficient. We will need to add a search feature to allow the users to quickly narrow down the number of items that they must look at.

### Version Control Demo

Summary:

Showed current schema for the version control database
Demoed how the version control works, specifically highlights the functionality related to propagating changes from a dashboard to its children, as well as accepting incoming changes.

Feedback:

Initial thoughts on the version control are positive, however, now our partners would prefer the utilisation of a database that is open-source. So rather than using Firebase, we could potentially switch to alternative databases such as MongoDB or CouchDB after all the code and endpoints are finalized. However, as this change does not affect the functionality of the project, as a MVP, these changes will only be made if time permits. 

Additional Feedback for all teams:

A good amount of documentation will be important as this project will be taken over by our partners at UNICEF. Therefore, we must ensure that this transition occurs as smoothly as possible. Some specific things that we will add include docstring for functions that we are writing, comments for difficult to understand sections of code, and leaving clear instructions to set up the project.
