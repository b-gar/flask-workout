from flask import Flask, render_template, request
import pandas as pd
from utils import aws_authenticate, dynamo_to_df, num_exercises, filter_exercises, create_table

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
        df_filtered = filter_exercises(df, request.form.get("equipment"), n_exercises)
        df_final = create_table(df_filtered, request.form.get("difficulty"))
        return render_template("create.html", df=df_final)
    else:
        return render_template("create.html", df=pd.DataFrame())

if __name__ == "__main__":
    app.run(debug=True)