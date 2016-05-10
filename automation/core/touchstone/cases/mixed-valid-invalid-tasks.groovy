{it ->
    automaton{
        job{
            remote {
                cmd
                url
                response_starts_with
                match_response_with
                measure_latency
                unknown 1
            }
            expression {}
            https {}
        }
        conn {}
        settings {}
   }
}