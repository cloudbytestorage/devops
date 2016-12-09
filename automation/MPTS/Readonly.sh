#!/bin/sh
python Readonly.py dedup.txt all false
python ReadonlyExecution.py dedup.txt all copy off
python Readonly.py dedup.txt all true
python ReadonlyExecution.py dedup.txt all delete on
python Readonly.py dedup.txt all false
python ReadonlyExecution.py dedup.txt all delete off
