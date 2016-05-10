package com.automaton.task.chain

import java.util.Map;

class ExpressionExecutor implements Executor{

    ExpressionExecutor(Executor next){
        super(next)
    }

    def execute(Map automaton){
        
        if(expressionExec(automaton)){
            
        }

        super.execute(automaton)
    }
}