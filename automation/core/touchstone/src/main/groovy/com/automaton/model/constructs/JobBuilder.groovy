package com.automaton.model.constructs

import com.automaton.dsl.AsConstruct
import com.automaton.types.MessageKey
import com.automaton.types.construct.AutomatonConstructType
import com.automaton.types.construct.JobConstructType
import com.automaton.utils.BasicUtils

@Deprecated
class JobBuilder implements AsConstruct{

    private void buildTask(JobConstructType type, TaskBuilder builder, Closure cls){
        
        Map props = [:]
        props[type] = builder.buildTaskFromScript(cls)

        add MessageKey.constructs, props
    }
    
    /**
     * Point of entry !!
     * 
     * @param cls
     * @return
     */
    def buildJobFromScript(Closure cls){

        assert cls != null, "Nil construct was provided while creating job construct."

        context = AutomatonConstructType.job

        BasicUtils.instance.runClosure(cls, this)

        getOrWarns()
    }

    void local(Closure cls){
        
        buildTask(JobConstructType.local, new LocalTaskBuilder(), cls)
    }

    void expression(Closure cls){
        
        buildTask(JobConstructType.expression, new ExpressionTaskBuilder(), cls)        
    }

    void remote(Closure cls){
        
        buildTask(JobConstructType.remote, new RemoteTaskBuilder(), cls)        
    }

    void http(Closure cls){
        
        buildTask(JobConstructType.http, new HttpTaskBuilder(), cls)        
    }

    void https(Closure cls){
        
        buildTask(JobConstructType.https, new HttpTaskBuilder(), cls)        
    }
}
