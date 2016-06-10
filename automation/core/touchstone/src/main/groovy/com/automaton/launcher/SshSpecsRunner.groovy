package com.automaton.launcher

import com.automaton.dsl.AsErrHandler
import com.automaton.dsl.GrSsh
import com.automaton.types.AutomatonSpecs
import com.automaton.utils.BasicUtils

/**
 * This class parses the ssh specifications.
 * Once the specifications (in form of a groovy closure) is provided
 * to the entry point method(s); the specification verbs will be
 * automatically invoked in the sequence provided within the closure.
 *
 * The suffix *Runner* signifies the **run** phase of the specifications.
 * In other words this class is meant to run the specifications.
 * 
 * @author amit.das@cloudbyte.com
 *
 */
class SshSpecsRunner implements AsErrHandler{

    private GrSsh grSsh

    /**
     * Point of entry !!
     * 
     * Will trigger the SSH iff the SSH specification is correct.
     *
     */
    def Map runner(String sshUuid = null, boolean canRun = true, Closure sshSpecs){

        assert sshSpecs != null, "Nil ssh specifications provided."

        sshUuid = sshUuid ?: BasicUtils.instance.time()
        
        // TODO Move this to constructor
        errHandler(sshUuid)

        if (!canRun){
            errRunCondition()
            return warns()
        }

        grSsh = new GrSsh(sshUuid)

        BasicUtils.instance.runClosure(sshSpecs, this)

        warns() ?: grSsh.trigger()
    }

    /**
     * A specification verb !!
     * 
     * @param funcName
     * @param func
     */
    private void then(String funcName = null, Closure func){

        funcName = funcName ?: "operation" + BasicUtils.instance.time(" HH:mm:ss")

        grSsh.then(funcName, func)
    }

    /**
     * A specification verb !!
     * 
     * @param conn
     * @param taskName
     */
    private void to(Closure conn, String taskName){
        grSsh.to(conn, taskName)
    }

    /**
     * A specification verb !!
     * 
     * @param command
     */
    private void run(String command){
        grSsh.run(command)
    }

    /**
     * A specification verb !!
     * 
     * @param key
     */
    private void storeAs(String key, Map container){
        grSsh.storeAs(key, container)
    }
    
    /**
     * A specification verb !!
     * 
     * @param repeatCondition
     */
    private void repeatIf(Closure repeatCondition){
        grSsh.repeatIf(repeatCondition)
    }
}
