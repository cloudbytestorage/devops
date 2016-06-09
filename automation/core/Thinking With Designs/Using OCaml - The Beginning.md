##### References
- https://forge.ocamlcore.org/docman/view.php/77/37/OCaml+as+fast+as+C.pdf
- https://ocaml.janestreet.com/ocaml-core/latest/doc/
- https://news.ycombinator.com/item?id=9582980
- https://github.com/facebook/hhvm/blob/master/hphp/hack/src/heap/hh_shared.c
- https://realworldocaml.org/v1/en/html/concurrent-programming-with-async.html
- http://ocsigen.org/lwt/2.5.1/manual/


##### Introduction
Readers may find this article to be a collage of information collected from
various references. The entire credit goes to these geniuses who articulated
their thoughts into above blog links. What I have tried here is to **connect the
dots** so that writing programs or thinking with designs in any language becomes
palatable.


##### Some goodies of OCaml
- Catch errors to get a working program that nobody will need to read again
- It is GC efficient


##### Features
- a functional language (a fluent programming language)
- strict typing
- compile time checks
- static compilation
- fast prototyping
  - When prototyping **quick & dirty** is the rule of thumb


##### From imperative to functional - An example
```Python
  def sum(list):
    total = 0
    for num in list:
      total = total + num
    return total
```

- versus

```OCaml
  let rec sum list =
    match list with
    | [] -> 0
    | first :: rest -> first + sum rest
  ;;
```

##### From imperative to functional - Observations
- Which approach does not have any mutations ?
- Mutations, side effects etc are not bad.
  - Real world programs will have side effects
  - Judge your language by how much it helps you program with effects
- Do not judge your language / programs which provides pure computations.


##### From imperative to functional - Second example
```Python
  def find_mismatches(d1, d2):
    mismatches = []
    for (key, data) in d1.items():
      if data != d2[key]:   // some language throw exception; while some != null
        mismatches.append(key)
    return mismatches
```

- versus

```OCaml
  open Core.Std

  let find_mismatches map1 map2 =
    Map.to_sequence map1
    |> Sequence.filter_map ~f:(fun (key, data) ->
      match Map.find map2 key with
      | None -> None
      | Some data' ->
        if data' <> data then Some key
        else None
    )
```

##### From imperative to functional - Second Observations
- Why have we written the OCaml **so differently** i.e. pattern matching ?
- Well **Map.find** returns a **Some** type which we need to match explicitly.
- Else compiler will shout at you !!
- Avoid ```if data != d2[key]:```
- Some language throw exception if key is not found; while some will think it as:
  - data != null
- Go with **sequences & pattern matching as much as possible**


##### match ... with... & exception handling @ OCaml 4.02
```java

  let rec readfile ic accu =
    match input_line ic with
    | "" -> readfile ic accu
    | l -> readfile ic (l :: accu)
    | exception End_of_file -> List.rev accu

```

##### Basics
- http://roscidus.com/blog/blog/2013/06/20/replacing-python-round-2/



##### System programming using OCaml
- https://ocaml.github.io/ocamlunix/ocamlunix.html
- https://github.com/UnixJunkie/setop


##### Irmin - same design principles as Git
- https://github.com/mirage/irmin


##### DNS Server that automatically starts unikernels on demand
- https://github.com/mirage/jitsu

##### Collection of bindings to various low-level system API
- https://github.com/ygrek/extunix


##### Binding to c libraries
- Writing c extensions are straight forward
- https://github.com/ocamllabs/ocaml-ctypes
- https://github.com/Z3Prover/z3/issues/411
- http://caml.inria.fr/pub/docs/manual-ocaml/intfc.html#sec458


##### Binding to c libraries - with examples
- Note - Go through the commit history
- Simple example of a **finalizer attached to a custom block**:
  - https://github.com/libguestfs/libguestfs/blob/master/mllib/progress-c.c
  - https://github.com/libguestfs/libguestfs/blob/master/mllib/progress.ml
  - https://github.com/libguestfs/libguestfs/blob/master/mllib/progress.mli
- Complex example using **generational roots to deal with callbacks from OCaml back to C**
  - https://github.com/libguestfs/libguestfs/blob/master/ocaml/guestfs-c.c
