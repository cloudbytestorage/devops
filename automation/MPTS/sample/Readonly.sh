#!/bin/sh
python Readonly.py dedup.txt nfs false
python ReadonlyExecution.py dedup.txt nfs copy off
python Readonly.py dedup.txt nfs true
python ReadonlyExecution.py dedup.txt nfs delete on
python Readonly.py dedup.txt nfs false
python ReadonlyExecution.py dedup.txt nfs copy off
