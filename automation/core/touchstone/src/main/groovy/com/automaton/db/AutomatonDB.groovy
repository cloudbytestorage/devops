package com.automaton.db

import groovy.transform.Canonical

import com.automaton.model.constructs.AutomatonSettings
import com.automaton.model.reports.AutomatonReport

/**
 * Consists of automation settings & automation reports.
 * 
 * @author amit.das@cloudbyte.com
 *
 */
@Canonical
class AutomatonDB {

    AutomatonSettings atmSettings
    AutomatonReport atmReport

    Map asMap() {

        Map props = [:]
        
        props.putAt('settings', atmSettings?.asMap())
        
        props.putAt('run_report', atmReport?.asMap())
        
        props
    }
}