- A tricky binding to libxml2
> Because libxml2 has objects containing pointers to other objects (at
> the C level) we need to shadow these with OCaml structs, to ensure
> that an OCaml object doesn't become unreachable when it is still
> pointed to from another object.
  - https://github.com/libguestfs/libguestfs/blob/master/v2v/xml-c.c
  - https://github.com/libguestfs/libguestfs/blob/master/v2v/xml.ml
  - https://github.com/libguestfs/libguestfs/blob/master/v2v/xml.mli


##### Read the async_* libraries of janestreet **imp**
-


##### Kernel implementation in OCaml **imp**
- https://github.com/mirage/mirage-tcpip
- https://github.com/mirage/shared-memory-ring
- https://github.com/mirage/mirage-block-xen
- https://github.com/mirage/io-page
- https://github.com/mirage/ocaml-cohttp

##### TLS implementation in OCaml **imp**
- https://github.com/mirleft/ocaml-tls


##### Binary protocols for cross language communication **imp**
- https://github.com/mfp/extprot


##### Implementing binary memcached protocol
- http://andreas.github.io/2014/08/22/implementing-the-binary-memcached-protocol-with-ocaml-and-bitstring/

##### capnproto - duo - data interchange format & capability based RPC system
- https://capnproto.org/


##### DAFT
- https://github.com/UnixJunkie/daft
- Allows file transfers across machines
- Actors
  - Meta Data Server (MDS)
  - Data Server(DS)
  - Command Line Interface (CLI)
- communication (may not be the entire list)
  - CLI push to DS
  - DS push to MDS
  - DS pull from MDS
  - DS pull from other DS
- Message encoding is secure
- state
  - MDS stores a global state
  - DSs' store a local view of global state
- Install
  - MDS on a single computer
  - DS, CLI & config on all computers
- Uses
  - Batteries
  - cryptokit
  - ZMQ
- Broadcast Algorithm
  - I - Using a chain
  - II - Using a binary tree
  - III - Using a binomial tree


##### Devops
- https://github.com/michipili/rashell


##### OCaml application templating
- https://github.com/michipili/gasoline


##### AI
- http://mmottl.github.io/aifad/


##### Unix cal replacement
- https://github.com/mor1/ocal


##### Batteries
- http://ocaml-batteries-team.github.io/batteries-included/hdoc2/


##### Sequence - Simple & efficient iterators
- https://github.com/c-cube/sequence/
- http://cedeela.fr/~simon/talks/sequence.pdf


##### Bigstrings - useful to interface with C, low level IO, memory-mapping, etc.
- https://github.com/c-cube/ocaml-bigstring/


##### Multicore with OCaml & c
- https://github.com/facebook/hhvm/blob/master/hphp/hack/src/heap/hh_shared.c
- https://www.youtube.com/watch?v=aN22-V-b8RM&feature=youtu.be&t=39m


##### MemCpy
- https://github.com/yallop/ocaml-memcpy


##### Workflow
- https://github.com/pveber/bistro/


##### Analyse pcap files
- https://github.com/mirage/ocaml-pcap


##### Establish connections to TCP & SSL
- https://github.com/mirage/ocaml-conduit


##### OCaml implementation of NBD
- https://github.com/xapi-project/nbd


##### OCaml implementation of block volumes in Mirage
- https://github.com/mirage/mirage-block-volume


##### Starting & Managing other services
- https://github.com/xapi-project/forkexecd


##### In-Memory message broker, queue, switch
- https://github.com/xapi-project/message-switch


##### Exploit the multicore
- https://github.com/rdicosmo/parmap


##### OCaml implementation of git format & protocol
- https://github.com/mirage/ocaml-git


##### Linter in OCaml
- https://github.com/facebook/pfff


##### OCaml bindings to glibc's passwd and shadow password file interface
- https://github.com/xapi-project/ocaml-opasswd


###### AString
- http://erratique.ch/software/astring/doc/Astring


##### Monad library
- https://github.com/michipili/lemonade

##### OCaml native
- native code compiler - ocamlopt
- compiles to native object files & links these objects to form an executable
- native code compiler is only available on certain platform


##### Reason
- https://facebook.github.io/reason/mlCompared.html
- https://github.com/facebook/reason

##### Mirage Projects
- https://github.com/mirage/mirage-www/wiki/Pioneer-Projects

##### traits & type
- http://www.lpw25.net/ml2014.pdf

##### Multicore
- https://ocaml.io/w/Multicore

##### Elixir vs. golang vs. OCaml
- Elixir doesn't target native code.
- Go type system is not much better than a safe C with interfaces and packages as addition.
- OCaml is much more modern language than golang
