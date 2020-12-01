from urllib.request import urlopen
import os, platform

#Webscrap data from the specified url and store it in the database.json file
def init_db(url):
    data = urlopen(url)
    
    for line in data:
        decoded_data = line.decode("utf-8")
        open('database.json', 'a').write(decoded_data)
        
    #The older database.json is deleted and the newer is moved into the static subfolder using shell commands
    if platform.system() == "Linux":
        if os.path.isfile("./static/database.json"):
            os.popen("rm ./static/database.json").read()
        os.popen("mv ./database.json ./static/").read()
    elif platform.system() == "Windows":
        if os.path.isfile(r".\static\database.json"):
            os.popen(r"del .\static\database.json").read()
        os.popen(r"move .\database.json .\static\database.json").read()
        