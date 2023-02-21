from flask import Flask, render_template, request
import pandas as pd
from math import ceil
from utils import aws_authenticate, dynamo_to_df, num_exercises

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
        df_new = df.groupby("Focus").sample(ceil(n_exercises / 3)).sample(n_exercises).drop("key", axis=1)
        return render_template("create.html", df=df_new)
    else:
        return render_template("create.html", df=pd.DataFrame())

if __name__ == "__main__":
    app.run(debug=True)