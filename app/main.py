from flask import Flask, render_template, request
import pandas as pd
from utils import aws_authenticate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_workout():
    if request.method == "POST":
        table = aws_authenticate("workout-exercises")
        return table.get_item(Key={"key": "key1"})
    else:
        return render_template("base.html")
