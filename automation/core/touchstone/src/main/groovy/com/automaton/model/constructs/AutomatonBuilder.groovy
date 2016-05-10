package com.automaton.model.constructs

import com.automaton.types.construct.AutomatonConstructType
import com.automaton.types.construct.SettingsConstructType;
import com.automaton.utils.BasicUtils

/**
 *
 * @author amit.das@cloudbyte.com
 *
 */
class AutomatonBuilder implements AsConstruct{

    def buildAutomatonFromScript(Closure cls){

        if(cls){
            
            context = AutomatonConstructType.automaton
            
            BasicUtils.instance.runClosure(cls, this)
            
        }else{
            println 'Nil closure provided'
        }

        getOrWarns()
    }

    void automaton(Closure cls){

        BasicUtils.instance.runClosure(cls, this)
    }

    void job(Closure cls){

        def jobBuilder = new JobBuilder()

        set AutomatonConstructType.job, jobBuilder.buildJobFromScript(cls)
    }

    void conn(Closure cls){

        def connBuilder = new ConnectionBuilder()

        set AutomatonConstructType.conn, connBuilder.buildConnFromScript(cls)
    }

    void settings(Closure cls){

        def settingsBuilder = new SettingsBuilder()

        set AutomatonConstructType.settings, settingsBuilder.buildSettingsFromScript(cls)
    }
}
