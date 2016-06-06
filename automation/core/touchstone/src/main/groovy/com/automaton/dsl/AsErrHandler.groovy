package com.automaton.dsl

import com.automaton.types.AutomatonSpecs
import com.automaton.types.MessageKey
import com.automaton.types.MessageValue
import com.automaton.utils.BasicUtils

trait AsErrHandler{

    Map errors = [:]

    def errHandler(String uuid){
        errors.put(AutomatonSpecs.uuid, uuid)
    }

    /**
     * A mutator!!
     * 
     * @return
     */
    String errRunCondition(){
        BasicUtils.instance.appendToWarns(errors, "Can not run as condition is not satisfied.")
    }

    /*String errPlacement(String name, String context){
     "'$name' function should be placed inside '$context'."
     }*/

    /**
     * A mutator!!
     *
     * @return
     */
    def errNilValue(String name){
        BasicUtils.instance.appendToWarns(errors, "Nil '$name' provided.", errSuggest())
    }

    /**
     * A mutator!!
     *
     * @return
     */
    def methodMissing(String name, args) {
        BasicUtils.instance.appendToWarns(errors, errConstruct(name), errSuggestAsInvalidConstruct(name))
    }

    /**
     * A mutator!!
     *
     * @return
     */
    def propertyMissing(String name) {
        BasicUtils.instance.appendToWarns(errors, errProperty(name), errSuggestAsConstruct(name))
    }

    /**
     * A utility !!
     * 
     * @return
     */
    Map warns(){
        Map warns = BasicUtils.instance.getWarnsOrEmpty(errors)

        warns ? details() << warns : warns
    }

    /**
     * A utility!!
     *
     * @return
     */
    boolean hasWarns(){
        warns() ? true : false
    }

    private String errConstruct(String name){
        "Invalid '$name' function used."
    }

    private String errProperty(String name){
        "Invalid '$name' property used."
    }

    private String errSuggest(){
        "Refer the docs w.r.t the usage."
    }

    private String errSuggestAsConstruct(String name){
        "Did you mean to use '$name' as a function ?"
    }

    private String errSuggestAsInvalidConstruct(String name){
        "Either '$name' is an invalid function or its arguments are invalid !"
    }

    private Map details(){

        Map props = [:]

        props.put(AutomatonSpecs.uuid, errors?.get(AutomatonSpecs.uuid))
        props.put(MessageKey.status, MessageValue.Failed)

        props
    }
}
