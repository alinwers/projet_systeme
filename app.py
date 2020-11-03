from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("database.json")

@app.route("/catalogue/")
def catalogue():
    return render_template("catalog.html")

@app.route("/graph/")
def graph():
    return render_template("graph.html")
