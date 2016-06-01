package com.automaton.dsl

import groovy.transform.TupleConstructor

import com.aestasit.infrastructure.ssh.dsl.CommandOutput

@TupleConstructor
class AutomatonSSHTask{
    String uuid
    String name
    String command
    String startTime
    String endTime
    String timeTaken
    String threadName
    CommandOutput cmdOutput
}
