{it ->
    automaton {        
        job {       
            
            task {
                cmd 'ls -a'
            }
            
            measure_latency null
            run_tasks_in_parallel null
            gumba
            hoho 1
        }        
    }
}