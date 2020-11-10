from flask import Flask, render_template,request
import json, pandas as pd
from math import trunc
from numpy import isnan


def truncate(nb,digits):
    powerOfTen=10**digits
    return trunc(nb*powerOfTen)/powerOfTen

app = Flask(__name__)

try:
    jsonFile = open("static/database.json","r")
    db = pd.read_json(jsonFile)     #dataframe object
    records = db.to_dict('records')
    colNames = db.columns.values
    displayedColNames = ["Host Name", "Planet Letter", "Planet Name", "Discovery Method", "Controversial Flag", "Number of Planets in System", "Orbital Period [days]",
    "Orbital Period Upper Unc. [days]", "Orbital Period Lower Unc. [days]", "Orbital Period Limit Flag", "Orbital Period Measurements", "Orbit Semi-Major Axis [au]",
    "Orbit Semi-Major Axis Upper Unc. [au]", "Orbit Semi-Major Axis Lower Unc. [au]", "Orbit Semi-Major Axis Limit Flag", "Orbit Semi-Major Axis Measurements","Eccentricity",
    "Eccentricity Upper Unc.", "Eccentricity Lower Unc.", "Eccentricity Limit Flag", "Eccentricity Measurements", "Inclination [deg]", "Inclination Upper Unc. [deg]",
    "Inclination Lower Unc. [deg]", "Inclination Limit Flag", "Inclination Measurements", "Planet Mass or M*sin(i) [Jupiter mass]", "Planet Mass or M*sin(i) Upper Unc. [Jupiter mass]",
    "Planet Mass or M*sin(i) Lower Unc. [Jupiter mass]", "Planet Mass or M*sin(i) Limit Flag", "Planet Mass Measurements", "Planet Mass or M*sin(i) Provenance",
    "Planet Radius [Jupiter radii]", "Planet Radius Upper Unc. [Jupiter radii]", "Planet Radius Lower Unc. [Jupiter radii]", "Planet Radius Limit Flag", "Planet Radius Measurements",
    "Planet Density [g/cm**3]", "Planet Density Upper Unc. [g/cm**3]", "Planet Density Lower Unc. [g/cm**3]", "Planet Density Limit Flag", "Planet Density Measurements", "TTV Flag",
    "Kepler Field Flag", "K2 Mission Flag", "RA [sexagesimal]", "Dec [sexagesimal]", "RA [decimal degrees]", "RA Error [decimal degrees]", "Dec [decimal degrees]",
    "Dec Error [decimal degrees]", "Stellar Position Measurements", "Dec [decimal degrees]", "Distance Upper Unc. [pc]", "Distance Lower Unc. [pc]", "Distance Limit Flag",
    "Distance Measurements", "Optical Magnitude [mag]", "Optical Magnitude Unc. [mag]", "Optical Magnitude Limit Flag", "Optical Magnitude Band", "G-band (Gaia) [mag]",
    "G-band (Gaia) Unc. [mag]", "G-band (Gaia) Limit Flag", "Effective Temperature [K]", "Effective Temperature Upper Unc. [K]", "Effective Temperature Lower Unc. [K]",
    "Effective Temperature Limit Flag", "Effective Temperature Measurements", "Stellar Mass [Solar mass]", "Stellar Mass Upper Unc. [Solar mass]", "Stellar Mass Lower Unc. [Solar mass]",
    "Stellar Mass Limit Flag", "Stellar Mass Measurements", "Stellar Radius [Solar radii]", "Stellar Radius Upper Unc. [Solar radii]", "Stellar Radius Lower Unc. [Solar radii]",
    "Stellar Radius Limit Flag", "Stellar Radius Measurements", "Number of Notes", "Date of Last Update", "Discovery Facility"]

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
except IOError:
    print("JSON file not found")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("database.json")

@app.route("/catalog/")
def catalog():
    return render_template("catalog.html",records=records,colNames=colNames, displayedColNames=displayedColNames)

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
                
    return render_template("catalog.html",records=searchedRecords,colNames=colNames, displayedColNames=displayedColNames)

@app.route("/record/")
def record():
    return "record"

@app.route("/graph/")
def graph():
    return render_template("graph.html")
