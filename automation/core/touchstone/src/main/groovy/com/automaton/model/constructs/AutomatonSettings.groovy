package com.automaton.model.constructs

import java.util.Map;

import groovy.transform.Canonical

@Canonical
class AutomatonSettings extends GenericSettings{

    ConnectionSettings connSettings
    JobSettings jobSettings

    boolean isInValid(){
        error
    }
    
    def filteredOut = [
        'class',
        'filteredOut',
        'connSettings',
        'jobSettings',
        'inValid'
    ]
    
    Map asMap() {

        Map props = this.properties.findAll {!filteredOut.contains(it.key) && it.value}
        
        props?.putAt('job', jobSettings?.asMap())
        
        props?.putAt('conn', connSettings?.asMap())
        
        props
    }
}
