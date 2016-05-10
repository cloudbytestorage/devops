package com.automaton.task.executors

import java.util.Map;

class RunIf implements Executor{

    RunIf(Executor next){
        super(next)
    }

    def execute(Map automaton){
        if(automaton.measureLatency){
            
        }

        super.execute(automaton)
    }
}
