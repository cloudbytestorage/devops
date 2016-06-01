package com.automaton.types.construct

import com.automaton.types.BaseConstructType


/**
 * The constructs supported within a task 
 * i.e. remote, or local, or http, or expression construct.
 * 
 * @author amit.das@cloudbyte.com
 *
 */
@Deprecated
enum TaskConstructType implements BaseConstructType{

    /*
     * a unique representation of this task
     */
    uuid,
    /*
     * command that will be executed,
     * may accept feeder data which can transform this command
     */
    command,
    /*
     * transform the response of the task
     */
    transform_response,
    /*
     * match the response with some pattern
     */
    match_response_with,
    /*
     * match the response with starts-with pattern
     */
    response_starts_with,
    /*
     * flag indicating if the task's execution time
     * should be measured
     */
    measure_latency,
    /*
     * flag indicating if task should
     * run in different thread
     */
    fork,
    /*
     * will accept uuid (optional) & a transform fn (optional)
     * that builds a feeder data map to be used while running a task
     */
    feed_data,
    /*
     * will accept uuid & predicate fn (optional) that determines
     * execution or no execution of current task
     */
    run_if,
    /*
     * indicates success or failure after parsing the construct
     */
    status,
    /*
     * provides success or failure message after parsing the construct
     */
    msg
}
