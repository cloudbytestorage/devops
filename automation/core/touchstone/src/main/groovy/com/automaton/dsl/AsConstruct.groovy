package com.automaton.dsl

@Deprecated
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
        reportFailure errConstruct(name), errSuggestAsInvalidConstruct(name)        
    }

    def propertyMissing(String name) {        
        reportFailure errProperty(name), errSuggestAsConstruct(name)        
    }
}
