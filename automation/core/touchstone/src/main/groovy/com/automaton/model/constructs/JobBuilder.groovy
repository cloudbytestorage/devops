package com.automaton.model.constructs

import com.automaton.types.construct.AutomatonConstructType
import com.automaton.types.construct.JobConstructType
import com.automaton.types.generic.MessagePropertyType
import com.automaton.utils.BasicUtils

class JobBuilder implements AsConstruct{

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

        LocalTaskBuilder taskBuilder = new LocalTaskBuilder()

        set JobConstructType.local, taskBuilder.buildTaskFromScript(cls)
    }

    void expression(Closure cls){
        ExpressionTaskBuilder taskBuilder = new ExpressionTaskBuilder()

        set JobConstructType.expression, taskBuilder.buildTaskFromScript(cls)
    }

    void remote(Closure cls){
        RemoteTaskBuilder taskBuilder = new RemoteTaskBuilder()

        set JobConstructType.remote, taskBuilder.buildTaskFromScript(cls)
    }

    void http(Closure cls){
        HttpTaskBuilder taskBuilder = new HttpTaskBuilder()

        set JobConstructType.http, taskBuilder.buildTaskFromScript(cls)
    }

    void https(Closure cls){
        HttpTaskBuilder taskBuilder = new HttpTaskBuilder()

        set JobConstructType.https, taskBuilder.buildTaskFromScript(cls)
    }
}
