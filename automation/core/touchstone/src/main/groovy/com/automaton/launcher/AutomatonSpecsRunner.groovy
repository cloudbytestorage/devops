package com.automaton.launcher

import com.automaton.dsl.AsErrHandler
import com.automaton.types.AutomatonSpecs
import com.automaton.utils.BasicUtils
import com.automaton.utils.Version

/**
 * This class parses the automation specifications.
 * Once the specifications (in form of a groovy closure) is provided
 * to the entry point method(s) the specification verbs will be 
 * automatically invoked in the sequence provided within the closure.
 * 
 * The suffix *Runner* signifies the **run** phase of the specifications.
 * In other words this class is meant to run the specifications.
 * 
 * @author amit.das@cloudbyte.com
 *
 */
class AutomatonSpecsRunner implements AsErrHandler{

    private Map<String, String> automatonTasks = [:]

    private Closure defaultUseCase = {
        String usecaseName = Version.instance.defaultCaseName
        String usecaseVersion = Version.instance.defaultCaseVersion
    }

    /**
     * Entry point
     */
    def specification(Closure specs){
        specification(specs, defaultUseCase)
    }

    /**
     * Entry point
     */
    def specification(Closure specs, Closure usecase){

        specs ? BasicUtils.instance.runClosure(specs, this) : reportFailure("Nil specifications provided.")

        usecase ? BasicUtils.instance.runClosure(usecase, this) : reportFailure("Nil usecase provided.")

        BasicUtils.instance.getWarnsOrInfo(automatonTasks)
    }

    /**
     * A specification verb !!
     * 
     * @param sshSpecs
     * @return
     */
    private ssh(String uuid = null, boolean canRun = true, Closure sshSpecs){

        def sshRunner = new SshSpecsRunner();

        BasicUtils.instance.appendTo(automatonTasks, AutomatonSpecs.ssh, sshRunner.runner(uuid, canRun, sshSpecs))

        BasicUtils.instance.incr(automatonTasks, AutomatonSpecs.sshCount)
    }

    /**
     * A specification verb !!
     * 
     * @param usecaseSpecs
     * @return
     */
    private usecase(Closure usecaseSpecs){
    }
}
