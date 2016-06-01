package com.automaton.model.constructs

import com.automaton.dsl.AsConstruct
import com.automaton.types.construct.AutomatonConstructType
import com.automaton.utils.BasicUtils
import com.automaton.utils.Version

/**
 *
 * @author amit.das@cloudbyte.com
 *
 */
@Deprecated
class AutomatonBuilder implements AsConstruct{

    private boolean isVersioned = false
    private boolean hasJob = false

    private void versionize(){
        isVersioned ?: usecase(Version.instance.defaultCaseName, Version.instance.defaultCaseVersion)
    }

    /*
     * Entry point
     */
    def buildAutomatonFromScript(Closure cls){

        context = AutomatonConstructType.automaton

        cls ? BasicUtils.instance.runClosure(cls, this) : reportFailure("Nil closure provided to '$context'.")

        getOrWarns()
    }

    void automaton(Closure cls){

        BasicUtils.instance.runClosure(cls, this)

        hasJob ?: reportFailure("'$context' does not have any job construct.", "Provide job and tasks that needs to be automated.")

        versionize()
    }

    void job(Closure cls){

        def jobBuilder = new JobBuilder()

        set AutomatonConstructType.job, jobBuilder.buildJobFromScript(cls)

        hasJob = true
    }

    void conn(Closure cls){

        def connBuilder = new ConnectionBuilder()

        set AutomatonConstructType.conn, connBuilder.buildConnFromScript(cls)
    }

    void settings(Closure cls){

        def settingsBuilder = new SettingsBuilder()

        set AutomatonConstructType.settings, settingsBuilder.buildSettingsFromScript(cls)
    }

    void usecase(String usecaseName, String usecaseVer){

        def versionBuilder = new VersionBuilder()

        set AutomatonConstructType.version, versionBuilder.buildVersion(usecaseName, usecaseVer)

        isVersioned = true
    }
}
