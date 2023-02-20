from flask import Flask, render_template, request
import pandas as pd
from utils import aws_authenticate, dynamo_to_df, num_exercises, num_seconds

app = Flask(__name__)

table = aws_authenticate("workout-exercises")
df = dynamo_to_df(table)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        n_exercises = num_exercises(request.form.get("difficulty"), request.form.get("duration"))
        n_seconds = num_seconds(request.form.get("difficulty"))
        return render_template("create.html", difficulty=n_exercises, equipment=n_seconds, duration="")
    else:
        return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)