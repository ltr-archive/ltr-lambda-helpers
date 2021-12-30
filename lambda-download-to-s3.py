# Download a specified path and save it to an S3 bucket

# Thanks to
# https://stackoverflow.com/a/47736376
# https://stackoverflow.com/a/32490661
# https://towardsdatascience.com/serverless-functions-and-using-aws-lambda-with-s3-buckets-8c174fd066a1

# Attempt 2
# https://stackoverflow.com/a/42254534
# https://stackoverflow.com/a/59185523

import os
import json
import boto3
import logging
from botocore.exceptions import ClientError
import urllib.request
import shutil
from pathlib import Path
from datetime import datetime

URL = os.environ['url']  # URL of the site to download, stored in the site environment variable
BUCKET = os.environ['destination_bucket']
FOLDER = os.environ['destination_folder']
FILENAME = os.environ['destination_file']

def generate_bucket_filename():
    date = datetime.today().strftime('%Y-%m-%d')
    folder = FOLDER
    filename = FILENAME
    return f'{folder}/{date}/{filename}'

def generate_tmp_filename():
    filename = FILENAME
    return f'/tmp/{filename}'


# Thanks to https://stackoverflow.com/a/7244263/756641

def download_to_filename(url, file_name):
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def upload_to_s3(local_file, bucket, key):
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.upload_file(local_file, bucket, key)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_and_upload():
    url = URL  # put your url here
    bucket = BUCKET  # your s3 bucket
    key = generate_bucket_filename()  # your desired s3 path or filename
    local_file = Path(generate_tmp_filename())

    

    print(f'Downloading from {url}')
    
    download_to_filename(url,generate_tmp_filename())

    print(f'Saving to bucket: {bucket} in {key}')

    upload_to_s3(generate_tmp_filename(), bucket, key)
    
    # Delete the local file
    local_file.unlink(missing_ok=True)

def lambda_handler(event, context):
    try:
        response = download_and_upload()
    except:
        raise Exception('Download and upload failed')
    else:
        print('Check passed!')
        return event['time']
    finally:
        print('Check complete at {}'.format(str(datetime.now())))
        return {
            'statusCode': 200,
            'body': json.dumps('Lambda run complete!')
        }
    

