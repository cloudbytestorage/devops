python Compression.py dedup.txt all on
python CompressionExecution.py dedup.txt all on 20.10.48.140 test
python delete.py dedup.txt iscsi
sleep 5
python ISCSIVolume.py dedup.txt
python setISCSIInitiatorGroup.py dedup.txt
python Compression.py dedup.txt all off
python CompressionExecution.py dedup.txt all off 20.10.48.140 test
python Compression.py dedup.txt all on
