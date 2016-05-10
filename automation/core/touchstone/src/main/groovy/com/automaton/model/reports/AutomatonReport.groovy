package com.automaton.model.reports

import java.util.Map;

import groovy.transform.Canonical

@Canonical
class AutomatonReport extends GenericReport{

    JobReport jobReport
    CodeCoverageReport codeCovReport

    def filteredOut = [
        'class',
        'filteredOut',
        'jobReport',
        'codeCovReport'
    ]

    Map asMap() {
        
        Map props = this.properties.findAll {!filteredOut.contains(it.key) && it.value}

        props?.putAt('job', jobReport?.asMap())

        props
    }
}
