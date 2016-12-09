#!/bin/sh
python createISCSIInitiatorGroup.py dedup.txt 20.10.48.5
python createIscsiAuthGroup.py dedup.txt
python IscsiSecurityExecution.py dedup.txt
python IscsiNegativeSecurityExecution.py dedup.txt
