from flask import Flask, render_template, request, redirect
from flask_mail import Message
import pandas as pd
from utils import aws_authenticate, gmail_authenticate, dynamo_to_df, num_exercises, filter_exercises, create_table
from pathlib import Path

app = Flask(__name__)

# Authenticate to Gmail
mail = gmail_authenticate(app)

# Get Path to Save Table to
file_path = Path.cwd().joinpath("static")
file_name = "exercises.csv"

# Authenticate to AWS Table and Convert it to DF
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
        df_final.to_csv(file_path / file_name, index=False)
        return render_template("create.html", df=df_final)
    else:
        return render_template("create.html", df=pd.DataFrame())

@app.route("/share", methods=["GET", "POST"])
def share():
    if request.method == "POST":
        msg = Message(
            "Your Workout",
            recipients=[request.form.get("email")]
        )
        msg.body = "Thank you for using my site, your workout is attached!"
        with app.open_resource(file_path / file_name) as fp:
            msg.attach("workout.csv", "text/csv", fp.read())
        mail.send(msg)
        return redirect("/create")
    else:
        return render_template("share.html")

if __name__ == "__main__":
    app.run(debug=True)