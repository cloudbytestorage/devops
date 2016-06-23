import json
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, filesave1

config = configFile(sys.argv);
stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])

### To list number of  Nodes
querycommand = 'command=listController'
resp_listController= sendrequest(stdurl,querycommand)
filesave("logs/CurrentNodes.txt","w",resp_listController) 
data = json.loads(resp_listController.text)
#version = data["listControllerResponse"]["version"]
controllers = data["listControllerResponse"]["controller"]
for controller in controllers:
    version = controller['version']
    break

filesave1("installed_version", "w", version)

print "Installed Version= ", version 
