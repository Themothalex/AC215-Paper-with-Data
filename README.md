# AC215 - Milestone5 - Paper with Data


**Team Members**

Jinghan HUANG, Zhiyu LI, Haozhuo YANG, Luozhong ZHOU

**Group Name**

Paper with Data

**Project**

In this project, we aim create a dataset-centered search portal. This portal will enable researchers to use fine-grained dataset catefories and filter papers not just based on the presence of datasets, but also on the nature of their relationships. The core of our project is to construct a database of summarise of dataset from which we can get the most relevant papers to the query by users. We first use Gemini to construct a database and then use RAG to facilitate the searching process.

**I. Prerequisites**

**II. Setup Instructions**

**III. Usage Example**

**IV. Known Issues and Limitations**

**V. More About The Project**

**VI. Demo for the Application of K8S**

---
---

## Prerequisites
---

Before you begin, ensure you have the following installed and configured:

**Docker Engine**

Install Docker if not already installed.
Verify the installation by running:

```
docker --version
```

**A Google Cloud Platform account with appropriate permissions.**

Required actions include:
1. Get a secret in the format of `JSON` from [service account](https://cloud.google.com/iam/docs/service-account-overview). You should assign your service account with the following roles:
  * Compute Admin
  * Compute OS Login
  * Container Registry Service Agent
  * Kubernetes Engine Admin
  * Service Account User
  * Storage Admin
2. Enable relevant APIs.
  * Compute Engine API
  * Service Usage API
  * Cloud Resource Manager API
  * Google Container Registry API

Ensure your GCP credentials are stored securely. You can download the service account key file from your GCP console.

## Setup Instructions
---

Clone the repository:
```
git clone https://github.com/Themothalex/AC215-Paper-with-Data.git
```

Create a folder called `secrets`.
```
mkdir secrets
```

Rename you secrets into `deployment.json` and put it into `./secrets/`

Go to `./src` and run the following code:
```
sh deploy_pipeline.sh
```

You may need to wait for a few minutes as the pipeline above has done anything for you!

Once the process completes, you can access the application by visiting the external IP address of your virtual machine.

You can get the IP address from:

<img src="/images/external_ip.jpg" alt="Description" width="600">

Then you will land our main page!

<img src="/images/main_page.jpg" alt="Description" width="600">

## Usage Example

The following is an example. Let's say you are interested in studying the factors affecting one's **income**. You can set the independent variable to be **income**, and then click "Search Paper". You will immediately get a list of studies having income as the variable of interest.

<img src="/images/demo.jpg" alt="Description" width="600">


## Known Issues and Limitations

**Known Issues:** The paper results are not well formatted. In the next version, we will prettify the format of paper results.

**Limitations:** The dataset is not big enough and specialized enough, so that users may not immediately get the value of this project. 


## More About The Project
---

**Application Design**

Before we start implementing the app we built a detailed design document outlining the application’s architecture. We built a Solution Architecture and Technical Architecture to ensure all our components work together.

Here is our Solution Architecture:

<img src="images/Solution Architecture.jpg"  width="600">

Here is our Technical Architecture:

<img src="images/Technical Architecture.jpg"  width="600">


**Backend API**

We built backend api service using fast API to expose model functionality to the frontend. We also added apis that will help the frontend display some key information about the model and data. 

<img src="images/Backend.jpg"  width="600">

**Frontend**

A user friendly React app was built to search the most relevant papers from our database of structured summaries of papers. The app will be much more accurate in terms of paper searching as it has fine-grained information in the database unlike traditional search engines that only rely on titles and abstract.

## Demo for the Application of K8S

**Deployment of Kubernetes cluster**

<img src="images/k8s_deploy_1.png"  width="600">

<img src="images/k8s_deploy_2.png"  width="600">

**Scaling K8S Load**

<img src="images/k8s_scale.png"  width="600">



