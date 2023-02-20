import boto3
import os
from math import floor
import pandas as pd

def aws_authenticate(table_name):
    dynamo = boto3.resource(
        service_name="dynamodb",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET")
    )
    table = dynamo.Table(table_name)
    return table

def dynamo_to_df(table):
    results = []
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = table.scan(ExclusiveStartKey=last_evaluated_key)
        else:
            response = table.scan()
        last_evaluated_key = response.get("LastEvaluatedKey")

        results.extend(response["Items"])

        if not last_evaluated_key:
            break
    return pd.DataFrame(results)

def num_exercises(difficulty_input, duration_input):
    if difficulty_input == "Easy":
        return floor(int(duration_input) / 2.75)
    elif difficulty_input == "Moderate":
        return floor(int(duration_input) / 3.42)
    else:
        return floor(int(duration_input) / 4.42)

def num_seconds(difficulty_input):
    if difficulty_input == "Easy":
        return 20
    elif difficulty_input == "Moderate":
        return 30
    else:
        return 45