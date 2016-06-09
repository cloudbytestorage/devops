##### References
- https://github.com/rzezeski/try-try-try/


##### Erlang & Process
- http://www.erlang.org/doc/reference_manual/processes.html


##### Erlang & bahavior
- Think behavior similar to an contract or interface.
- The callback methods needs to be implemented.
- http://www.erlang.org/doc/design_principles/fsm.html
- http://erldocs.com/R14B/stdlib/gen_fsm.html


##### Erlang & Function
- http://www.erlang.org/doc/reference_manual/functions.html


##### Node vs. a vnode
- A Node refers to a physical machine.
- A virtual node is abbreviated as vnode.
- A physical node can be composed of multiple vnodes.
- A vnode is an Erlang process.
- Think vnode as a custom application's runtime running on Erlang runtime.
- vnode is a **behavior** written on top of the gen_fsm behavior

##### Vnode vs. Application
- They should not be treated against each other.
- A vnode can be thought of as an application:
  - handling incoming requests
  - storing data to be retrieved later
- An application is coded on top of the vnode behavior.

##### Why vnode ?
- It is a unit of **concurreny, replication & fault tolerance**.
- Is Erlang not meant to give us above ?


##### vnode - tricky parts
- Each machine has a vnode master
- A vnode master keeps track of all active vnodes on its node


##### vnode & callbacks
- init/1
  - initializes the state of the vnode
- terminate/2
- handle_exit/3
  - invoked during a crash


##### vnode & requests
- All incoming requests become commands on the vnode
- To implement a command, add a handle_command/3 that matches the incoming request.

##### vnode & handoff
- A handoff occurs when a vnode realizes it's not on the proper node
- vnode is typically tagged against a node
- A handoff happens when the ring has changed.
  - e.g. when a node is added or removed
  - e.g. when a node comes alive after it has been down

##### riak core & hinted handoff
- hint is a piece of data that **tells the partition where its proper home is**.
- A home check is a periodic check that uses hint data.
- The check ensures if the vnode is on the correct physical host.

##### if handoff then data transfer
- The purpose of handoff is to transfer data from one vnode to another.
- Note - **data transfers are not required** if vnode is **purely computational**
- A bunch of functions i.e. callbacks will actually do the handoff data transfer.


##### handoff & heuristics
- vnode has the final say in whether or not the handoff will occur.
- vnode might have some heuristics that determines its load
  - & choose not to participate in handoff if overloaded at the moment.


##### coordination
- https://github.com/rzezeski/try-try-try/tree/master/2011/riak-core-the-coordinator

##### conflict resolution
- https://github.com/rzezeski/try-try-try/tree/master/2011/riak-core-conflict-resolution
