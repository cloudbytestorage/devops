package com.automaton.model.constructs

import com.automaton.dsl.AsConstruct
import com.automaton.types.construct.AutomatonConstructType
import com.automaton.types.construct.ConnectionConstructType
import com.automaton.utils.BasicUtils

@Deprecated
class ConnectionBuilder implements AsConstruct{

    def buildConnFromScript(Closure cls){

        assert cls != null, "Nil construct was provided while creating connection construct."

        context = AutomatonConstructType.conn

        BasicUtils.instance.runClosure(cls, this)

        getOrWarns()
    }

    void host(String host){

        isNull(host) ? reportFailure(errNilValue(ConnectionConstructType.host)) : set(ConnectionConstructType.host, host)
    }

    void user(String userName){

        isNull(userName) ? reportFailure(errNilValue(ConnectionConstructType.user)) : set(ConnectionConstructType.user, userName)
    }

    void password(String pw){

        set ConnectionConstructType.password, pw
    }
}
