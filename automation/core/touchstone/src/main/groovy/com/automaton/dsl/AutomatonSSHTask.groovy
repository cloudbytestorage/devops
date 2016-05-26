package com.automaton.dsl

import groovy.transform.TupleConstructor

import com.aestasit.infrastructure.ssh.dsl.CommandOutput

@TupleConstructor
class AutomatonSSHTask{
    String name
    String command
    String timeTaken
    String threadName
    CommandOutput cmdOutput
}
