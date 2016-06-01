package com.automaton.dsl

import com.automaton.types.AutomatonSpecs
import com.automaton.types.MessageKey
import com.automaton.types.MessageValue
import com.automaton.utils.BasicUtils

trait AsErrHandler{

    Map errors = [:]

    String errRunCondition(){
        BasicUtils.instance.appendToWarns(errors, "Can not run as condition is not satisfied.")
    }
    
    String errConstruct(String name){
        "Invalid '$name' function used."
    }

    String errProperty(String name){
        "Invalid '$name' property used."
    }

    String errPlacement(String name, String context){
        "'$name' function should be placed inside '$context'."
    }

    String errNilValue(String name, String context){
        "'$name' function is used inside '$context' but without any value."
    }

    String errSuggest(){
        "Refer the docs w.r.t the usage."
    }

    String errSuggestAsConstruct(String name){
        "Did you mean to use '$name' as a function ?"
    }

    String errSuggestAsInvalidConstruct(String name){
        "Either '$name' is an invalid function or its arguments are invalid !"
    }

    def methodMissing(String name, args) {
        BasicUtils.instance.appendToWarns(errors, errConstruct(name), errSuggestAsInvalidConstruct(name))
    }

    def propertyMissing(String name) {
        BasicUtils.instance.appendToWarns(errors, errProperty(name), errSuggestAsConstruct(name))
    }

    Map warns(){
        Map warns = BasicUtils.instance.getWarnsOrEmpty(errors)

        warns ? details() << warns : warns
    }

    private Map details(){

        Map props = [:]

        props.put(AutomatonSpecs.uuid, errors?.get(AutomatonSpecs.uuid))
        props.put(MessageKey.status, MessageValue.Failed)
    
        props
    }

    boolean hasWarns(){
        warns() ? true : false
    }
}
