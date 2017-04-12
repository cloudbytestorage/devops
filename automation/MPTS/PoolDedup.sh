#!/bin/sh
python PoolDedup.py dedup.txt on
python PoolDedupExecution.py dedup.txt nfs P 20.10.32.11 on
python PoolDedup.py dedup.txt off
python PoolDedupExecution.py dedup.txt nfs P 20.10.32.11 off
python PoolDedup.py dedup.txt on
