package com.automaton.types.construct

import com.automaton.types.BaseConstructType


/**
 * The constructs supported within a Automaton construct.
 *  
 * @author amit.das@cloudbyte.com
 *
 */
enum AutomatonConstructType implements BaseConstructType{

    /*
     * Property to map automaton.
     */
    automaton,
    /*
     * Property to map version.
     */
    version,
    /*
     * Property to map job.
     */
    job,
    /*
     * Property to map connection.
     */
    conn,
    /*
     * Property to map settings.
     */
    settings
}
