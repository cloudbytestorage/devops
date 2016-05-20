##### pseudo code for p5 cython test case

##### STEP 1
- ssh to 20.10.48.140 (p5/p6 box)
- login to jail which is under test
- remove the disabledlockd file
- verify the removal
- restart lockd
- exit the ssh connection
- continue on success else exit

##### STEP 2
- ssh to 20.10.112.21 (cython)
- trigger the execution of test cases
- exit the ssh connection
- continue on success else exit

##### STEP 3
- after an interval
- ssh to 20.10.112.21 (cython)
- verify the output of the test cases
- exit the ssh connection
- retry if run is in progress

##### STEP 4
- ssh to 20.10.48.140 (p5/p6 box)
- login to a specific jail
- add the disabledlockd file
- verify the presence of file
- restart lockd
- exit the ssh connection

##### STEP 5
- report failure or success
