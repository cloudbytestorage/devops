##### Introduction
Readers may find this article to be a collage of information collected from
various references (refer part `1` in the series). The entire credit goes to
these geniuses who articulated their thoughts into above blog links. What I have
tried here is to **connect the dots** so that writing programs or thinking with
designs in any language becomes palatable.


##### OCaml support for multicore parallelism
- Had a poor support. What is the current status ?
- **Quote 1**
> You can make OS level threads, but they can't be both running at the same time
> due to the GIL (Global Interpreter Lock). Then why are they even there you
> might ask? Because it allows you to do a blocking call on a thread and to keep
> executing other stuff in the main thread. Other languages that have a GIL
> (and the same restriction) are Javascript (including Node.js), Ruby and Python.

- **Quote 2**
> In practice,  You're never gonna make your own thread to block on things.
> You're gonna use Lwt to manage all your concurrency so you can do tons of
> blocking stuff at the same time and combine the tasks nicely without ending up
> in a Node.js-style "callback hell". But still, even with tons of concurrency,
> you don't have parallelism. It's all you need for 98% of your programs, but if
> you then need to do heavy number-crunching it won't be enough.

- **Quote 3** - Option 1 for CPU bound work !!
> you can use ctypes to call C code easily (from Lwt_preemptive) and then release
> the lock from within C with caml_release_runtime_system(), so your C code will
> be truly parallel (and running in the thread pool automatically managed by
> Lwt_preemptive), and you can call caml_acquire_runtime_system() before returning
> the result back to OCaml to get the lock back and merge back with the normal code.

- **Quote 3** - Option 2 for CPU bound work !!
> Do an oldschool fork() and communicate with message-passing. Or have a master
> that manages workers and communicates with ZMQ, HTTP, TCP, IPC, etc. Or use a
> library that does it all for you like parmap, Async Parallel, etc etc.
> What this "multicore support" means is that you'll be able to have threads in
> the same process that run in parallel because the GIL is going away. In practice
> it'll probably be implemented directly into Lwt so you'll be able to do something
> with Lwt_preemptive and just tell it to run some function in a separate thread
> and then use >>= to handle its result. It's gonna be simpler than both options
> I described above.

- **Quote 4** - How FaceBook manages parallelism for Hack
> Hack is a language type checker. Since it needs to operate on the scale of
> Facebook's codebase (tens of millions of lines of code), it's a pretty
> performance-sensitive program. We needed real parallelism, but doing it with
> fork() and IPC was too costly for us, both in terms of storage (if you aren't
> careful you end up duplicating a bunch of data) and CPU (serializing/deserializing
> OCaml data structures to send over IPC is CPU-intensive). FB ended up doing
> it differently. Before fork(), mmap a MAP_ANON|MAP_SHARED region of memory --
> that region will be backed by the same physical frames in each child after we
> fork, so writes to it in one child process will be visible in the others. We
> use a little bit of C code to safely manage the shared-memory concurrency here.



##### Concurrency
> A completely different kettle of fish, nothing to do with parallelism and
> should not be bundled under the same subheading. OCaml has had very solid
> support for concurrency for over 15 years now.


##### Concurrent programming with async
- Use case for concurrency:
  - waiting for a click
  - waiting for data to be fetched from disk
  - waiting for space to be available on an outgoing network buffer
- Solution 1 to concurrency
  - use **preemptive system threads** (Java/C# use this approach)
  - here each thread can block or wait without blocking the whole program
  - note - system threads require significant memory
  - note - OS can interleave execution of these threads & hence need for immutability
  - note - In addition the need to protect shared resources due to OS interleaving
- Solution 2 to concurrency
  - single threaded approach, where the **single thread runs in an event loop**
  - event loop reacts to external events by invoking a callback function
  - note - the control flow has to be inverted. Its awkward to have a maze of callbacks
- OCaml's **async library** to solve concurrency
  - a hybrid model
  - note - avoid performance compromises
  - note - avoid synchronization woes of preemptive threads
  - note - avoid confusing inversion of control found in event driven systems
- OCaml's Lwt library to solve concurrency
  - It provides a light weight cooperative threads
  - Launching a thread is very fast
  - It does not requrie a new stack, a new process, etc.
  - Context switches are very fast
  - We can launch a thread for every system call
  - These threads can be composed & hence easy to code async programming


##### IO in Ocaml core vs. in Async
- In core, In_channel.read_all, is a blocking operation.
- The fact that it returns a concrete string means it can't return until the read has completed.
- Whereas in Async it returns a deferred that will be computed in future.
- In Async, processing of IO & other events is handled by the Async scheduler.
- Deferred.bind d f
  - takes a deferred value d & applies function f when d is available*)

```OCaml


  # let uppercase_file filename =
    Deferred.bind (Reader.file_contents filename)
     (fun text ->
         Writer.save filename ~contents:(String.uppercase text))
  ;;
  val uppercase_file : string -> unit Deferred.t = <fun>

  (*
  * Writing out Deferred.bind explicitly can be rather verbose,
  * and so Async.Std includes an infix operator for it: >>=.
  *)

  # let uppercase_file filename =
    Reader.file_contents filename
    >>= fun text ->
    Writer.save filename ~contents:(String.uppercase text)
  ;;
  val uppercase_file : string -> unit Deferred.t = <fun>

```


##### Async bind contd..
```OCaml

  # let count_lines filename =
    Reader.file_contents filename
    >>= fun text ->
    List.length (String.split text ~on:'\n')
  ;;
  Characters 85-125:
  Error: This expression has type int but an expression was expected of type
         'a Deferred.t

```
- remember the inflix operator for Async bind **>>=**
- What is this **~** operator ?
- compiler shouts here. Why ?
  - bind expects a function that returns deferred but code does not do so
  - we need a function that wraps the value & returns as deferred
- In Async it has been thought of well. The function **return** does this !!
```OCaml

  # return;;
  - : 'a -> 'a Deferred.t = <fun>
  # let three = return 3;;
  val three : int Deferred.t = <abstr>
  # three;;
  - : int -> 3

  # let count_lines filename =
    Reader.file_contents filename
    >>= fun text ->
    return (List.length (String.split text ~on:'\n'))
  ;;
  val count_lines : string -> int Deferred.t = <fun>
```


##### Async bind & return === Monad === .map operator
- bind & return form a design pattern in functional programming known as **monad**.
- This is again shortcut as Deferred.map
```OCaml

  # Deferred.map;;
  - : `a Deferred.t -> f:(`a -> `b) -> `b Deferred.t = <fun>
```


##### Async bind & return === Monad === .map === >>|
- can be written more succintly using >>|
```OCaml

  # let count_lines filename =
    Reader.file_contents filename
    >>| fun text ->
    List.length (String.split text ~on:'\n')
    ;;    
  val count_lines : string -> int Deferred.t = <fun>

  # count_lines "/etc/hosts";;
  - : int = 11
```


##### ivars
