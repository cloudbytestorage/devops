package com.automaton.task.chain

import java.util.Map;

class FeedData implements Executor{

    FeedData(Executor next){
        super(next)
    }

    def execute(Map automaton){
        
        if(feedData(automaton)){
            
        }

        super.execute(automaton)
    }
}
