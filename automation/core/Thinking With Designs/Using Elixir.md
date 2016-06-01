##### References
- http://elixir-lang.org/


##### Features
- Code runs within lightweight threads of execution (called processes)
- Each process is isolated & exchange information via messages
- This is not same as an OS process
- Processes are also able to communicate with other processes in different machines
- Hence, distributed coordination across multiple nodes (horizontal scaling)
- Elixir provides supervisors to restart parts of the system when things go wrong
- Can invoke any Erlang function with no runtime cost


##### Tools
- Mix is a build tool
- Hex is the package manager
- IEx for interactive development


##### Version
- Elixir - Version 1.2.0
- Erlang - Version 18.0


##### iex
- In Windows, the terminal may not use UTF-8 by default
- Run ```chcp 65001``` before entering IEx
- When it is provided with a list of printable ASCII numbers:
  - Elixir prints it as a char list
  - Use i/1 to retrieve info if in doubt
  - [104, 101, 108, 108, 111]   # hello
  - i 'hello'


##### Hello World
```java
  "Hello" <> " World"
  >> Hello World
```


##### Tuple
```java

  {1, 2, 3}                   # a tuple
  sometuple = {:ok, "hello"}  # any type

  # Elements are stored **contiguously in memory**.
  # Accessing a element per index is fast.
  # Getting the tuple size is a fast operation.
  # Tuple index starts from 0.

  elem(sometuple, 1)          # hello
  tuple_size(sometuple)       # 2

  put_elem(sometuple, 1, "world")     # {:ok, "world"}

  # The original tuple was **not modified**.
  # Elixir data types are immutable.
  # Updating or adding elements is expensive.
  # Updating or adding involves copying the whole tuple in memory.
  # Accessors are fast operations, while mutators are slow.

  # size vs length
  # size operation is in constant time i.e. pre-calculated value
  # length operation is linear i.e. slower as input grows

  # Use tuple as return objects in functions
  {:ok, "...", true, ...}
  or
  {:error, ""}

```


##### Un-Apply or De-structure
- via pattern matching
- allows de-structuring of data & easy access to its contents
- pattern matching be mixed with guards i.e. predicates


##### List
```java

  [1, 2, 3]               # list
  [1, 2, true]            # any type
  [1, 2] ++ [3, 4]        # concatenate
  [1, 2, true] -- [true]  # subtraction

  list = [1, 2, 3]
  hd(list)                # 1
  tl(list)                # [2, 3]

  # Lists are linked lists.
  # Each element holds a value & a pointer to following element
  # This element i.e. a pair is known as a **cons cell**

  list = [1 | [2 | [3 | []]]]     # [1, 2, 3]
  # Accessing the length is a linear operation.
  # Accessing the length involves traversing the whole list.
  # Updating the list is fast if we are pre-pending elements.

```


##### Atom / Symbol
```java

  :atom # atom / symbol

  # Atoms are constants where the name itself is the value
  # Booleans true & false are atoms

  true == :true       # true
  is_atom(false)      # true
  is_boolean(:false)  # true
```


##### Other interesting data types
- Port, Reference, PID
- Used during process communication


##### Arithmetic
```java

  10/2          # 5.0, floats are 64 bit double precision
  div(10, 2)    # 5
  div 10, 2     # 5 ; very similar to Groovy
  rem 10, 3     # 1

  0b1010        # shortcut for entering binary number
  0o777         # shortcut for entering octal number
  0x1F          # shortcut for entering hexadecimal number

  round(4.7)    # 5
  trunc(4.7)    # 4
```



##### String Interpolation
```java

  "hello #{:world}"   # hello world

  "hello" == 'hello'  # false; double quote & single quote are not equal
  # single quotes are character list

```


##### Functions
```java

  add = fn a, b -> a + b end  # anonymous functions; delimited by fn & end keywords
  is_function(add, 1) # false; checking arity

  # anonymous functions are closures
  add.(1, 2)                          # dot(.) invokes closures
  add_two = fn a -> add.(a, 2) end    # currying; rcurry
  (fn -> x = 0 end).()                # x is scoped within the closure
```
