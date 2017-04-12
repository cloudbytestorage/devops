#!/bin/sh
python Compression.py dedup.txt nfs on
python CompressionExecution.py dedup.txt nfs on 20.10.32.11 test
python Compression.py dedup.txt nfs off
python CompressionExecution.py dedup.txt nfs off 20.10.32.11 test
python Compression.py dedup.txt nfs on
