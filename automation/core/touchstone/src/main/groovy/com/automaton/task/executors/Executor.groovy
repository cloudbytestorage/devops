package com.automaton.task.executors

trait Executor {

    private nextExecutor

    def execute(Map automaton){
        if(nextExecutor){
            nextExecutor.execue(automaton)
        }
    }
}
