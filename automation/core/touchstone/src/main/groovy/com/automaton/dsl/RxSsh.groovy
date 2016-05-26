package com.automaton.dsl


import java.util.concurrent.Callable

import rx.Observable

import com.aestasit.infrastructure.ssh.SshOptions
import com.aestasit.infrastructure.ssh.dsl.CommandOutput
import com.aestasit.infrastructure.ssh.dsl.SshDslEngine
import com.aestasit.infrastructure.ssh.log.SysOutEventLogger;

@Singleton
class RxSsh {

    Observable<AutomatonSSHTask> sequencedTasks;

    Observable<AutomatonSSHTask> ssh(Closure specificOpts, String taskName, String cmd){
        SshDslEngine sshEngine = buildSshEngine(specificOpts)
        Observable<AutomatonSSHTask> observableTask = executeO(sshEngine, taskName, cmd)
        sequencedTasks = sequencedTasks?.concat(observableTask) ?: observableTask
    }

    String trigger(){
        sequencedTasks.subscribe(
                { task -> },
                { task -> println "ERROR: $task" } , { task -> println "INFO: $task completed" }
                )

        "Tasks were triggered."
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

    private Observable<AutomatonSSHTask> executeO(SshDslEngine sslEngine, String taskName, String cmd){
        Observable.fromCallable({
            execute(sslEngine, taskName, cmd)
        } as Callable<AutomatonSSHTask>)
    }


    private AutomatonSSHTask execute(SshDslEngine sslEngine, String taskName, String cmd){
        CommandOutput cmdOutput = null
        sslEngine.remoteSession({  cmdOutput = exec(cmd)  })

        def task = new AutomatonSSHTask(name: taskName, cmdOutput: cmdOutput, timeTaken: 'x secs')

        println ("'${task.toString()}' executed on thread '${Thread.currentThread().name}'")

        task
    }


}
