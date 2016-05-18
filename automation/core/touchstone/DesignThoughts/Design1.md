#### Design - 1
- dated April 25th 2016

##### Introduction
This marks the consolidation of learnings we have w.r.t automation. We tried with
few options, and are ready to weed out the un-necessary parts while building our 
core library for automation.

##### Code in pure groovy
- Use of @Canonical groovy classes
  - e.g. JobMetrics, TaskMetrics, JobSettings, TaskSettings
    - SSHSettings extends TaskSettings
    - RestClientSettings extends TaskSettings 
- Use of builders
  - e.g. JobMetricsBuilder, TaskMetricsBuilder, JobSettingsBuilder, TaskSettingsBuilder, etc..

#### Adding behaviors
- either via Chain of Responsibility pattern 
- or via Groovy Meta Programming
- below is a sample of the Groovy Meta Programming

```

	class CheckRespStartsWith implements TaskResponseOperator {     
	     def exec(String resp) { ... }
	}
	
	class CheckRespAs implements TaskResponseOperator {     
	     def exec(String resp) { ... }
	}
	
	class RunClosureOnResp implements TaskResponseOperator {     
	     def exec(String resp) { ... }
	}
	
	somewhere in the endpoint class i.e. cli class
	
	def taskConstructProps = [...]
	def taskOp = [...]
	
	
	def executor = new Object()
	
	executor.metaClass {
	     executors = TheFactory.executors(taskConstructProps)
	     mixin executors     
	     
	     exec {         
	         transformedOp = []
	         executors.each {
	              transformedOp << mixedIn[it].exec(taskOp)     // or simply exec the mixin one by one
	         }         
	         transformedOp
	     }
	}
	
	def transformedOp = executor.exec()
```

#### DSL looks like below:
- dated 23rd April 2016

```

	automaton {
	    job{
	        task01 {
	            run cmd 
	            verify response starts with
	            measure latency
	            run after 5 seconds
	        }
	        task02 {
	            run url
	            verify response as
	            run after task01 has run successfully
	            do not measure latency
	        }
	        
	        measure latency
	        run tasks in parallel
	    }
	}

```

#### Input & Output of Automaton
- dated 10th May 2016

```

	>> Input :
	
	automaton{
		job{
			  remote {uuid: 1, cmd:.. }
			  expression { uuid: 2, query_key: 1, cmd:...}
			  http {uuid: 3, cmd:...}
			  expression {uuid: 4, query_key: 2, cmd:...}
			  expression {uuid: 5, query_key: 3, cmd:..}
		}
		conn {}
		settings {}
	}
	
	>> Output >> config

	automaton
	
	  version
	    tool:
	    usecase:
	
	  warnings
	
	  job
	      warnings    
	      constructs
	        uuid1
	           warnings
	           constructs
		type: remote
	        uuid2
	           warnings
	           constructs
		type: local
	
	  settings
	      warnings
	      constructs
	
	  conn
	      warnings
	      constructs


	>> Output >> run

	automaton-run
	      ...
	      job-run
	              ...
	              remote-task-uuid1-run
	                 ...
	              local-task-uuid2-run
	                 ...
```