##### Features of Erlang
- very light weight processes
- very fast message passing
- total separation between processes
- automatic marshalling/demarshalling
- fast sequential code
- strict functional code
- dynamic typing
- transparent distribution
- compose sequential and concurrent code


##### Due to hardware changes
- each year your sequential program will go slower
- each year your concurrent program will go faster


##### Making a fault tolerant **system**
- need atleast 2 computers
- if one crashes the other must take over
- some conditions that should be adhered to
  - no shared data
  - distributed programming
  - pure message passing


##### Making a fault tolerant **computing**
- need atleast 2 isolated computers
- conditions  
  - concurrent programming
  - pure message passing

##### Making **very fault tolerant** computing
- need lots of isolated computers
- summary
  - fault tolerance,
  - distribution,
  - concurrency,
  - scalability **are inseparable**

##### Two models of concurrency
- Erlang programs are thread safe if they don't use an external resource.
- Shared Memory vs. Message Passing
- Shared memory will involve mutexes, threads & locks.
  - Sharing is the property that **prevents** fault tolerace & thread safety
- Message passing will involve messages & processes.


##### Concurrency Oriented Programming (COP)
- large no. of processes
- complete isolation between processes
- location transparency
- no sharing of data
- pure message passing systems

##### COP architectures
- email
- google map reduce
