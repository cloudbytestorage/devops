package com.automaton.types.generic

enum MessagePropertyType implements BaseType{
    /*
     * Property to map against a message
     */
    msg,
    /*
     * Property to map against a status
     */
    status,
    /*
     * Property to map against a suggestion
     */    
    suggest,
    /*
     * Property to map against warnings
     */
    warnings,    
    /*
     * Used as value
     */
    success,
    /*
     * Used as value
     */
    failed
}
