package com.automaton.experimental

import java.util.concurrent.TimeUnit

@Grab('io.reactivex:rxjava:1.1.5')
@Grab('com.aestasit.infrastructure.sshoogr:sshoogr:0.9.25')
import com.aestasit.infrastructure.ssh.dsl.SshDslEngine
import com.aestasit.infrastructure.ssh.dsl.CommandOutput
import com.aestasit.infrastructure.ssh.SshOptions
import com.aestasit.infrastructure.ssh.log.SysOutEventLogger

import rx.Observable
import rx.Subscriber
import rx.schedulers.TimeInterval;

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

def commonSshOpts = {

    logger = new SysOutEventLogger()

    trustUnknownHosts = true

    execOptions.with {
        showCommand = false
        showOutput = false
        failOnError = false
    }
}

// PREPARE Elastistor Machine
def esOpts = new SshOptions()
esOpts.with commonSshOpts
esOpts.with elastistorMacOpts
def elastistorMacEngine = new SshDslEngine(esOpts)

// PREPARE Cython Machine
def cthonOpts = new SshOptions()
cthonOpts.with commonSshOpts
cthonOpts.with cythonMacOpts
def cthonMacEngine = new SshDslEngine(cthonOpts)

// BUILD rx Observable from remote command execution output
Observable sshObservable(SshDslEngine sslEngine, String cmd){
    sshObservable(sslEngine, [cmd])
}

// BUILD rx Observable from remote command execution output
Observable sshObservable(SshDslEngine sslEngine, Collection<String> cmds){
    Observable.create({Subscriber<String> aSubscriber ->
        try {

            if (aSubscriber.isUnsubscribed()) {
                return;
            }

            CommandOutput cmdOutput = null
            sslEngine.remoteSession({ cmdOutput = exec(cmds) })

            aSubscriber.onNext(cmdOutput)

            if (!aSubscriber.isUnsubscribed()) {
                aSubscriber.onCompleted();
            }

        } catch(Throwable t) {
            if (!aSubscriber.isUnsubscribed()) {
                aSubscriber.onError(t);
            }
        }
    })
    .timeInterval()
}

// BUILD rx Subscriber that subscribes to rx Observable
Subscriber sshListener(String context, boolean debug=false){
    [
        onCompleted: {
            // uncomment below to debug
            // println("Task '$context' completed.")
        },
        onError: {Throwable e ->
            println("ERROR:: task: '$context' msg: '$e'")
        },
        onNext: {TimeInterval<CommandOutput> val ->
            if(val?.value?.failed()){
                def warns = val?.value?.getException()?: val?.value?.getOutput()?.trim()?: "Error during execution"
                println("WARN:: task: '$context' msg: '$warns'" )
            }else{
                def value = debug ? val?.value?.output?.trim()?: "No Output" : "--"
                def logPrefix = debug ? "DEBUG::" : "INFO::"
                def timeTaken = val?.intervalInMilliseconds?: "--"
                println("$logPrefix task: '$context' msg: '$value' timetaken: '$timeTaken' msecs")
            }
        }
    ] as Subscriber<String>
}

// TASK 1 - Remove lock file @ elastistor
sshObservable(elastistorMacEngine, 'rm /tenants/f7ec4eb1486c3aa6a4bafaa12d93e084/PoolRaidz1/Account1TSM1/amit.has')
        .subscribe(sshListener('remove lock'))

// TASK 2 - Restart lockd @ elastistor
sshObservable(elastistorMacEngine, 'do restart')
        .subscribe(sshListener('restart lockd after removing lock'))

// TASK 3 - Trigger execution of cython test cases
sshObservable(cthonMacEngine, ['cd /cthon04 && pwd'])
.subscribe(sshListener('trigger cython tests'))

// TASK 4 - Verify output of cython test cases
Observable.interval(5, TimeUnit.SECONDS)
        .flatMap({tick ->
            sshObservable(cthonMacEngine, 'cd /cthon04 && cat abc.out')
        })
        .take(3)
        .toBlocking()
        .subscribe(sshListener('verify cython tests'))

// TASK 5 - Enable lock file & restart lockd @ elastistor
sshObservable(elastistorMacEngine, 'touch /tenants/f7ec4eb1486c3aa6a4bafaa12d93e084/PoolRaidz1/Account1TSM1/amit.has')
        .subscribe(sshListener('enable lock & restart lockd'))

// TASK 6 - Restart lockd @ elastistor
sshObservable(elastistorMacEngine, 'do restart')
        .subscribe(sshListener('restart lockd after enabling lock'))