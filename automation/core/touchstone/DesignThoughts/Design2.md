#### Design - 3
- start date - 16th May 2016
- version - 0.0.1

#### Introduction
The core theme remains the same. This is not a new idea or diverging from design 1.
This is part of continuous improvement & marks consolidation of our learnings once again.
The idea here is to reflect on the parts that are in the process of building the core
automation & investigate if existing libraries that can be reused. This will reduce
the burden of maintaining yet another automation library.

#### References
- http://www.slideshare.net/g33ktalk/data-pipeline-acial-lyceum20140624
- https://www.infoq.com/presentations/funnel-distributed-monitoring
- http://reactivex.io/

#### Using a streaming library to build a data pipeline & finally exposing via Groovy DSLs.
- The points mentioned here are lifted outright from the references' links.
- What are streams ?
  - Streams are 'lazy lists' of data & effects.
  - Immutable & referentially transparent.
- What is a data pipeline ?
  - A Unified system for capturing events for analysis & building products
- How can a streams based library be used to build data pipelines ?
  - It understands events.
    - Can easily create:
      - event streams or
      - data streams
  - Analysis can be swiftly done via operators
  - Think it as another pattern that is implemented.    
    - Observer pattern done right.
    - A combination of best ideas from Observer, Iterator & functional programming.
    - Ready to be imported & used from day 1.
  - Avoid stateful logic by using functions over observable streams
  - Functional programming implies less code.
    - e.g. "ReactiveX's operators often reduce what was once an elaborate challenge into a few lines of code."
- Why a DSL wrapper is needed over a streaming library ?
  - To justify lets think in below terms:
    - Can we expose these programming concepts to a wider audience ?
    - Can this concepts be used by a QA, Support or an Admin in his day to day work ?
    - Why limit this to developers alone ?
  - The wrapper might evolve into providing a schema
    - i.e. describe data, provide a contract between fields & types
  - The wrapper will provide easy to understand error messages & suggestions
    - i.e. no more stack traces as error messages

#### Fitting RxJava into Automaton library i.e. the DSL wrapper (WIP)
- No need to write yet another automation library
  - Simply wrap around this proven stuff & expose as a DSL
- Design goals:
  - compositional
  - expressive  
  - dry
  - testable
- Phases:
  - Verify
    - Verify phases will parse the DSL & mark it as fit or unfit
  - Run
    - If verification phase passes then run phase will be executed
- Run Logic:
  - Observables may be created via
    - fromCallable operator for remote operations
    - single operator for local operations
  - Observable chained to a variant of retry operator  
  - Observable chained to a variant of sample operator
  - An Observable will wrap the remote/http calls
  - It might be desired to execute an Observable based on a Predicate.
  - It might be desired to combine the Observables & have a single subscriber.
  - Various transformers will verify the content that is emitted by the Observable.
  - Subscriber will publish the results.
  - We need to have a file based subscriber that will contain the formatted results.
  - What if the remote call takes a lot of time for completion?
- Look out for:
  - various retry operators
  - various sample operators
  - various combination operators
  - execution on particular Schedulers
  - take operator or throttle operator along with timeout operator for hang cases
  - debug the computations & the subscriptions with the Thread names
