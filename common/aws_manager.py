import boto3
import os
from common import utils

root = utils.get_project_root()


def upload_file(file_name, bucket, object_name):
    """
    Function to upload a file to an S3 bucket
    """
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response


def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = os.path.join('data', 'videos', file_name)
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def list_videos(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        for extension in utils.ALLOWED_EXTENSIONS:
            if item.get('Key').endswith(extension):
                contents.append(item)
    return contents


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        if item.get('Key').endswith('.txt'):
            contents.append(item)
    return contents
