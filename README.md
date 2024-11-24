# AC215 - Milestone3 - Cheesy App


**Team Members**
Jinghan HUANG, Zhiyu LI, Haozhuo YANG, Luozhong ZHOU

**Group Name**
Paper with Data

**Project**
In this project, we aim to develop an AI-powered cheese application. The app will feature visual recognition technology to identify various types of cheese and include a chatbot for answering all kinds of cheese-related questions. Users can simply take a photo of the cheese, and the app will identify it, providing detailed information. Additionally, the chatbot will allow users to ask cheese-related questions. It will be powered by a RAG model and fine-tuned models, making it a specialist in cheese expertise.


----

### Milestone4 ###

In this milestone, we have the components for frontend, API service, also components from previous milestones for data management, including versioning, as well as language models.

After completions of building a robust ML Pipeline in our previous milestone we have built a backend api service and frontend app. This will be our user-facing application that ties together the various components built in previous milestones.

**Application Design**

Before we start implementing the app we built a detailed design document outlining the application’s architecture. We built a Solution Architecture and Technical Architecture to ensure all our components work together.

Here is our Solution Architecture:

<img src="images/Solution Architecture.jpg"  width="800">

Here is our Technical Architecture:

<img src="images/Technical Architecture"  width="800">


**Backend API**

We built backend api service using fast API to expose model functionality to the frontend. We also added apis that will help the frontend display some key information about the model and data. 

```Add screenshots here```

**Frontend**

A user friendly React app was built to search the most relevant papers from our database of structured summaries of papers. The app will be much more accurate in terms of paper searching as it has fine-grained information in the database unlike traditional search engines that only rely on titles and abstract.

Here are some screenshots of our app:

```Add screenshots here```

## Running Dockerfile
Instructions for running the Dockerfile can be added here.
To run Dockerfile - `Instructions here`

