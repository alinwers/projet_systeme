from urllib.request import urlopen
import os, platform

def init_db(url):
    data = urlopen(url) # it's a file like object and works just like a file
    
    for line in data:
        decoded_data = line.decode("utf-8")
        open('database.json', 'a').write(decoded_data)
        
    if platform.system() == "Linux":
        if os.path.isfile("./static/database.json"):
            os.popen("rm ./static/database.json").read()
        os.popen("mv ./database.json ./static/").read()
    elif platform.system() == "Windows":
        if os.path.isfile(r".\static\database.json"):
            os.popen(r"del .\static\database.json").read()
        os.popen(r"move .\database.json .\static\database.json").read()  #r for a row string
        