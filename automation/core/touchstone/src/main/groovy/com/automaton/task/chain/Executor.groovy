package com.automaton.task.chain

trait Executor {

    private nextExecutor

    def execute(Map automaton){
        if(nextExecutor){
            nextExecutor.execue(automaton)
        }
    }
}
