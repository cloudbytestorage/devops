package com.automaton.task.executors

import java.util.Map;

class ResponseStartsWith implements Executor{

    ResponseStartsWith(Executor next){
        super(next)
    }

    def execute(Map automaton){
        
        if(responseStartsWith(automaton)){
            
        }

        super.execute(automaton)
    }
}
