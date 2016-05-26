package com.automaton.dsl

import com.aestasit.infrastructure.ssh.SshOptions
import com.aestasit.infrastructure.ssh.dsl.CommandOutput
import com.aestasit.infrastructure.ssh.dsl.SshDslEngine
import com.aestasit.infrastructure.ssh.log.SysOutEventLogger
import com.automaton.utils.BasicUtils

/**
 * The class that enables lazy execution of ssh command & 
 * the corresponding map operations.
 * 
 * <p>
 * NOTE - This class is a wrapper over sshoogr-0.9.25 library. 
 * 
 * @author amit.das@cloudbyte.com
 *
 */
class GrSsh {

    private Closure<AutomatonSSHTask> task = null

    private Map<String, Closure> operations = [:]

    private Map<String, String> results = [:]

    private final String ERR = "ERROR"

    /**
     * This will build the ssh command that needs to be executed
     * at a later point in time.
     * 
     */
    def of(Closure connOpts, String taskName, String cmd){

        assert connOpts != null, "Nil connection options provided."
        assert taskName != null, "Nil task name provided."
        assert cmd != null, "Nil command provided."

        SshDslEngine sshEngine = buildSshEngine(connOpts)

        // build the function as a closure to be executed later
        task = {
            doSsh(sshEngine, taskName, cmd)
        }
    }

    /**
     * Save the operations to be executed later.
     * These operations will be invoked on the output of 
     * just executed ssh command.
     * 
     */
    def map(String name, Closure func){

        assert name != null, "Nil function name provided."
        assert func != null, "Nil function provided."

        operations.put(name, func)
    }

    /**
     * This needs to be invoked by the caller to start 
     * execution of ssh & the series of map operations.
     * 
     * @return the results
     */
    Map trigger(){
        // actual execution of ssh
        AutomatonSSHTask automatonTask = task()
        def cmdOutput = automatonTask.cmdOutput

        results.put('task', automatonTask.name)
        results.put('command', automatonTask.command)
        results.put('result', cmdOutput.output)
        results.put('error', cmdOutput.exception?: "None")
        results.put('exit_status', cmdOutput.exitStatus)
        results.put('start_time', 'x:y:z')
        results.put('end_time', 'x1:y1:z1')
        results.put('latency', automatonTask.timeTaken)

        String operationalOutput = cmdOutput.output

        operations?.each {
            operationalOutput = operationalOutput ?
                    BasicUtils.instance.runClosure(it.value, operationalOutput, operationalOutput) :
                    null

            operationalOutput ?
                    results.put(it.key, operationalOutput) :
                    results.put(it.key, "Could not run function on nil value.")

        }

        results
    }

    /**
     * Stuff necessary to build the ssh engine on which ssh command 
     * will be executed.
     * 
     * @param sshOptions
     * @return
     */
    private SshDslEngine buildSshEngine(Closure connOpts){
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

        // mutate with connection options
        atmSshOptions.with connOpts

        SshDslEngine sshEngine = new SshDslEngine(atmSshOptions)
    }

    /**
     * Actual execution of ssh command!!!
     * 
     * @param sslEngine
     * @param taskName
     * @param cmd
     * @return
     */
    private AutomatonSSHTask doSsh(SshDslEngine sshEngine, String taskName, String cmd){
        CommandOutput cmdOutput = null
        sshEngine.remoteSession({cmdOutput = exec(cmd)})

        def task = new AutomatonSSHTask(
                name: taskName,
                command: cmd,
                timeTaken: 'x secs',
                threadName: Thread.currentThread().name,
                cmdOutput: cmdOutput)

        task
    }

}
