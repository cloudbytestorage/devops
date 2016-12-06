# cleaning results file
echo > results/result.csv

# CLEAN THE SYSTEM
python cleanup.py conf.txt

# RUNNING STANDARD WORK LOAD WITH NFS
python AMSx-WLAx-SWxx-GENx-VDBx-TC_WORKLOAD_SIMULATION_TEST.py conf.txt nfs

# CLEAN THE SYSTEM
python cleanup.py conf.txt

# RUNNING STANDARD WORK LOAD WITH ISCSI
python AMSx-WLAx-SWxx-GENx-VDBx-TC_WORKLOAD_SIMULATION_TEST.py conf.txt iscsi
