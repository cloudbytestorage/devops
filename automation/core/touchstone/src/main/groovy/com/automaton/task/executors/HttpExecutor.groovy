package com.automaton.task.executors

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