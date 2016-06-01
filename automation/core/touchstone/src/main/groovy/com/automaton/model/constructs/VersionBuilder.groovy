package com.automaton.model.constructs

import com.automaton.dsl.AsConstruct
import com.automaton.types.construct.AutomatonConstructType
import com.automaton.types.construct.VersionConstructType
import com.automaton.utils.Version

@Deprecated
class VersionBuilder implements AsConstruct{

    /**
     * Point of entry
     * 
     * @param usecaseName
     * @param usecaseVer
     * @return
     */
    def buildVersion(String usecaseName, String usecaseVer){

        context = AutomatonConstructType.version

        tool()

        usecase(usecaseName, usecaseVer)

        getOrWarns()
    }

    void usecase(String usecaseName, String usecaseVer){
        set(VersionConstructType.usecase, usecaseName + Version.instance.delimiter + usecaseVer)
    }

    void tool(){
        set(VersionConstructType.tool, Version.instance.toolName + Version.instance.delimiter + Version.instance.toolVersion)
    }
}
