package com.automaton.utils

@Singleton
class Version {
    /*
     * tool specific
     * If below modified then remember to modify at build.gradle too
     */
    String toolName = 'touchstone'
    String toolVersion = '0.0.2'
    
    /*
     * usecase specific defaults
     */
    String defaultCaseName = 'NA'
    String defaultCaseVersion = '0.0.0'
    
    /*
     * delimiter between name & version
     */
    String delimiter = ":"
}
