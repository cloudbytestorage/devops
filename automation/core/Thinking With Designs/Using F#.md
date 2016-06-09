##### References
- http://fsharpforfunandprofit.com/
- https://t.co/l0mfex3MUS
- [Erlang vs F#](http://programmers.stackexchange.com/questions/123218/f-performance-vs-erlang-performance-is-there-proof-the-erlangs-vm-is-faster)


##### F# vs Erlang
> F# benefits from the optimization capabilities of the .NET Jitter.
> In addition, the language itself is designed to be a high-performing functional
> language (it being a variant of OCaml, widely used in the financial industry
> because of its speed).


> Ultimately, unless you plan on running millions of tiny agents at the same time
> (which is what Erlang is optimized for), F# should be up to the task.


##### Kids will love these features !!
- one-liner logic
- no curly braces, semicolons, parentheses
- type inference
- easy composition of functions
- automatic equality & comparison
- no need of null checks
- embed business logic into types
- units of measure


##### Can grown-ups fall in love ?
- Can the logic implicitly contain **less errors** ?
  - Strongly typed
  - Semantic whitespace
  - Functional first
  - Option types
  - Units of measure
- Can the logic be **readable** ?
  - Type inference
- Can it be inherently fast ?
  - Static typing
  - Good parallel primitives (lazy fast)
- Can the logic be built quickly i.e. **less development time** ?
  - Rich built-in data types
  - Type providers
- Can the logic have fewer or **no dependency** ?
  - Open source
  - Decent library support (don’t want to roll my own db driver)
  - Language iterop


##### Does a language play any role in a programmer's productivity ?
- Yes !!!
- Built-in high level data structures
  - e.g. dict, tuples, lists, etc
- Terse syntax
- Readable
- Rich operators


##### F# syntax
- Can be developed interactively  
- No commas, semicolons are used as delimiters in lists
- Commas are used in Tuples
- No semicolons, only indents for multiline functions
- Semicolons are used in Records
- No curly braces, use indents or new lines
- Curly braces are used in Records
- No simple braces, use spaces
- ```let``` keyword defines an immutable value
- ```let``` keyword can also define a named function
- **|>** removes the need for simple braces
- **match..with..** is the switch case statement
- match..with.. makes use of **|** and **->** and **_**
- It is **printfn** here and not println
- **type** is a keyword used for defining Record
- type keyword is used for defining **Union** types
- Automatic type inference or type cast when needed
- Automatic type inference or use of **of** operator


##### Interactive Development
- Can be developed interactively.
  - Keep an interactive window open.
  - Try the new functions here.
  - Move these functions to project once satisfied.
- NOTE : This is no replacement for unit tests.


##### Type inference
```java

  let square x = x * x

  let sumOfSquares n =
   [1..n] |> List.map square |> List.sum    // type in inferred to be int

  sumOfSquares 100                          // type in inferred to be int

  let squareF x = x * x

  let sumOfSquaresF n =
     [1.0 .. n] |> List.map squareF |> List.sum  // "1.0" is a float

  sumOfSquaresF 100.0                       // passing 100 will throw type error

```

##### Nullable Wrappers
- let validValue = Some(100)
- let invalidValue = None


##### List
```java

  let lister = [1;2;3;4]

  let zerolister = 0 :: lister  // [0;1;2;3;4]
  let zerol = [0] @ lister      // [0;1;2;3;4]

```

##### Tuples
```java

  let threeTuple = 1,"a",true
```

##### Record Types
```java

  type person = {First:string; Last:string} // named fields, use of semicolons

  let per1 = {First="john";Last="das"}      // kind of a format
```


##### Union types
```java

  type Temp =               // use of **type** keyword
    | DegreesC of float     // use of **|** and **of**
    | DegreesF of float
  let temp = DegreesF 98.6

```


##### Build new types from existing ones
```java

  type Employee =               // a union type
    | Worker of Person          // use of **of**
    | Manager of Employee list  // contain the self type

  let adas = {First="amit";Last="das"}
  let worker = Worker adas      // type casting

```


##### printfn
```java

  printfn "Printing an int %i, a float %f, a bool %b" 1 2.0 true
  printfn "A string %s, and something generic %A" "hello" [1;2;3;4]

  printfn "aTuple=%A,\nPerson=%A,\nTemp=%A,\nEmployee=%A"
    aTuple person1 temp worker

```


##### Functions
```java

  let square x = x * x        // use of **let** and **=**

  let evens list =            // multiline function
    let isEven x = x%2 = 0    // nested inner function; **=** as comparison check
    List.filter isEven list   // use of library function with 2 parameters

```


##### ```|>``` pipe operator & other goodies
```java

  // define the square function
  let square x = x * x

  // define the sumOfSquares function
  let sumOfSquares n =
    [1..n] |> List.map square |> List.sum

  // or multiline indented logic
  let sumOfSquares n =
    [1..n]
    |> List.map square
    |> List.sum

  // using anonymous functions
  let sumOfSquares n =
    [1..n]
    |> List.map (fun x -> x * x)
    |> List.sum

  // try it
  sumOfSquares 100

```
- let variable defines an immutable value
- Type declarations not required
- Type is inferred ```val square : int -> int```
- Proper indentations will indicate a block of code (like Python)
- Whitespace is used to separate parameters than commas
- Can test in an interactive window
- No ```return``` needed, as function always returns the value of last expression.


##### Scripting
- Understands a script i.e. ```.fsx extension```
- Alternatively REPL style or interactive window is possible with F#
  - Similar to javascript linting ```;;``` is used to mark end of interaction.
-





##### F# vs Erlang - syntax
- http://theburningmonk.com/2012/07/what-does-this-f-code-look-like-in-erlang-part-1-of-n/
