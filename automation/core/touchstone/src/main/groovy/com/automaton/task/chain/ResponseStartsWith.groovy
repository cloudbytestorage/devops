package com.automaton.task.chain

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
