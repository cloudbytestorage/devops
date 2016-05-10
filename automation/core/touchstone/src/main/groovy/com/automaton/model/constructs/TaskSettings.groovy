package com.automaton.model.constructs

import groovy.transform.Canonical

@Canonical
class TaskSettings extends GenericSettings {
    
    ConnectionSettings connSettings
    String verify_response_as = null
    String response_starts_with = null
    boolean measure_latency = true
    String ssh_command = null
    String http_url = null

    boolean isHttp(){
        http_url
    }

    boolean isSsh(){
        ssh_command
    }

    boolean isInValid(){
        (error || (!http_url && !ssh_command) || (http_url && ssh_command))
    }

    def filteredOut = [
        'connSettings',
        'class',
        'filteredOut',
        'ssh',
        'http',
        'inValid',
        'error',
        'suggest'
    ]

    Map asMap() {
        Map props = this.properties.findAll {!filteredOut.contains(it.key) && it.value}

        if(connSettings?.asMap()){
            props.putAt('conn', connSettings.asMap())
        }
        
        props
    }
}
