package com.automaton.utils

import com.automaton.model.constructs.AutomatonSettings
import com.automaton.model.constructs.ConnectionSettings
import com.automaton.model.constructs.JobSettings
import com.automaton.model.constructs.TaskSettings
import com.automaton.model.reports.AutomatonReport
import com.automaton.model.reports.JobReport
import com.automaton.model.reports.TaskReport

class TheFactory {

    private static Map atmFactory = [settings: AutomatonSettings, report: AutomatonReport]

    private static Map jobFactory = [settings: JobSettings, report: JobReport]

    private static Map connFactory = [settings: ConnectionSettings]

    private static Map taskFactory = [settings: TaskSettings, report: TaskReport]

    static AutomatonReport noScriptFoundReport(){

        atmFactory.report.newInstance([
            status: 'WARNING',
            message: 'No script was found to run.',
            suggest: 'Read the docs to understand the process of providing script.'
        ])
    }

    static AutomatonReport invalidScriptReport(AutomatonSettings atmSettings){

        def msg = atmSettings?.error ?: "Script is not constructed properly."

        def suggestion = atmSettings?.suggest ?: "Read the docs to understand the scripting process."

        atmFactory.report.newInstance([
            status: 'WARNING',
            message: msg,
            suggest: suggestion
        ])
    }

    static AutomatonReport validScriptReport(){

        atmFactory.report.newInstance([
            status: 'REGISTERED',
            message: 'A valid automaton script.'
        ])
    }

    static JobReport validJobReport(){

        jobFactory.report.newInstance([
            status: 'REGISTERED',
            message: 'A valid job.'
        ])
    }

    static JobReport invalidJobReport(JobSettings jobSettings){

        def msg = jobSettings?.error ?: "job is not constructed properly."

        def suggestion = jobSettings?.suggest ?: "Read the docs to understand the scripting process."

        jobFactory.report.newInstance([
            status: 'WARNING',
            message: msg,
            suggest: suggestion
        ])
    }

    static JobReport noJobFoundReport(){

        jobFactory.report.newInstance([
            status: 'WARNING',
            message: 'No job was found.',
            suggest: 'Read the docs to understand the scripting process.'
        ])
    }

    static TaskReport noTaskFoundReport(){

        taskFactory.report.newInstance([
            status: 'WARNING',
            message: 'No task was found.',
            suggest: 'Task is the primary construct which is automated.'
        ])
    }

    static TaskReport invalidTaskReport(TaskSettings taskSettings){

        def msg = taskSettings?.error ?: "Task is not constructed properly."

        def suggestion = taskSettings?.suggest ?: "Read the docs to understand the scripting process."

        taskFactory.report.newInstance([
            status: 'WARNING',
            message: msg,
            suggest: suggestion
        ])
    }

    static TaskReport validTaskReport(){

        taskFactory.report.newInstance([
            status: 'REGISTERED',
            message: 'A valid task.'
        ])
    }
}
