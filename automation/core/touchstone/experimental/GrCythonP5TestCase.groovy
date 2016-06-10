package com.automaton.experimental

@Grab('com.aestasit.infrastructure.sshoogr:sshoogr:0.9.25')
@Grab('com.cb:touchstone:0.0.2')

import com.automaton.launcher.AutomatonSpecsRunner;
import static groovy.json.JsonOutput.prettyPrint
import static groovy.json.JsonOutput.toJson

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

def Map container = [:]

def automaton = {
    
    ssh {
        
        to(elastistorMacOpts, 'Remove lock file @ elastistor')
        
        run('rm /tenants/f7ec4eb1486c3aa6a4bafaa12d93e084/PoolRaidz1/Account1TSM1/amit.has')        
    }

    ssh('task-002') {
        
        to(elastistorMacOpts, 'Restart lockd service @ elastistor')
        
        run('restart lockd')
        
        storeAs('restart-lock.output', container)
    }

    ssh {
        
        to(cythonMacOpts, 'Trigger cython test cases')
        
        run('cd /cthon04 && pwd')
        
        storeAs('cython-trigger.output', container)

        then('is it cthon05', { contains("cthon05") ? "It contains cthon05." : "It does not have cthon05." })

        then('is numeric', { isNumber() ? "It is a number." : "It is a string." })

        then('is empty', { isEmpty() ? "'$it' is an empty thing." : "'$it' is a filled stuff." })
        
        storeAs('cython-trigger.output2', container)        
    }

    ssh([repeat: 3, interval: 4000]) {
        
        to(cythonMacOpts, 'Verify cython test cases by sampling at periodic intervals')
        
        run('cd /cthon04 && cat abc.out')
        
        storeAs('cython-sampler.output', container)
        
        repeatIf({ contains("Nooop such file") })
        
    }

    ssh {
        
        to(elastistorMacOpts, 'Enable lock file @ elastistor')
        
        run('touch /tenants/f7ec4eb1486c3aa6a4bafaa12d93e084/PoolRaidz1/Account1TSM1/amit.has')
        
        storeAs('enable-lock.output', container)
    }

    ssh(!container?.get('enable-lock.output')?.contains('No such file')) {
        
        to(elastistorMacOpts, 'Restart lockd service @ elastistor')
        
        run('restart lockd')
    }
}

AutomatonSpecsRunner runner = new AutomatonSpecsRunner()

println prettyPrint(toJson(runner.specification(automaton)))
