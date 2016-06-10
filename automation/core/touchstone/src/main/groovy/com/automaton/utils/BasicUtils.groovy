package com.automaton.utils

import static groovy.json.JsonOutput.prettyPrint
import static groovy.json.JsonOutput.toJson

import java.text.SimpleDateFormat

import com.automaton.model.constructs.AutomatonBuilder
import com.automaton.types.BaseType
import com.automaton.types.MessageKey

@Singleton
class BasicUtils {

    private List<String> TRUTHS = ['yes', 'YES', 1, '1', 'true', 'TRUE']

    boolean isTrue(truthy){
        truthy in TRUTHS
    }

    void pPrint(data){
        println prettyPrint(toJson(data)) + '\n'
    }

    def buildAtomatonConfigFromFile(File conf){
        AutomatonBuilder atmBuilder = new AutomatonBuilder()
        GroovyShell gShell = new GroovyShell()
        atmBuilder.buildAutomatonFromScript(gShell.evaluate(conf.text))
    }

    def Map getWarnsOrEmpty(Map props){
        Map warns = props?.subMap(MessageKey.warnings) ?: [:]
    }

    /*def Map getWarnsOrInfo(Map props){
        getWarnsOrEmpty(props) ?: props
    }*/

    def void incr(Map props, BaseType key){
        assert props != null, "Nil props was provided."
        assert key != null, "Nil key was provided."

        int currentCount = props.get(key, 0)

        currentCount++

        props.putAt(key, currentCount)
    }

    def Map toMap(object, boolean flatten = false) {

        assert object != null, "Nil object was provided."

        return object.properties
                .findAll{
                    (it.key != 'class')
                }.collectEntries {
                    it.value == null || it.value instanceof Serializable ?
                            [it.key, it.value]:
                            flatten ? toMap(it.value, true) : [it.key, toMap(it.value)]
                }
    }

    def void appendTo(Map props, key, newValue){

        assert props != null, "Nil props was provided."
        assert key != null, "Nil key was provided."
        assert newValue != null, "Nil value was provided."

        List existingVals = props.get(key, [])

        existingVals?.add(newValue)

        props.putAt(key, existingVals)
    }

    def void appendToWarns(Map props, failureMsg, suggestion = null){
        assert props != null, "Nil props was provided."
        assert failureMsg != null, "Nil failure message was provided."

        Map newprops = [:]

        newprops.put(MessageKey.msg, failureMsg)
        if(suggestion){
            newprops.put(MessageKey.suggest, suggestion)
        }

        appendTo(props, MessageKey.warnings, newprops)
    }

    /**
     * Utility method that is used to set the closure
     * properties before running the closure itself.
     *
     * @param cls
     * @return
     */
    def runClosure(Closure cls, Object args = null, Object context){

        assert cls != null, "Nil construct was provided."

        // create clone of closure to handle the thread safety issues
        Closure clsClone = cls.clone()
        // set delegate of closure to this object
        clsClone.delegate = context
        // only use this builder as the closure delegate
        //clsClone.resolveStrategy = Closure.DELEGATE_ONLY
        clsClone.resolveStrategy = Closure.DELEGATE_FIRST
        // run the closure
        args ? clsClone(args) : clsClone()
    }

    def time(String format = "yyyy-MM-dd HH:mm:ss"){
        new SimpleDateFormat(format).format(new Date())
    }

    /**
     * A closure that builds a Command Line Interface.
     * 
     * <p>
     * Note - This CLI is dependent on script file named atm 
     * (atm.bat for Windows) which is available in the project's root folder.
     */
    def buildCli = { args ->

        def cli = new CliBuilder(usage:'atm [options] <testcase or usecase folder/file>')

        cli.with {
            h longOpt: 'help', 'Usage Information', required: false
            f longOpt: 'folder', 'Folder path that must have script.groovy file', required: false
            s longOpt: 'script', 'File path of Groovy script file i.e. ending with .groovy', required: false
        }

        def options = cli.parse(args)

        if(!options){
            BasicUtils.instance.pPrint([
                'error': 'No options provided.',
                'suggest': 'Check the help option to learn using this CLI.',
                'help': 'atm -h'
            ])
            return
        }

        if(options.h){
            cli.usage()
            return
        }

        def extraArguments = options.arguments() ? options.arguments()[0] : null

        if(options.f && extraArguments){
            return new File("$extraArguments/script.groovy")
        }else if(options.s && extraArguments){
            return new File("$extraArguments")
        }

        BasicUtils.instance.pPrint([
            'error': 'Provided cli options is invalid.',
            'suggest': 'Did you forget to provide folder/file path ?',
            'help': 'atm -h'
        ])

        return
    }
}
