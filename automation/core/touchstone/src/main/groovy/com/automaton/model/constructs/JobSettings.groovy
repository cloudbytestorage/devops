package com.automaton.model.constructs

import groovy.transform.Canonical

@Canonical()
class JobSettings {
    String error
    String suggest
    boolean run_tasks_in_parallel = true
    boolean measure_latency
    int tasks_count
    Set<TaskSettings> taskSettings

    boolean isInValid(){

        if(!taskSettings){
            error = "No task found in job construct."
        }

        (error || taskSettings?.find {it.inValid})
    }

    def filteredOut = [
        'connSettings',
        'taskSettings',
        'class',
        'filteredOut',
        'inValid',
        'error',
        'suggest'
    ]

    Map asMap(boolean considerNilValue = false) {

        Map props = this.properties.findAll {!filteredOut.contains(it.key) && (it.value || considerNilValue)}

        taskSettings?.eachWithIndex { task, idx ->
            props.putAt("task_$idx", task.asMap())
        }

        props
    }
}
