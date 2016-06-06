package com.automaton.launcher

import com.automaton.dsl.AsErrHandler
import com.automaton.dsl.TaskRepeater
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
 * <p>
 * NOTE - This class is not threadsafe.
 * 
 * @author amit.das@cloudbyte.com
 *
 */
class AutomatonSpecsRunner implements AsErrHandler{

    /**
     * Will be used to add various properties & their values.
     * 
     */
    private Map<String, String> automatonTasks = [:]

    /**
     * A multi-property setter!!
     * 
     */
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

        String automatonUuid = BasicUtils.instance.time()

        // TODO Move this to constructor 
        errHandler(automatonUuid)

        specs ? BasicUtils.instance.runClosure(specs, this) : errNilValue("specifications")

        usecase ? BasicUtils.instance.runClosure(usecase, this) : errNilValue("usecase")

        //BasicUtils.instance.getWarnsOrInfo(automatonTasks)

        //warns() ?: automatonTasks
        def automatonWarns = warns()
        automatonWarns ? automatonWarns << automatonTasks : automatonTasks 
    }

    /**
     * A specification verb !!
     * 
     * @param repeater
     * @param sshSpecs
     * @return
     */
    private ssh(boolean canRun = true, Map repeater, Closure sshSpecs){

        TaskRepeater taskRepeater = new TaskRepeater(repeater)

        taskRepeater.repeat.times {

            doSsh(canRun, sshSpecs)

            if(it < taskRepeater.repeat) {
                sleep(taskRepeater.interval)
            }
        }
    }

    /**
     * A specification verb !!
     * 
     * @param sshSpecs
     * @return
     */
    private ssh(String sshUuid = null, boolean canRun = true, Closure sshSpecs){

        doSsh(sshUuid, canRun, sshSpecs)
    }

    /**
     * Makes actual ssh call & mutates the reports.
     * 
     * @return
     */
    private doSsh(String sshUuid = null, boolean canRun, Closure sshSpecs){

        SshSpecsRunner sshRunner = new SshSpecsRunner();

        BasicUtils.instance.appendTo(automatonTasks, AutomatonSpecs.sshRuns, sshRunner.runner(sshUuid, canRun, sshSpecs))

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
