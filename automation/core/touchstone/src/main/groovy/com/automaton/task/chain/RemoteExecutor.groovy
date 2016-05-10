package com.automaton.task.chain

import java.util.Map;

class RemoteExecutor implements Executor{

    RemoteExecutor(Executor next){
        super(next)
    }

    def execute(Map automaton){
        
        if(remoteExec(automaton)){
            
        }

        super.execute(automaton)
    }
}