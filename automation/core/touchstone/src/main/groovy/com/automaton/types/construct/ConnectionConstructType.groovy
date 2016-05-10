package com.automaton.types.construct

enum ConnectionConstructType {
    /*
     * Property to map against a host.
     */
    host,
    /*
     * Property to map against the user name.
     */
    user,
    /*
     * Property to map against the password. 
     */
    password,
    /*
     * Property to map success or failure; required after parsing the construct
     */
    status,
    /*
     * Property to map success or failure message; required after parsing the construct
     */
    msg
}
