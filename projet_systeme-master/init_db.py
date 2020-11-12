import json
from urllib.request import urlopen
import os, platform


url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=json"
if (not os.path.exists(".\static\database.json") and platform.system() == "Windows") or \
    (not os.path.exists("./static/database.json") and platform.system() == "Linux"):

    data = urlopen(url) # it's a file like object and works just like a file

    for line in data:
        decoded_data = line.decode("utf-8")
        open('database.json', 'a').write(decoded_data)
        
    if platform.system() == "Linux":
        os.popen("mv ./database.json ./static/")
    elif platform.system() == "Windows":
        os.popen(r"move .\database.json .\static\database.json")  #r for a row string