package com.automaton.model.constructs

import groovy.transform.Canonical

@Canonical
class ConnectionSettings extends GenericSettings{

    String host
    String user
    String password

    boolean isInValid(){
        error
    }

    def filteredOut = [
        'inValid',
        'class',
        'filteredOut',
        'password',
        'error',
        'suggest'
    ]

    Map asMap() {
        this.properties.findAll {!filteredOut.contains(it.key) && it.value}
    }
}
