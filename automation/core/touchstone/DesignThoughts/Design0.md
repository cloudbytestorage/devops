#### Design - 0
- dated - Mid of April 2016

#### Introduction
This design marks the beginning of creating or reusing a library that meets
our automation requirements.

##### Started with Spock
- advantages:
  - reports with operation times & status
  - internal, external & custom plugin development are possible (via gradle plugins)
- disadvantages: 
  - fit everything w.r.t BDD
  - the concepts of steps though useful can be done easily without spock
  - cannot provide options from conf file
  - user has to write some boilerplate code
- summary
  - will use this probably for data driven automation testing if hand crafted code does not work out

#### Using Gradle build system
- advantages:
  - similar in spirit to [Capistrano](http://capistranorb.com/)
  - less boilerplate code
  - script that gives compilation errors
  - external & custom plugin development possible
- disadvantages:
  - takes a lot of time to get the output ( 6 to 9 seconds & more)
  - it is inherently designed to check everything before running the tasks
  - not using its core features i.e. tasks
  - use of tasks will make the conf more verbose with lots of boilerplate
  - so have resorted to single task & hand crafted steps/flows logic
- summary
  - script looks like a conf file after bit of custom coding (150 lines)
  - next action 
   - These 150 loc will be re-factored as this will keep growing.
   - Push these logic in pure groovy code & expose the DSL without using gradle's task

#### Current DSL looks like below:

```

	plugins { id 'org.hidetake.ssh' version '2.0.0' }
	
	apply from: "$projectDir/../common_tasks/ssh_utils.gradle"
	apply from: "$projectDir/../common_tasks/iscsi_initiator_utils.gradle"
	
	// Project Description
	description = "TCL ENV SUB PROJECT"
	version = "0.0.1"
	
	ssh.settings { logging = 'none' }
	
	remotes {
		client01 {
			role 'storage_client'
			host = '20.10.87.81'
			user = 'root'
			password = 'test@123'
		}
	}
	
	// define local functions from utility gradle files
	def flow = tt_ssh['flow']
	
	
	task verify_env << {
	
		//def settings = ['level': 'verbose', 'exit_condition': 'on_error']
		def settings = ['exit_condition': 'on_error']
		
		def options = [
			1: ['cmd': "cat /etc/*-release", 'check': [{op -> op =~ /CentOS release 6.9.*/}, "Must be CentOS 6.7"]],
			2: ['cmd': "yum --version", 'check': [{op -> op =~ /CentOS release 6.7.*/}, "Is this yum"]],
			3: ['cmd': "yum --version", 'startsWith': ["CentOS release 6.7", "This is not CentOS 6.7"]],
			4: null,
			5: null,
			6: ['cmd': "yum --version"]
		]
	
		flow(remotes.client01, options, settings)
	}
```
