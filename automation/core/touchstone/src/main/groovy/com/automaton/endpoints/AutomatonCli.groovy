package com.automaton.endpoints

import com.automaton.utils.BasicUtils

/**
 * A script class that provides a fluent command line API for Automaton library.
 *
 * @author amit.das@cloudbyte.com
 *
 */

/*
 *  STEP 1 - Build a CLI that can accept user input from terminal.
 *  
 *  Note - This is the default CLI. One may create custom CLI for custom extensions.
 *  Note - The expected user input for this CLI is the groovy DSL file.
 *  Note - 'args' comes from static void main method's argument.
 *  Note - This groovy script will be compiled into a static void main method class.
 */
File conf = BasicUtils.instance.runClosure(BasicUtils.instance.buildCli, args, this)

/*
 * STEP 2 - Build the config from the provided DSL.
 */
def config = null
if(conf){
    config = BasicUtils.instance.buildAtomatonConfigFromFile(conf)
}else{
    return
}

/*
 * STEP 3 - Display the generated config
 */
config = config ?: [
    error: "Config could not be generated from the provided DSL.",
    suggest: "Refer to docs on usage of DSL."
]

BasicUtils.instance.pPrint(config)

/*
 * STEP 4 - 
 */

// check if any warnings after parsing

// build the task chain

// execute the chain

