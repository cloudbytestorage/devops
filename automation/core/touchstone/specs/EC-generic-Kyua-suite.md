##### pseudo code for any Kyua automation test case
##### This is test suite for verifying stability of the kernel.

##### STEP 1
- ssh to machine where we want to run these test cases (20.10.48.140). (p5/p6/release* box)
- install the pkg package for installing kyua test suite.
- install kyua package.
- verify kyua pkg has been installed.

##### STEP 2
- run kyua test cases.
- convert the results in junit compatible form.

##### STEP 3
- check if the junit xml file has been generated.
- copy the xml file to jenkins machine.
- run jenkins job.
- The results will get published as html dashboard.

##### STEP 4
- report failure or success
