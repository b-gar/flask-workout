import boto3
from flask_mail import Mail
import os
from math import floor, ceil
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

def gmail_authenticate(app):
    app.config['MAIL_SERVER'] = "smtp.gmail.com"
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "swolify.app@gmail.com"
    app.config['MAIL_PASSWORD'] = os.getenv("GMAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = "swolify.app@gmail.com"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    return mail

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

def set_time(difficulty_input):
    if difficulty_input == "Very Easy":
        return 130
    elif difficulty_input == "Easy":
        return 160
    elif difficulty_input == "Moderate":
        return 150
    elif difficulty_input == "Hard":
        return 190
    else:
        return 240

def rest_time(difficulty_input):
    if difficulty_input in ["Moderate", "Hard"]:
        return 40
    else:
        return 50

def num_exercises(difficulty_input, duration_input):
    time = set_time(difficulty_input)
    rest = rest_time(difficulty_input)
    return floor(((int(duration_input) * 60) + rest) / time)

def filter_exercises(df, equipment_input, n_exercises):
    if equipment_input == "Bodyweight":
        return df[df.Equipment == "Bodyweight"].groupby("Focus").sample(ceil(n_exercises / 3)).sample(n_exercises).drop(["key", "Focus", "Category", "Equipment"], axis=1)
    elif equipment_input == "Kettlebell":
        return df[df.Equipment == "Kettlebell"].groupby("Focus").sample(ceil(n_exercises / 3)).sample(n_exercises).drop(["key", "Focus", "Category", "Equipment"], axis=1)
    else:
        return df.groupby("Focus").sample(ceil(n_exercises / 3)).sample(n_exercises).drop(["key", "Focus", "Category", "Equipment"], axis=1)

def create_table(df, difficulty_input):
    if difficulty_input == "Very Easy":
        df["Sets"] = 3
        df["Time(s)"] = 20
        df["Set Rest(s)"] = 10
        df["Rest(s)"] = 50
    elif difficulty_input == "Easy":
        df["Sets"] = 3
        df["Time(s)"] = 30
        df["Set Rest(s)"] = 10
        df["Rest(s)"] = 50
    elif difficulty_input == "Moderate":
        df["Sets"] = 3
        df["Time(s)"] = 30
        df["Set Rest(s)"] = 10
        df["Rest(s)"] = 40
    elif difficulty_input == "Hard":
        df["Sets"] = 4
        df["Time(s)"] = 30
        df["Set Rest(s)"] = 10
        df["Rest(s)"] = 40
    else:
        df["Sets"] = 4
        df["Time(s)"] = 40
        df["Set Rest(s)"] = 10
        df["Rest(s)"] = 50
    return df


