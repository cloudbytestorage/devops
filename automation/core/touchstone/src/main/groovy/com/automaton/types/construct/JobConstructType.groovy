package com.automaton.types.construct

import com.automaton.types.BaseConstructType


/**
 * The constructs supported within a job construct.
 * There may be multiple occurrences of each construct. 
 * A construct may be dependent on another construct.
 * 
 * @author amit.das@cloudbyte.com
 *
 */
@Deprecated
enum JobConstructType implements BaseConstructType{    
    /*
     * Property to map against a remote task.
     */
    remote,
    /*
     * Property to map against a local task.
     */
    local,
    /*
     * Property to map against a http task.
     */
    http,
    /*
     * Property to map against a https task.
     */
    https,
    /*
     * Property to map against a local expression based task. 
     */
    expression,
    /*
     * Property to map success or failure; required after parsing the construct
     */
    status,
    /*
     * Property to map success or failure message; required after parsing the construct
     */
    msg,
    /*
     * Property to map against a generic task
     */
    task
}
