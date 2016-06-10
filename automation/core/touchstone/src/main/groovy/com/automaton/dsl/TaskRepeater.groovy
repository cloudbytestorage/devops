package com.automaton.dsl

import groovy.transform.Immutable;

@Immutable
class TaskRepeater {
    int repeat = 1
    long interval = 5000    
}
