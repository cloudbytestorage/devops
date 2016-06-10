package com.automaton.dsl

import com.aestasit.infrastructure.ssh.SshOptions
import com.aestasit.infrastructure.ssh.dsl.CommandOutput
import com.aestasit.infrastructure.ssh.dsl.SshDslEngine
import com.aestasit.infrastructure.ssh.log.SysOutEventLogger
import com.automaton.types.AutomatonSpecs
import com.automaton.types.SshSpecs
import com.automaton.utils.BasicUtils


/**
 * The class that enables lazy execution of ssh command & 
 * the corresponding post execute operations. This class can 
 * be considered as the core class for executing a command
 * over ssh. 
 * 
 * <p>
 * NOTE - This class is a dependent on sshoogr-0.9.25 library. 
 * 
 * @author amit.das@cloudbyte.com
 *
 */
class GrSsh implements AsErrHandler{

    private final String uuid

    private Closure<AutomatonSSHTask> theSshTask = null

    private Map<String, String> props = [:]

    private Map<String, Closure> operations = [:]

    private Map<String, String> results = [:]

    /**
     * Constructor that accepts a unique identifier.
     * 
     * @param uuid
     */
    GrSsh(String sshUuid){
        assert sshUuid != null, "Nil ssh uuid provided."

        props.put(AutomatonSpecs.uuid, sshUuid)
    }

    /**
     * Set the connection properties & task name.
     * 
     * @param conn
     * @param taskName
     * @return
     */
    def to(Closure conn, String taskName){
        of(conn, taskName, "Yet to provide the command")
    }

    /**
     * Set the command.
     *
     * @param conn
     * @param taskName
     * @return
     */
    def run(String cmd){
        assert cmd != null, "Nil command provided."

        props.put(SshSpecs.command, cmd)
    }

    /**
     * Save the operations to be executed later.
     * These operations will be invoked on the output of 
     * just executed ssh command.
     * 
     */
    def then(String name, Closure func){

        assert name != null, "Nil function name provided."
        assert func != null, "Nil function provided."

        operations.put(name, func)
    }

    /**
     * An operation that stores the current operational value 
     * at a point in time. This value can be referred to in future. 
     * <p>
     * Note - There might be several operations done on this value
     * after invoking this method.
     * 
     * @param key
     */
    def storeAs(String key, Map container){
        assert key != null, "Nil store key provided."

        operations.put(key, {
            container.put(key, it)
            it
        })
    }

    /**
     * Indicates whether a repeated invocation of similar instances 
     * is allowed or not. 
     * <p>
     * NOTE - The caller logic will exit or repeat the invocation 
     * after the specified delay. 
     * 
     * @param repeatCondition
     * @return
     */
    def repeatIf(Closure repeatCondition){
        assert repeatCondition != null, "Repeat condition not provided."

        operations.put(SshSpecs.allowRepeat, repeatCondition)
    }

    /**
     * This needs to be invoked by the caller to start 
     * execution of ssh & the series of map operations.
     * 
     * @return the results
     */
    Map trigger(){

        // actual execution of ssh
        AutomatonSSHTask automatonTask = theSshTask()

        fillSshResults(automatonTask)

        runPostSshOperations(automatonTask)

        results
    }

    /**
     * This will build the ssh command that needs to be executed
     * at a later point in time.
     *
     */
    private void of(Closure connOpts, String taskName, String cmd){

        assert connOpts != null, "Nil connection options provided."
        assert taskName != null, "Nil task name provided."
        assert cmd != null, "Nil command provided."

        props.put(SshSpecs.taskName, taskName)
        props.put(SshSpecs.command, cmd)

        SshDslEngine sshEngine = buildSshEngine(connOpts)

        // build the function as a closure to be executed later
        theSshTask = { doSsh(sshEngine) }
    }

    /**
     * This runs the operations intended to be executed after running the ssh
     * command. The operation name as well as the output is saved.
     * 
     * @param automatonTask
     * @return
     */
    private runPostSshOperations(AutomatonSSHTask automatonTask){
        String operationalOutput = automatonTask.cmdOutput.output

        operations?.each {

            operationalOutput = operationalOutput ?
                    BasicUtils.instance.runClosure(it.value, operationalOutput, operationalOutput) :
                    null

            operationalOutput ?
                    results.put(it.key, operationalOutput) :
                    results.put(it.key, "Could not run function on nil value.")

        }

    }

    /**
     * This fills up the results derived from the output 
     * by execution of ssh command.
     * 
     * @param automatonTask
     * @return
     */
    private fillSshResults(AutomatonSSHTask automatonTask){
        results << BasicUtils.instance.toMap(automatonTask, true)
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
    private AutomatonSSHTask doSsh(SshDslEngine sshEngine){
        CommandOutput cmdOutput = null
        sshEngine.remoteSession({cmdOutput = exec(props.get(SshSpecs.command))})

        def task = new AutomatonSSHTask(
                uuid: props.get(AutomatonSpecs.uuid),
                name: props.get(SshSpecs.taskName),
                command: props.get(SshSpecs.command),
                startTime: 'x:y:z',
                endTime: 'x1:y1:z1',
                timeTaken: 'x secs',
                threadName: Thread.currentThread().name,
                cmdOutput: cmdOutput)

        task
    }

}
