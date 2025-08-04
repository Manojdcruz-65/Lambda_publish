import json
import os
import urllib.request
import http

def lambda_handler(event, context):

    repo = os.environ["GITHUB_REPO"]    # Replace with your GitHub repository name   
    token = os.environ["GITHUB_TOKEN"]  # Replace with your GitHub token     
    workflow_file = "your_workflow_file.yml"  # Replace with your workflow file name

    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_file}/dispatches"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

    payload = {
        "ref": "main", 
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            print("Github triggered successfully")
    except urllib.error.HTTPError as e:
        print("GitHub API error:", e.read().decode())
        raise
