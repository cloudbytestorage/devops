package com.automaton.task.chain


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
