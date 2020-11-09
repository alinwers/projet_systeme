from flask import Flask, render_template,request
import json, pandas as pd
from math import trunc
from numpy import isnan


def truncate(nb,digits):
    powerOfTen=10**digits
    return trunc(nb*powerOfTen)/powerOfTen

app = Flask(__name__)

jsonFile = open("static/database.json","r")
db = pd.read_json(jsonFile)
records = db.to_dict('records')
colNames = db.columns.values
#displayedColNames = ["Host Name","Planet Letter","Planet Name","Discovery Method","Controversial Flag","Number of Planets in System","Orbital Period [days]"
# ,"Orbit Semi-Major Axis [au]","Eccentricity","Inclination [deg]","Planet Mass or M*sin(i) [Jupiter Mass]","Planet Mass or M*sin(i) Provenance",
# "Planet Radius [Jupiter radii]","Planet Density [g/cm**3]","TTV Flag","Kepler Field Flag","K2 Mission Flag","Number of Notes","RA [sexagesimal]",
# "Dec [sexagesimal]","Distance [pc]","Gaia Distance [pc]","Optical Magnitude [mag]","Optical Magnitude Band","G-band (Gaia) [mag]","Effective Temperature [K]",
# "Stellar Mass [Solar mass]","Stellar Radius [Solar radii]","Date of Last Update","Discovery Facility"]

for i in range(0, len(records)):
    for key in records[i]:
        if isinstance(records[i][key], float) and str(records[i][key]) != "nan":
            records[i][key] = truncate(records[i][key], 6)

colTypes=[]
for col in colNames:
    for row in records:
        if row[col]!="nan":
            colTypes.append(type(row[col]).__name__)
            break
colTypes[31]="str" #to avoid NoneType


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("database.json")

@app.route("/catalog/")
def catalog():
    return render_template("catalog.html",records=records,colNames=colNames)

@app.route("/catalog/search/",methods=["GET","POST"])
def search():
    formData = request.args
    searchInput = formData["searchInput"]
    colName = formData["colName"]
    comparator = formData["comparator"]
    searchedRecords = []
    colType = colTypes[list(colNames).index(colName)]
    
    if colType=="int":
        searchInput=int(searchInput)
        for record in records:
            observedValue=record[colName]
            if str(observedValue)!="nan":
                if searchInput==observedValue:
                    searchedRecords.append(record)

    elif colType=="float":
        searchInput=float(searchInput)
        for record in records:
            observedValue=record[colName]
            if str(observedValue)!="nan":
                nbDecimales=str(searchInput)[::-1].find('.')
                if searchInput==truncate(observedValue,nbDecimales):
                    searchedRecords.append(record)
                    
    elif colType=="str":
        for record in records:
            if searchInput in record[colName]:
                searchedRecords.append(record)
                
    return render_template("catalog.html",records=searchedRecords,colNames=colNames)

@app.route("/record/")
def record():
    return "record"

@app.route("/graph/")
def graph():
    return render_template("graph.html")
