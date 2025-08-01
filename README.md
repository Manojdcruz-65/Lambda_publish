# 🌀 AWS Lambda Version Sync to GitHub (Automated Pipeline)

This repository contains the automation to extract AWS Lambda **published versions**, store them in **S3**, and sync the extracted code to **GitHub** using GitHub Actions.

## 📌 Use Case

Automatically track the code of deployed Lambda functions by:
- Capturing every **published version**
- Saving the code to **Amazon S3**
- Triggering **GitHub Actions** to pull that code into GitHub
- Enabling **Git-based diffs**, change tracking, and version history

## ⚙️ Architecture Overview


L2G.jpg 

