package com.automaton.task.chain

import java.util.Map;

class LocalExecutor implements Executor{

    LocalExecutor(Executor next){
        super(next)
    }

    def execute(Map automaton){
        
        if(localExec(automaton)){
            
        }

        super.execute(automaton)
    }
}