package com.automaton.model.constructs

import com.automaton.types.generic.MessagePropertyType
import com.automaton.utils.AsObject

trait AsConstruct implements AsObject{

    String context

    String errConstruct(String name){
        "Invalid '$name' construct used inside '$context'."
    }

    String errProperty(String name){
        "Invalid '$name' property used inside '$context'."
    }

    String errPlacement(String name){
        "'$name' construct should be placed inside '$context'."
    }

    String errNilValue(String name){
        "'$name' construct is used inside '$context' but without any value."
    }

    String errSuggest(){
        "Refer the docs w.r.t the usage of '$context' construct."
    }

    String errSuggestAsConstruct(String name){
        "Did you mean to use '$name' as a construct ?"
    }

    String errSuggestAsInvalidConstruct(String name){
        "Either '$name' is an invalid construct or its arguments are invalid !"
    }
    
    def methodMissing(String name, args) {
        Map<String, String> props = [:]
        props.putAt(MessagePropertyType.status, MessagePropertyType.failed)
        props.putAt(MessagePropertyType.msg, errConstruct(name))
        props.putAt(MessagePropertyType.suggest, errSuggestAsInvalidConstruct(name))

        List warningVals = get()?.get(MessagePropertyType.warnings, [])
        warningVals?.add(props)
        
        get()?.putAt(MessagePropertyType.warnings, warningVals)
    }

    def propertyMissing(String name) {
        Map<String, String> props = [:]
        props.putAt(MessagePropertyType.status, MessagePropertyType.failed)
        props.putAt(MessagePropertyType.msg, errProperty(name))
        props.putAt(MessagePropertyType.suggest, errSuggestAsConstruct(name))

        List warningVals = get()?.get(MessagePropertyType.warnings, [])
        warningVals?.add(props)
        
        get()?.putAt(MessagePropertyType.warnings, warningVals)
    }
}
