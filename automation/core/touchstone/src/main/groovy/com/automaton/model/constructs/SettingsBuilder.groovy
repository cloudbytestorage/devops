package com.automaton.model.constructs

import com.automaton.dsl.AsConstruct
import com.automaton.types.construct.AutomatonConstructType
import com.automaton.utils.BasicUtils

@Deprecated
class SettingsBuilder implements AsConstruct{

    /**
     * Point of entry !!
     *
     * @param cls
     * @return
     */
    def buildSettingsFromScript(Closure cls){

        assert cls != null, "Nil construct was provided while creating settings construct."

        context = AutomatonConstructType.settings

        BasicUtils.instance.runClosure(cls, this)

        getOrWarns()
    }
}
