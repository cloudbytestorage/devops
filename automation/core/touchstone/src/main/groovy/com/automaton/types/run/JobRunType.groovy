package com.automaton.types.run

/**
 * All are in past tense.
 * Used to set properties after a use case has run.
 * 
 * @author amit.das@cloudbyte.com
 *
 */
enum JobRunType {
    /*
     * count of total tasks present in the job
     */
    total_tasks_count,
    /*
     * count of tasks that ran successfully
     */
    successful_tasks_count,
    /*
     * flag that specifies if remaining tasks should 
     * run in case of any failure of any task
     */
    continue_on_error,
    /*
     * specifies if use case was run successfully
     * or had any failures 
     */
    status,
    /*
     * success or failure description after running the use case
     */
    msg,
    /*
     * start time of the job
     */
    started_at,
    /*
     * completion time or exit time of the job
     */
    completed_at,
    /*
     * time taken for the job to run
     */
    latency
}
