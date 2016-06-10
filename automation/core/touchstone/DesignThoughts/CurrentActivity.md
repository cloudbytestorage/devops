##### 26th May 2016 -to- 27th May 2016
- [x] Model the design looking at sshoogr-0.9.25 library
- [x] Re-factor the namespaces

##### 31st May 2016 - 3rd Jun 2016
- [x] review board & svn checkin the modified code on 31st May
- [x] More friendly DSL - I
- [] Remove deprecated classes & methods.
- [] Can we use groovy default methods as operators ?
  - Refer - [Default Groovy Methods]( http://docs.groovy-lang.org/latest/html/api/org/codehaus/groovy/runtime/DefaultGroovyMethods.html)

```java

// current
then('verify if numeric', { isNumber() ? "'$it' is a number." : "'$it' is a string." })

// future
{ isNumber(), "'$it' is a number.", "'$it' is a string." }

```

- [] Save & Load the point-in-time value(s)
  - [x] Save
  - [x] Load
- [-] Finish off cython
- [] Look into scripts provided by karthik
- [] Remove the gradle sub projects
- [] Latency, start time & end time per task
- [] Error handling & reporting
- [] Robust error handling:
  - [] else parts,
  - [] user entries,
  - [] closures executed at runtime,
  - [] default arguments,  
  - [] try catch as decorators in AsErrHandler trait
- [] Dependent tasks
- [] Exit process on error
- [] Dump output to a file
- [] Verify the output & inject the verification results as a summary into the output itself.
- [] Run Condition
  - A immutable class that represents the condition to run. {runIf}
- [x] Sampling / Looping
  - [-] A immutable class that represents looping {repeat, interval, **runIf**}
  - [-] repeatIf grammar
- [] Metrics
  - [] Calculations (avg, mean, median, percentile) of one or more properties (latency, value, etc.)
- [] Threads / Parallel execution
- [] Ensure types for all closures
- [] Enable compile time checks for the program
