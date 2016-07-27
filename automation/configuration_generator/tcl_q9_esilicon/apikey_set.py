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
## Commenting because,now we are using password as text(1.4.1)
#payload = {'command': 'login', 'username': 'admin', 'password': md5_set_pwd, 'domain': '/', 'response': 'json'}
payload = {'command': 'login', 'username': 'admin', 'password': config['admin_set_password'], 'domain': '/', 'response': 'json'}

### First time login
r = s.post(stdurl_noapikey, verify=False, data=payload)


### List userid
querystring = 'command=listUsers'
r = s.get(stdurl_noapikey+querystring, verify=False)
data = json.loads(r.text)
users = data["listusersresponse"]["user"]
for user in users:
    if user['username'] == "admin":
        user_id = user['id']

### Update User ID
querystring = 'command=updateUser&id=%s&password=%s&firstname=%s&lastname=%s&email=%s&mobileno=%s' %(user_id, md5_set_pwd, config['firstname'], config['lastname'], config['email'], config['mobile'])
r = s.get(stdurl_noapikey+querystring, verify=False)

### Update Email ID
querystring = 'command=updateConfiguration&name=alert.email.addresses&value=%s' %(config['email'])
r = s.get(stdurl_noapikey+querystring, verify=False)

### Generate ApiKey
existingApikey = "%s" %(config["apikey"])
querystring = 'command=registerUserKeys&id=%s' %(user_id)
r = s.get(stdurl_noapikey+querystring, verify=False)
data = json.loads(r.text)
apikey = data["registeruserkeysresponse"]["userkeys"]["apikey"]
print existingApikey
print apikey
for line in fileinput.FileInput('%s' %(configfilename), inplace=1):
    line = line.replace(existingApikey, apikey)
    print line,

#############Apikey Generated
