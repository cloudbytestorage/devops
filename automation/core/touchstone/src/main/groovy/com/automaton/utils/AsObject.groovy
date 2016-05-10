package com.automaton.utils

import com.automaton.types.generic.MessagePropertyType

trait AsObject {

    private Map props = [:]

    void set(key, value){
        props.put(key, value)
    }

    void set(Map<String, String> props){
        props.putAll(props)
    }
    
    void add(key, newValue){
        List existingVals = get()?.get(key, [])
        
        existingVals?.add(newValue)
        
        get()?.putAt(key, existingVals)
    }

    Map getWarns(){
        props?.subMap(MessagePropertyType.warnings) ?: null
    }

    Map getOrWarns(){
        getWarns() ?: props
    }

    Map get(){
        props
    }

    void reportFailure(failureMsg, suggestion = null){

        Map newprops = [:]

        newprops.put(MessagePropertyType.status, MessagePropertyType.failed)
        newprops.put(MessagePropertyType.msg, failureMsg)
        if(suggestion){
            newprops.put(MessagePropertyType.suggest, suggestion)
        }

        add(MessagePropertyType.warnings, newprops)
    }

    boolean isNull(value){
        null == value
    }
}
