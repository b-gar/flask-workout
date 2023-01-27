from flask import Flask, render_template, request
import pandas as pd
from google.cloud import bigquery
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_workout():
    if request.method == "POST":
        try:
            secret = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            return secret[0]
        except Exception as e:
            return e
        # table_id = "flask-workout.workout.exercises"
        # query = f"""
        #     SELECT exercise, category
        #     FROM {table_id}
        #     WHERE
        #     type = 'Kettlebell';
        #     """
        # query_job = client.query(query)
        # df = query_job.result().to_dataframe()
        # return df.head()
    else:
        return render_template("base.html")
