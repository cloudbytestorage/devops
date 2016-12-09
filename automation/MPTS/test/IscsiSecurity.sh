#!/bin/sh
python createISCSIInitiatorGroup.py dedup.txt
python createIscsiAuthGroup.py dedup.txt
python IscsiSecurityExecution.py dedup.txt
python IscsiNegativeSecurityExecution.py dedup.txt
