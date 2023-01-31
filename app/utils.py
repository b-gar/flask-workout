import boto3
import os

def aws_authenticate(table_name):
    dynamo = boto3.resource(
        service_name="dynamodb",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET")
    )
    table = dynamo.Table(table_name)
    return table
