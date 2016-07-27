import json
import requests
import md5
import fileinput
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, configFileName

config = configFile(sys.argv);
configfilename = configFileName(sys.argv);
#######Generate Apikeys
m = md5.new()
m.update("%s" %(config['admin_org_password']))
md5_org_pwd =  m.hexdigest()
m = md5.new()
m.update("%s" %(config['admin_set_password']))
md5_set_pwd =  m.hexdigest()
stdurl_noapikey = 'https://%s/client/api?response=%s&' %(config['host'], config['response'])

s = requests.session()

### using "password" as text directly works for 1.4.1 build and onword
payload = {'command': 'login', 'username': 'admin', 'password': config['admin_set_password'], 'domain': '/', 'response': 'json'}

### using md5sum of "password" works for 1.4.0 buils and downword
#payload = {'command': 'login', 'username': 'admin', 'password': md5_set_pwd, 'domain': '/', 'response': 'json'}

### First time login
r = s.post(stdurl_noapikey, verify=False, data=payload)


### List userid
querystring = 'command=listUsers'
r = s.get(stdurl_noapikey+querystring, verify=False)
data = json.loads(r.text)
users = data["listusersresponse"]["user"]
existingApikey = "%s" %(config["apikey"])
for user in users:
    if user['username'] == "admin":
        user_id = user['id']
        apikey = user['apikey']

print apikey

for line in fileinput.FileInput('%s' %(configfilename),inplace=1):
    line = line.replace(existingApikey,apikey)
    print line,

#############Apikey Generated
