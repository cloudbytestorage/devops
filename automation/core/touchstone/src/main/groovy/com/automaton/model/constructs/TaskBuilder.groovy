package com.automaton.model.constructs

import com.automaton.dsl.AsConstruct
import com.automaton.types.construct.JobConstructType
import com.automaton.types.construct.TaskConstructType
import com.automaton.utils.BasicUtils

/**
 * 
 * @author amit.das@cloudbyte.com
 *
 */
@Deprecated
trait TaskBuilder implements AsConstruct{

    def buildTaskFromScript(Closure cls){

        assert cls != null, "Nil construct was provided while creating task construct."

        context = JobConstructType.task

        BasicUtils.instance.runClosure(cls, this)

        getOrWarns()
    }

    void measure_latency(String truthy){

        isNull(truthy) ? reportFailure(errNilValue(TaskConstructType.measure_latency)) : set(TaskConstructType.measure_latency, BasicUtils.instance.isTrue(truthy))
    }

    void cmd(String command){

        isNull(command) ? reportFailure(errNilValue(TaskConstructType.command)) : set(TaskConstructType.command, command)
    }

    void url(String url){

        isNull(url) ? reportFailure(errNilValue(TaskConstructType.command)) : set(TaskConstructType.command, url)
    }

    void response_starts_with(String match){

        isNull(match) ? reportFailure(errNilValue(TaskConstructType.response_starts_with)) : set(TaskConstructType.response_starts_with, match)
    }

    void match_response_with(String match){

        isNull(match) ? reportFailure(errNilValue(TaskConstructType.match_response_with)) : set(TaskConstructType.match_response_with, match)
    }
}
