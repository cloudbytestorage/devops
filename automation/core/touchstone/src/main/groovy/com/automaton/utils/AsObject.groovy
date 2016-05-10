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

    Map getWarns(){
        props?.subMap(MessagePropertyType.warnings) ?: null
    }
    
    Map getOrWarns(){
        getWarns() ?: props
    }
    
    Map get(){
        props
    }

    void fail(key, value){
        props.put(key, value)
        props.put(MessagePropertyType.status, MessagePropertyType.failed)
    }

    boolean isNull(value){
        null == value
    }
}
