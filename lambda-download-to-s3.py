# Download a specified path and save it to an S3 bucket

# Thanks to
# https://stackoverflow.com/a/47736376
# https://stackoverflow.com/a/32490661
# https://towardsdatascience.com/serverless-functions-and-using-aws-lambda-with-s3-buckets-8c174fd066a1

import os
import json
import boto3
import botocore.vendored.requests.packages.urllib3 as urllib3
import logging
from botocore.exceptions import ClientError
from datetime import datetime

URL = os.environ['url']  # URL of the site to download, stored in the site environment variable
BUCKET = os.environ['destination_bucket']
FOLDER = os.environ['destination_folder']
FILENAME = os.environ['destination_file']

def generate_filename():
    date = datetime.today().strftime('%Y-%m-%d')
    folder = FOLDER
    filename = FILENAME
    return f'{folder}/{date}/{filename}'

def download_and_upload():
    url = URL  # put your url here
    bucket = BUCKET  # your s3 bucket
    key = generate_filename()  # your desired s3 path or filename

    print(f'Downloading from {url}')
    print(f'Saving to bucket: {bucket} in {key}')

    s3=boto3.client('s3')
    http=urllib3.PoolManager()
    try:
        s3.upload_fileobj(http.request('GET', url,preload_content=False), bucket, key)
    except ClientError as e:
        logging.error(e)
        return False
    return True

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
    

