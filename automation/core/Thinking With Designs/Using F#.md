##### References
- http://fsharpforfunandprofit.com/
- https://t.co/l0mfex3MUS


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
- Strongly typed 		             ```reduces errors```
- Semantic whitespace		         ```reduces errors```
- Functional first		           ```reduces errors```
- Option types			             ```reduces errors```
- Units of measure		           ```reduces errors```
- Type inference		             ```reduces RSI, makes #1 palatable```
- Static typing			             ```fast```
- Good parallel primitives	     ```lazy fast```
- Rich built-in data types		   ```reduces development time```
- Type providers		             ```reduces development time```
- Open source			               ```reduces dependency```
- Decent library support		     ```don’t want to roll my own db driver```
- Language iterop (*)		         ```increases library support```


##### Does a language play any role in a programmer's productivity ?
- Yes !!!
- Built-in high level data structures
  - e.g. dict, tuples, lists, etc
- Terse syntax
- Readable
- Rich operators


##### Functions
```java

  let evens list =
    let isEven x = x%2 = 0
    List.filter isEven list

```
- a multiline function block is defined using indents
- isEven is a inner nested function
- List.filter is a library function


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
