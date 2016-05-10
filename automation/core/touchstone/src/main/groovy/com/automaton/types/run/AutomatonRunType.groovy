package com.automaton.types.run

/**
 * All are in past tense. 
 * Used to set properties after a use case has run.
 * 
 * @author amit
 *
 */
enum AutomatonRunType {
    /*
     * indicates the version of automaton on 
     * which the use case was run
     */
    version,
    /*
     * specifies if running the automaton for 
     * the use case was a success or has failed
     */
    status,
    /*
     * success or failure message after automaton was
     * run for the use case
     */    
    msg
}
