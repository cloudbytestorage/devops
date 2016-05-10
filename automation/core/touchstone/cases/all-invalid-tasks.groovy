{it ->
    automaton{
        job{
            remote {
                cmd
                url
                response_starts_with                
                unknown 1
            }
            
            expression {
                cmd                
                match_response_with
                measure_latency
                known 1
            }            
        }
        
        conn {}
        
        settings {}
   }
}