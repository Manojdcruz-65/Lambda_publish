import boto3
import os
import zipfile
import tempfile
import urllib.request

# S3 bucket name
s3_bucket = "your-s3-bucket-name"  # Replace with your actual S3 bucket name

# AWS clients
lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event:", event)

    try:
        # Extract Lambda function details from CloudTrail Event
        detail = event.get("detail", {}).get("responseElements", {})
        function_arn = detail.get("functionArn")
        function_name = detail.get("functionName")

        if not function_arn or not function_name:
            raise ValueError("Missing functionArn or functionName in event.")

        print("Function Name:", function_name)

        # Use full function name as folder name
        folder_prefix = function_name
        print(f"Uploading to: {folder_prefix}/")

        # Find latest published version (not $LATEST)
        version_set = set()
        paginator = lambda_client.get_paginator('list_versions_by_function')
        for page in paginator.paginate(FunctionName=function_name):
            for version in page["Versions"]:
                ver = version["Version"]
                if ver != "$LATEST":
                    version_set.add(ver)

        if not version_set:
            raise Exception("No published versions found.")

        latest_version = max(version_set, key=lambda x: int(x))
        print(f"Latest Published Version: {latest_version}")

        # Get download URL for that version
        version_info = lambda_client.get_function(
            FunctionName=function_name,
            Qualifier=latest_version
        )
        code_url = version_info["Code"]["Location"]

        # Temporary download and extract
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "lambda.zip")
            urllib.request.urlretrieve(code_url, zip_path)

            extract_path = os.path.join(tmpdir, "extracted")
            os.mkdir(extract_path)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)

            # Upload to S3
            for root, _, files in os.walk(extract_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, extract_path).replace("\\", "/")
                    s3_key = f"{folder_prefix}/{relative_path}"

                    with open(local_file_path, "rb") as data:
                        s3_client.upload_fileobj(data, s3_bucket, s3_key)

                    print(f"Uploaded: s3://{s3_bucket}/{s3_key}")

        return {
            "statusCode": 200,
            "message": f"Uploaded latest files for {function_name} to {folder_prefix}/"
        }

    except Exception as e:
        print("Error occurred:", str(e))
        return {
            "statusCode": 500,
            "error": str(e)
        }
