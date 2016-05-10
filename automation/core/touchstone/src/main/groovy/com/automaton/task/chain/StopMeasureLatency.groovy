package com.automaton.task.chain


class StopMeasureLatency implements Executor{

    StopMeasureLatency(Executor next){
        super(next)
    }

    def execute(Map automaton){
        if(automaton.measureLatency){
        }

        super.execute(automaton)
    }
}