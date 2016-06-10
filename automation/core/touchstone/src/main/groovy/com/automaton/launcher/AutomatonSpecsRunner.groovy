package com.automaton.launcher

import com.automaton.dsl.AsErrHandler
import com.automaton.dsl.TaskRepeater
import com.automaton.types.AutomatonSpecs
import com.automaton.types.SshSpecs
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
 * NOTE - There is no variant Algebraic Data Type in Groovy. Hence, we
 * need to use couple of overloaded ssh functions. 
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

        def automatonWarns = warns()
        automatonWarns ? automatonWarns << automatonTasks : automatonTasks
    }

    /**
     * A specification verb !!
     * Multiple variants exists.
     * 
     * @param repeater
     * @param sshSpecs
     * @return
     */
    private String ssh(boolean canRun = true, Map repeater, Closure sshSpecs){

        TaskRepeater taskRepeater = new TaskRepeater(repeater)

        Map<String, String> results

        for(int i=1; i <= taskRepeater.repeat; i++){

            results = doSsh(canRun, sshSpecs)

            /*
             * Check the just executed repeat flag to break or repeat.  
             */
            if(null != results.get(SshSpecs.allowRepeat) && "false" == results.get(SshSpecs.allowRepeat)){
                break
            }

            /*
             * Sleep if it is not the last repetition
             */
            if(i < taskRepeater.repeat) {
                sleep(taskRepeater.interval)
            }
        }

        /*(1..taskRepeater.repeat)
         .each {
         uuid = doSsh(canRun, sshSpecs)
         if(it < taskRepeater.repeat) {
         sleep(taskRepeater.interval)
         }
         }*/
    }

    /**
     * A specification verb !!
     * Multiple variants exists.
     * 
     * @param sshSpecs
     * @return
     */
    private Map<String, String> ssh(String sshUuid = null, boolean canRun = true, Closure sshSpecs){

        doSsh(sshUuid, canRun, sshSpecs)
    }

    /**
     * A specification verb !!
     * Multiple variants exists.
     * 
     */
    private Map<String, String> ssh(boolean canRun, Closure sshSpecs){

        doSsh(canRun, sshSpecs)
    }

    /**
     * Makes actual ssh call & mutates the reports.
     * 
     * @return
     */
    private Map<String, String> doSsh(String sshUuid = null, boolean canRun, Closure sshSpecs){

        SshSpecsRunner sshRunner = new SshSpecsRunner();

        Map<String, String> runResults = sshRunner.runner(sshUuid, canRun, sshSpecs)

        BasicUtils.instance.appendTo(automatonTasks, AutomatonSpecs.sshRuns, runResults)

        BasicUtils.instance.incr(automatonTasks, AutomatonSpecs.sshCount)

        runResults
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
