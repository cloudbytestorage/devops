package com.automaton.task.executors


class TransformResponse implements Executor{

    TransformResponse(Executor next){
        super(next)
    }

    def execute(Map automaton){
        
        if(transformResponse(automaton)){
        }

        super.execute(automaton)
    }
}