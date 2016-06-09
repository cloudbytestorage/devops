##### References
- https://tech.esper.com/2014/07/30/algebraic-data-types/
- Refer to **On Better Coding** for basics on Algebraic Data Types


##### Pair - a product in ADT
```OCaml

  # let pair = (1, 2);;
  val pair : int * int = (1, 2)
```

##### Pair - Observations
- A cross-product of sets

##### Possible operations on above pair i.e. product
```OCaml

  # let left (x , y) = x;;
  val left : `a * `b -> `a = <fun>  
```

##### Create a tuple - a product in ADT
```OCaml

  # let tuple = (1, 2, 3, 4);;
  val tuple : int * int * int * int = (1, 2, 3, 4)
```

##### Create a named tuple - a product in ADT
```OCaml

  # type blah = {foo: int; bar: int};;
  type blah : {foo: int; bar:int;}

  # let bb = {foo=1; bar=2};;
  val bb : blah = {foo=1; bar=2}
```

##### Create an either type - a variant in ADT
```OCaml

  # type (`a, `b) either = Left of 'a
                          | Right of 'b

  # let lefty = Left 1;;
  val lefty : (int, 'a) either = Left 1

  # let righty = Right 1;;
  val righty : ('a, int) either = Right 1
```

##### Either type - Some Observations
- The return value is a wrapped one.
- Hence, very suitable for pattern matching.


##### Create an option type - a variant in ADT
```OCaml

  # type 'a option = Some of 'a
                    | None
```

##### Enum - a variant in ADT which does not have a value
```OCaml

  # type state = START
                | STOP
                | PAUSE
```


##### Create a variant to represent a JSON
```OCaml

  type json = Object of json StringMap
              | Array of json list
              | String of string
              | Number of float
              | True
              | False
              | Null
```

##### Create a json variant - Observations
- parsing can be done via pattern matching
