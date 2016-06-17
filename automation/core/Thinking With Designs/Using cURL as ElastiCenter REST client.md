### Using command line as REST client to ElastiCenter

##### cURL
- How to learn cURL ?
  - curl --help
  - https://curl.haxx.se/docs/manual.html
- [cURL & stderr redirections](http://unix.stackexchange.com/questions/166359/how-to-grep-the-output-of-curl)
- [cURL & Unix pipes](http://serverfault.com/questions/313599/how-do-i-pipe-the-output-of-uptime-df-to-curl)
  - echo "time=`uptime`" | curl -d @- http://URL
    - -d option in curl with a **@-** argument to accept input from a pipe
    - backticks imply that the enclosed command will be executed
-


##### cURL as REST client to ElastiCenter
- ElastiCenter - 20.10.112.70  
- Client Environment
  - Git Bash on Windows 7
  - $ curl --version

```
curl 7.30.0 (i386-pc-win32) libcurl/7.30.0 OpenSSL/0.9.8x zlib/1.2.7
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smtp smtps telnet tftp
Features: AsynchDNS GSS-Negotiate IPv6 Largefile NTLM SPNEGO SSL SSPI libz
```

- **Getting Started - Use of -k is a must to ignore security**

```
$ curl https://20.10.112.70/client/api?command=listTsm -k

<?xml version="1.0" encoding="ISO-8859-1"?>
  <listTsmResponse cloud-stack-version="1.4.0.897">
  <errorcode>401</errorcode>
  <errortext>unable to verify user credentials and/or request signature</errortext>
  <licensetype>trial</licensetype>
</listTsmResponse>

```

- **Pass query parameters via -d**
  - **use of -G is a must with -d as EC is pure GET !!!**

```
$ curl https://20.10.112.70/client/api -d 'command=listTsm' -G -k

<?xml version="1.0" encoding="ISO-8859-1"?>
  <listTsmResponse cloud-stack-version="1.4.0.897">
  <errorcode>401</errorcode>
  <errortext>unable to verify user credentials and/or request signature</errortext>
  <licensetype>trial</licensetype>
</listTsmResponse>

```

- **Pass multiple query parameters**

```
$ curl https://20.10.112.70/client/api -d 'command=listTsm' -d 'response=json' -G -k

{ "listTsmResponse" : {
  "uuidList": [],
  "errorcode": 401,
  "errortext": "unable to verify user credentials and/or request signature",
  "licensetype": "trial"
} }

```


- **What to do with password ?**
  - NOTE - Store api key in a file to avoid repetition.

```
amit@CLOUDBYTE-AMIT ~
$ echo apiKey=OjvktW98EGI6QkGicGh40Pd4FevWXo2jLQePg1fSMx4QXwQedR5Xkrm_yphF1Hk_63kpOfwjvAeX7YQHoajevA > ecapi

amit@CLOUDBYTE-AMIT ~
$ cat ecapi
apiKey=OjvktW98EGI6QkGicGh40Pd4FevWXo2jLQePg1fSMx4QXwQedR5Xkrm_yphF1Hk_63kpOfwjvAeX7YQHoajevA

```

- **I want data !!**
  - Example of using listTsm command

```
amit@CLOUDBYTE-AMIT ~
$ curl https://20.10.112.70/client/api -d 'command=listTsm' -d 'response=json' -d @ecapi -G -k

{ "listTsmResponse" : { "count":2 ,"listTsm" : [  {
  "id": "d9a86229-9698-382a-a240-ff26b489a1f0",
  "simpleid": 146,
  "name": "VSMTEST2",
  "ipaddress": "20.10.39.239",
  "accountname": "ACC1",
  "sitename": "SITE1",
  "clustername": "HAG1",
  ....
  ....
  "totalprovisionquota": "24117248",
  "haNodeStatus": "Available",
  "ispooltakeoveronpartialfailure": true,
  "cifsauthentication": "user",
  "minrecommendedvolblocksize": 0
} ] } }

```

- **Can we reduce verbosity ?**
 - NOTE - Store the URL in a file as shown below & understood by cURL.

```
amit@CLOUDBYTE-AMIT ~
$ echo "url=https://20.10.112.70/client/api" > ec112.70

amit@CLOUDBYTE-AMIT ~
$ cat ec112.70
url=https://20.10.112.70/client/api

```

- **Show me the terse syntax now!!!**
  - NOTE - Use cURL with -K option.  

```
amit@CLOUDBYTE-AMIT ~
$ curl -K ec112.70 -d 'command=listTsm' -d 'response=json' -d @ecapi -G -k

{ "listTsmResponse" : { "count":1 ,"listTsm" : [  {
  "id": "d9a86229-9698-382a-a240-ff26b489a1f0",
  "simpleid": 146,
  "name": "VSMTEST2",
  "ipaddress": "20.10.39.239",
  "accountname": "ACC1",
  "sitename": "SITE1",
  "clustername": "HAG1",
  "controllerName": "NODE1",
  ...
  ...
  "qosgrouplist": [
    {
      "id": "23afe0f5-622c-3cda-bf38-bb62252d5704",
      "networkspeed": "0",
      "iops": "500",
      "latency": "15",
      "name": "QoS_SampleNFSVolACC1VSMTEST2",
      "memlimit": "0",
      "throughput": "0"
    }
  ]
} ] } }  

```

- **Can we limit the verboseness further ?**
  - NOTE - Put the common stuff in ecapi file itself.
  - NOTE - Let the URL stuff be present in ec112.70 file.

```
  $ cat ecapi
  apiKey=OjvktW98EGI6QkGicGh40Pd4FevWXo2jLQePg1fSMx4QXwQedR5Xkrm_yphF1Hk_63kpOfwjvAeX7YQHoajevA&response=json

  $ cat ec112.70
  url=https://20.10.112.70/client/api

```

  - NOTE - The quotes '' for providing value to -d seems optional.
  - Here we go. **The terse ever syntax !!!**

```

$ curl -K ec112.70 -d command=listTsm -d @ecapi -G -k

{ "listTsmResponse" : { "count":1 ,"listTsm" : [  {
  "id": "d9a86229-9698-382a-a240-ff26b489a1f0",
  "simpleid": 146,  
  ...
  ...
  "qosgrouplist": [
    {
      "id": "23afe0f5-622c-3cda-bf38-bb62252d5704",
      "networkspeed": "0",
      ...  
      "throughput": "0"
    }
  ]
} ] } }  

```

- **Can I use it in Unix pipes ?**
  - Yes.
  - NOTE - Redirect std err to std output & then use it in Unix pipes.

```
$ curl https://20.10.112.70/client/api -d 'command=listTsm' -d 'response=json' -G -k --stderr - | grep uuidList

  "uuidList": [],
```

  - Alternative & compact way to use the output from curl in Unix pipes
  - -s -> silent, i.e. do not show progress
  - -S -> show errors

```
$ curl -K ec112.70 -d command=listUserss -d @ecapi -G -k -s -S| awk '{print NR ": " $0}'
1: { "errorresponse" : {
2:   "uuidList": [],
3:   "errorcode": 432,
4:   "errortext": "The given command does not exist",
5:   "licensetype": "trial"
6: } }
```

- **Can I create a ElastiStor volume with such ease ?**
  - In other words, can we avoid resorting to programming for such complex tasks ?
  - Remember, this is the best of a complex REST client use-case w.r.t ElastiCenter.
  - Refer - create_volume in python (OpenStack cinder plugin for CloudByte)

| Task                           | REST Command           | Query Parameters       | Filter            |
| :-------------                 | :-------------         | :-------------         | :-------------    |
| Account ID from Account Name   | listAccount            | __                     | account name (m)  |
| List VSM details               | listTsm                | accountid              | VSM name (m)      |
| Add QOS group                  | addQosGroup            | name, tsmid, ..        | id                |
| Create Volume                  | createVolume           | datasetid, name, ..    | jobid             |
| Verify Job Result (repeat if)  | queryAsyncJobResult    | jobid                  | jobstatus         |
| Fetch volume id                | listFileSystem         | __                     | volume name (m)   |
| Fetch iscsi id                 | listVolumeiSCSIService | storageid              | volume id (m)     |
| Fetch initiator group id       | listiSCSIInitiator     | accountid              | name (m)          |
| Update iscsi service           | updateVolumeiSCSIService | id, igid, ..         | __                |



  - (m) refers to match, provided by user
  - .. indicates presence of more query parameters
  - __ indicates none
  - repeat if indicates the same task may be retried again & again


- Lets list down the json parser cli libraries that can help us in our effort:
  - [underscore-cli](https://github.com/ddopson/underscore-cli)
  - [json](http://trentm.com/json/)
  - [Lenses, Folds, and Traversals ](https://github.com/ekmett/lens)
  - [Lens Tutorial from School of Haskell](https://www.schoolofhaskell.com/school/to-infinity-and-beyond/pick-of-the-week/a-little-lens-starter-tutorial)
  - [jq](https://stedolan.github.io/jq/)


### Miscellaneous

##### Network & Speed Calculations
- How cURL does it ?

```
amit@CLOUDBYTE-AMIT ~
$ curl -L https://raw.githubusercontent.com/micha/resty/master/resty > resty
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  5651  100  5651    0     0   2683      0  0:00:02  0:00:02 --:--:--  2703

```
