import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
from common import utils

root = utils.get_project_root()
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('Videos')


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
        key = item.get('Key')
        if key.endswith('.txt'):
            video_name_no_extension, video_name_extension = os.path.splitext(key)
            contents.append(video_name_no_extension)
    return contents


def dynamo_upload(item):
    table.put_item(Item=item)


def dynamo_download(video_name):
    response = table.get_item(
        Key={
            'name': video_name
        })
    return response


def dynamo_delete(video_name):
    response = table.delete_item(
        Key={
            'name': video_name
        })
    return response


def dynamo_list(result_type):
    table_list = table.scan(FilterExpression=Attr('type').eq(result_type))
    return table_list['Items']

