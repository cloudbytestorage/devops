package com.automaton.task.chain

import java.util.Map;

class HttpExecutor implements Executor{

    HttpExecutor(Executor next){
        super(next)
    }

    def execute(Map automaton){

        if(httpExec(automaton)){
        }

        super.execute(automaton)
    }
}