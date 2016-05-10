package com.automaton.task.executors

class StartMeasureLatency implements Executor{

    StartMeasureLatency(Executor next){
        super(next)
    }

    def execute(Map automaton){
        
        if(measureLatency(automaton)){
            
        }

        super.execute(automaton)
    }
}
