package com.automaton.task.executors


class Fork implements Executor{

    Fork(Executor next){
        super(next)
    }

    def execute(Map automaton){

        if(fork(automaton)){
        }

        super.execute(automaton)        
    }
}
