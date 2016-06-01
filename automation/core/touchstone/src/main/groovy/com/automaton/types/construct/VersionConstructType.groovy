package com.automaton.types.construct

import com.automaton.types.BaseConstructType

@Deprecated
enum VersionConstructType implements BaseConstructType{
    /*
     * Property to map against tool.
     */
    tool,
    /*
     * Property to map against usecase.
     */
    usecase,
}
