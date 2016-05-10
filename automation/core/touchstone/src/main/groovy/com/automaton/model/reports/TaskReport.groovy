package com.automaton.model.reports

import groovy.transform.Canonical

@Canonical
class TaskReport extends GenericReport{
    String name
    String time_taken
    String error_msg
    String failed_verification_msg
    String verification_status

    def filteredOut = ['class', 'filteredOut']

    Map asMap() {
        this.properties.findAll {!filteredOut.contains(it.key) && it.value}
    }
}
