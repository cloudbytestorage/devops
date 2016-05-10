package com.automaton.model.reports

import java.util.Map;

import groovy.transform.Canonical
import groovy.transform.TupleConstructor;;

@Canonical
class GenericReport {
    String status
    String message
    String suggest = null

    def filteredOut = ['class', 'filteredOut']

    Map asMap() {
        this.properties.findAll {!filteredOut.contains(it.key) && it.value}
    }
}
