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
            expression {
                cmd
                url
                response_starts_with
                match_response_with
                measure_latency
                unknown 1
            }
            https {
                cmd
                url
                response_starts_with
                match_response_with
                measure_latency
                unknown 1
            }
        }
        conn {}
        settings {}
   }
}