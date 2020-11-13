from flask import Flask, render_template,request
from pandas import read_json
from json import dumps
from math import trunc
from numpy import isnan
from init_db import init_db

def truncate(nb,digits):
    powerOfTen=10**digits
    return trunc(nb*powerOfTen)/powerOfTen

def loadJson():
    try:
        jsonFile = open("static/database.json","r")
    except IOError:
        print("JSON file not found")
    db = read_json(jsonFile)     #dataframe object
    jsonFile.close()
    records = db.to_dict('records')
    colNames = db.columns.values
    
    for i in range(len(records)):
        for key in records[i]:
            if isinstance(records[i][key], float) and str(records[i][key]) != "nan":
                records[i][key] = truncate(records[i][key], 6)

    colTypes=[]
    for col in colNames:
        for row in records:
            if row[col]!="nan":
                typeStr = type(row[col]).__name__
                if typeStr=="NoneType":
                    colTypes.append("str")
                else:
                    colTypes.append(typeStr)
                break
    
    return records,colNames,colTypes  

def refreshDB(url):
    init_db(url)
    return loadJson()
     
def eqComp(searchInput,observedValue,digits):
    if observedValue==searchInput:
        return True
    return False

def aroundComp(searchInput,observedValue,digits):
    if round(observedValue,digits)==searchInput:
        return True
    return False

def truncatedToComp(searchInput,observedValue,digits):
    if truncate(observedValue,digits)==searchInput:
        return True
    return False

def supComp(searchInput,observedValue,digits):
    if observedValue>searchInput:
        return True
    return False

def infComp(searchInput,observedValue,digits):
    if observedValue<searchInput:
        return True
    return False

def supEqComp(searchInput,observedValue,digits):
    if observedValue>=searchInput:
        return True
    return False

def infEqComp(searchInput,observedValue,digits):
    if observedValue<=searchInput:
        return True
    return False

url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=json"

app = Flask(__name__)

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

records,colNames,colTypes=loadJson()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("database.json")

@app.route("/catalog/")
def catalog():
    return render_template("catalog.html",records=records,colNames=colNames,displayedColNames=displayedColNames,colTypes=dumps(colTypes))

@app.route("/catalog/search/",methods=["GET","POST"])
def search():
    formData = request.args
    searchInput = formData["searchInput"]
    colIndex = int(formData["colName"])
    comparator = formData["comparator"]
    searchedRecords = []
    colType = colTypes[colIndex]
    colName=colNames[colIndex]
    comparatorToComparison = {"=":eqComp,"≃":aroundComp,"truncated":truncatedToComp,">":supComp,"<":infComp,">=":supEqComp,"<=":infEqComp}
    
    if colType=="str":
        for record in records:
            if searchInput in record[colName]:
                searchedRecords.append(record)
    else:
        if colType=="int":
            searchInput=int(searchInput)
            digits=0
        elif colType=="float":
            searchInput=float(searchInput)
            digits=str(searchInput)[::-1].find('.')
            
        for record in records:
            observedValue=record[colName]
            if str(observedValue)!="nan" and comparatorToComparison[comparator](searchInput,observedValue,digits):
                searchedRecords.append(record)
        
    return render_template("catalog.html",records=searchedRecords,colNames=colNames,displayedColNames=displayedColNames,colTypes=dumps(colTypes))

@app.route("/record/<index>")
def record(index):
    index=int(index)
    record=records[index]
    return render_template("record.html",record=record,isnan=isnan)

@app.route("/refresh/")
def refresh():
    global records,colNames,colTypes
    records,colNames,colTypes = refreshDB(url)
    return render_template("home.html")

@app.route("/graph/")
def graph():
    return render_template("graph.html")

