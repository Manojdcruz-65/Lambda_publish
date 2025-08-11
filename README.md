# 🌀 AWS Lambda Version Sync to GitHub (Automated Pipeline) + SonarQube Integration

This repository contains the automation to:
- Extract **published versions** of AWS Lambda functions
- Store the extracted code in **Amazon S3**
- Automatically sync the code to **GitHub** via **GitHub Actions**
- Trigger **SonarQube (or SonarCloud)** scans for static code analysis

---

## 📌 Use Case

Automatically track and analyze the code of deployed Lambda functions by:

- Capturing every **published version**
- Saving the code to **Amazon S3**
- Triggering **GitHub Actions** to:
  - Pull the Lambda code into the repository
  - Run a **SonarQube/SonarCloud** static code analysis scan
- Enabling:
  - **Git-based diffs**
  - **Change tracking**
  - **Version history**
  - **Code quality reporting**

---

## 🔧 Prerequisite

🚨 **Create a GitHub Actions workflow** from the directory:

🚨 Set up SonarCloud (or SonarQube)
Option 1: SonarCloud (Cloud-hosted, preferred for ease)
Go to https://sonarcloud.io
1.Log in with GitHub
2.Import your repo
3.Generate a token:
     Click on your avatar → My Account → Security → Generate Token
     Save this token in your GitHub repo secrets as SONAR_TOKEN

Option 2: SonarQube (Self-hosted)
You need a running SonarQube server with a project set up.
Generate a token from SonarQube
Save it in GitHub repo secrets as SONAR_TOKEN
Also set SONAR_HOST_URL if you're using SonarQube (e.g., http://your-sonarqube-domain)


## ⚙️ Architecture Overview

<img width="1087" height="699" alt="image" src="https://github.com/user-attachments/assets/bccff367-845b-435c-91bc-3b6989961868" />




## ✅ Step 1: Enable CloudTrail

If you haven’t already, follow these steps:

### 🛠️ Via AWS Console

1. Go to **AWS CloudTrail → Trails**
2. Click **Create trail**
3. Trail name: `default-trail` (or any name)
4. Choose **Management Events → Read/Write events → Write-only**
5. Choose **Create a new S3 bucket** or select an existing one
6. Click **Create trail**
> 📝 You only need to enable **Management Events** — no need for Data Events.
CloudTrail is now capturing the required publish events.
---


1. Go to **S3 → Create bucket**
2. Bucket name: e.g., `your_bucket_name`  
3. Region: Choose the same region where your Lambda runs
4. Uncheck **"Block all public access"**
5. Click **Create bucket**


## ✅ Step 3: create lambda

1. Go to **AWS Lambda > Create function**
2. Choose **Author from scratch**
3. Function name: `your_function_name`
4. Runtime: **Python 3.9 or 3.11**
5. Execution role:
   - Create a new role with basic Lambda permission
6.paste the code from above directory called Lambda_1 
7.Then after creating the role > go to roles then give this permisson's
        "lambda:GetFunction",
        "lambda:ListVersionsByFunction",
        "s3:PutObject"
   
## ✅ Step 4: Create EventBridge Rule
🛠️ Create via Console
1. Go to Amazon EventBridge → Rules
2. Click Create rule
3. Rule name: trigger-lambda-on-publish
4. Select Event Source: AWS Events or CloudTrail
5. In Event Pattern, choose Custom pattern, and paste the JSON above   ##paste the code from above directory called eventbridge_rule > rules.json
6. Target: Select your Lambda function ( previously created lambda)
7. Click Next, review, and create


## ✅ Step 5: create lambda for git actions trigger

1. Go to **AWS Lambda > Create function**
2. Choose **Author from scratch**
3. Function name: `your_function_name` 
4. Runtime: **Python 3.9 or 3.11**
5. Execution role:
   - Create a new role with basic Lambda permission (this basic rule is enough)
6.paste the code from above directory called Lambda_2


## ✅ Step 6: Create s3 event notification trigger for lambda

### Open the S3 Console
1. Go to the **S3 bucket** we created before
2. Click on the **Properties** tab
3. Scroll to **Event notifications**
4. Click **Create event notification**
    - **Name**: `trigger-github-action`
    - **Event types**: ✅ `All object create events`
    - **Destination**:  
       - ✅ **Lambda function**
        - Choose `your-lambda-function for git triggers`
Click **Save changes**


## ✅ Final Setup Complete

Your automated pipeline is now live! 🎉

Whenever you **publish a new version** of an AWS Lambda function, the pipeline will:

1. **Detect** the publish event via CloudTrail + EventBridge  
2. **Extract** the Lambda code using AWS Lambda  
3. **Store** it temporarily in Amazon S3  
4. **Push** it to GitHub via GitHub Actions  
5. **Scan** it with SonarQube for code quality and security issues  

No manual steps required — just **publish in Lambda**, and the process handles everything automatically. 🚀


## ✅ Conclusion

This fully automated, event-driven pipeline bridges the gap between **deployed AWS Lambda functions** and **source control visibility**.

By combining:
- **CloudTrail + EventBridge** for detecting version publications  
- **AWS Lambda** for extraction and orchestration  
- **Amazon S3** for temporary code staging  
- **GitHub Actions** for syncing to version control
- **SonarQube** for static code analysis, quality gating, and security scanning

You get a **cost-effective**, **serverless**, and **version-aware DevOps solution** that:
- Maintains a Git-tracked history of production Lambda code  
- Makes debugging and audits easier through code transparency  
- Supports clean DevOps practices without adding manual steps

> Ideal for teams using CI/CD, GitOps, or managing distributed Lambda functions across environments.

---
With this automation in place, every published Lambda version is automatically archived and version-controlled — giving you peace of mind and visibility into what’s really running in production.
