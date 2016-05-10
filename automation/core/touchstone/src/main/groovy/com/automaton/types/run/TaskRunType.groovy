package com.automaton.types.run

/**
 * All are in past tense.
 * Used to set properties after a use case has run.
 * 
 * @author amit.das@cloudbyte.com
 *
 */
enum TaskRunType {
    /*
     * success or failure message after execution of the task
     */
    msg,
    /*
     * flag indicating if the task executed successfully or failed
     */
    status,
    /*
     * start time of task execution
     */
    started_at,
    /*
     * completion time or exit time of task execution
     */
    completed_at,
    /*
     * time taken for the task to execute
     */
    latency
}
