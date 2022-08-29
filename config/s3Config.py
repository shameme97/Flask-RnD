import boto3, botocore
import os


s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    endpoint_url="http://localhost:4566/movies",
    # endpoint_url="https://movies.s3.ap-southeast-1.localhost.localstack.cloud"
)

s3 = boto3.resource(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    endpoint_url="http://localhost:4566/movies",
    # endpoint_url="https://movies.localhost.localstack.cloud"
)
