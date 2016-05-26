package com.automaton.dsl

import com.automaton.types.generic.BaseType
import com.automaton.types.generic.MessageKey

trait AsObject {

    private Map props = [:]

    void set(key, value){
        props.put(key, value)
    }

    void set(Map<String, String> props){
        props.putAll(props)
    }
    
    void incr(BaseType key){
        assert key != null, "Nil key was provided."
        
        int currentCount = get()?.get(key, 0)
        
        currentCount++
        
        get()?.putAt(key, currentCount)
    }

    void add(key, newValue){

        assert key != null, "Nil key was provided."
        assert newValue != null, "Nil value was provided."

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

    Map toMap(object) {
        return object?.properties
                .findAll{
                    (it.key != 'class')
                }.collectEntries {
                    it.value == null || it.value instanceof Serializable ? [it.key, it.value]: [it.key, toMap(it.value)]
                }
    }

    void reportFailure(failureMsg, suggestion = null){

        assert failureMsg != null, "Nil failure message was provided."

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
