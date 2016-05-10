package com.automaton.model.reports

import groovy.transform.Canonical

/**
 * reference - http://mrhaki.blogspot.in/2014/05/groovy-goodness-use-builder-ast.html
 * @author amit
 *
 */
@Canonical
class JobReport extends GenericReport{
    int expected_tasks_run
    int actual_tasks_run
    int failed_verifications_count
    int errors_count
    String time_taken
    String verifications_status
    Set<TaskReport> taskReports

    def filteredOut = ['class', 'filteredOut', 'taskReports']

    Map asMap() {
        Map props = this.properties.findAll {!filteredOut.contains(it.key) && it.value}

        taskReports?.eachWithIndex { taskreport, idx ->
            props?.putAt("task_$idx", taskreport.asMap())
        }

        props
    }
}
