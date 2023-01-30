from flask import Flask, render_template, request
import pandas as pd
from utils import google_authenticate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_workout():
    if request.method == "POST":

        client = google_authenticate()
        table_id = "flask-workout.workout.exercises"
        query = f"""
            SELECT exercise, category
            FROM {table_id}
            WHERE
            type = 'Kettlebell';
            """
        query_job = client.query(query)
        df = query_job.result().to_dataframe()
        return df.head().to_dict()
    else:
        return render_template("base.html")
