package com.automaton.experimental

@Grab('com.aestasit.infrastructure.sshoogr:sshoogr:0.9.25')
@Grab('com.cb:touchstone:0.0.2')

import com.automaton.GrSshAutomaton

def cythonMacOpts = {
    defaultHost = '20.10.112.21'
    defaultUser = 'root'
    defaultPassword = 'test123'
}

def elastistorMacOpts = {
    defaultHost = '20.10.48.140'
    defaultUser = 'root'
    defaultPassword = 'test'
}


// TASK 1 - Remove lock file @ elastistor
def task1 = new GrSshAutomaton()
task1.of(elastistorMacOpts, 'remove lock', 'rm /tenants/f7ec4eb1486c3aa6a4bafaa12d93e084/PoolRaidz1/Account1TSM1/amit.has')
println task1.trigger()

// TASK 2 - Restart lockd @ elastistor
def task2 = new GrSshAutomaton()
task2.of(elastistorMacOpts, 'restart lockd service', 'restart lockd')
println task2.trigger()

// TASK 3 - Trigger execution of cython test cases
def task3 = new GrSshAutomaton()
task3.of(cythonMacOpts, 'trigger cython test cases', 'cd /cthon04 && pwd')
task3.map('verify', {String it ->
    it.contains("cthon05") ? "true" : "false"
})
task3.map('verify once again', {String it ->
    it ? "yeah" : "naah"
})
task3.map('last verification', {String it ->
    it == "yoho" ? "yoho" : "nono"
})
println task3.trigger()

// TASK 4 - Verify output of cython test cases by sampling at periodic intervals
def task4 = new GrSshAutomaton()
task4.of(cythonMacOpts, 'verify cython test cases', 'cd /cthon04 && cat abc.out')
println task4.trigger()

// TASK 5 - Enable lock file & restart lockd @ elastistor
def task5 = new GrSshAutomaton()
task5.of(elastistorMacOpts, 'enable lock', 'touch /tenants/f7ec4eb1486c3aa6a4bafaa12d93e084/PoolRaidz1/Account1TSM1/amit.has')
println task5.trigger()

// TASK 6 - Restart lockd @ elastistor
def task6 = new GrSshAutomaton()
task6.of(elastistorMacOpts, 'restart lockd service', 'restart lockd')
println task6.trigger()

