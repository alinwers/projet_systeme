from flask import Flask, render_template
import json, pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("database.json")

@app.route("/catalogue/")
def catalogue():
    db = pd.read_json("http://127.0.0.1:5000/api/data")
    temp = db.to_dict('records')
    columnNames = db.columns.values
    return render_template("catalog.html", records=temp, colnames=columnNames)

@app.route("/graph/")
def graph():
    return render_template("graph.html")