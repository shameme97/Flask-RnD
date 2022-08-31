import boto3
import os
import sys
sys.path.append("..")
from config.s3Config import s3_client, s3
from werkzeug.utils import secure_filename
from boto3.s3.transfer import TransferConfig

BUCKET = os.getenv('AWS_BUCKET_NAME')
BUCKET = 'movies'

def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    print(file_name)
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=5*GB)
    object_name = file_name
    response = s3_client.upload_file(file_name, bucket, object_name, Config=config)

    return response


def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    contents = []
    print(s3_client.list_objects(MaxKeys=2,Bucket='movies'))
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            print(item)
            contents.append(item)
    except Exception as e:
        return "error bro"
        pass

    return contents