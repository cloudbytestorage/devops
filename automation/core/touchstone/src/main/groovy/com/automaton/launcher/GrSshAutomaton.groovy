package com.automaton.launcher

import com.aestasit.infrastructure.ssh.SshOptions
import com.aestasit.infrastructure.ssh.dsl.CommandOutput
import com.aestasit.infrastructure.ssh.dsl.SshDslEngine
import com.aestasit.infrastructure.ssh.log.SysOutEventLogger
import com.automaton.dsl.AutomatonSSHTask;

class GrSshAutomaton {
    
    private Closure<AutomatonSSHTask> task = null

    private Map<String, Closure> operations = [:]

    private Map<String, String> results = [:]

    def of(Closure specificOpts, String taskName, String cmd){

        SshDslEngine sshEngine = buildSshEngine(specificOpts)

        task = {
            doSsh(sshEngine, taskName, cmd)
        }
    }

    def map(String name, Closure operation){
        operations.put(name, operation)
    }

    Map trigger(){
        AutomatonSSHTask automatonTask = task()
        def cmdOutput = automatonTask.cmdOutput

        results.put('task', automatonTask.name)
        results.put('command', automatonTask.command)
        results.put('result', cmdOutput.output)
        results.put('error', cmdOutput.exception?: null)
        results.put('exit_status', cmdOutput.exitStatus)
        results.put('latency', automatonTask.timeTaken)

        String operationalOutput = cmdOutput.output
        
        operations?.each {
            operationalOutput = it.value.call(operationalOutput)
            results.put(it.key, operationalOutput)
        }

        results
    }

    private buildSshEngine(Closure sshOptions){
        def atmSshOptions = new SshOptions()

        // set defaults
        atmSshOptions.with {

            logger = new SysOutEventLogger()

            trustUnknownHosts = true

            execOptions.with {
                showCommand = false
                showOutput = false
                failOnError = false
            }
        }

        // mutate with user specified
        atmSshOptions.with sshOptions

        SshDslEngine sshEngine = new SshDslEngine(atmSshOptions)
    }

    private AutomatonSSHTask doSsh(SshDslEngine sslEngine, String taskName, String cmd){
        CommandOutput cmdOutput = null
        sslEngine.remoteSession({cmdOutput = exec(cmd)})

        def task = new AutomatonSSHTask(
                name: taskName,
                command: cmd,
                timeTaken: 'x secs',
                threadName: Thread.currentThread().name,
                cmdOutput: cmdOutput)

        task
    }

}
