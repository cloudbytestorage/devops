##### Lets understand this FRP via ELM the language: ELM Introduction
- ELM is a functional language that compiles to JavaScript
- No runtime errors.
- No null & undefined does not exist.

##### ELM - core language
- A function
  - isNegative n = n < 0
  - over100 n = if n > 100 then "over" else "under"
  - double n = n * 2
- A List
  - number = [1, 2, 3, 4]
  - List.map double numbers
  - List.sort numbers
- \
  - used in REPL to split into multiple lines
- Tuples
  - holds a fixed no. of values & each value can have a type
  - common use case is to return more than one value from a function
  - NOTE: When logic gets complicated, we may want to use records instead of tuples
- Records
  - set of key:value pairs
  - bill = {name = "Amite", age = 34} // bill.name etc..
  - note the dot operator on a record
    - it is actually a function i.e .name is a function in above syntax
    - .name is a function that gets the name field of the record
- Functions using Records
  - under70 {age} = age < 70
  - under70 bill  // True
  - under70 {id = 123, age = 60}  // True   // **Wow !!!**
- Update a Record
  - {bill | name = "das"} // {name = "das", age = 34}
  - Above creates a new record
  - ELM makes the update efficient by sharing the content


##### Infinitely nested components === ELM Architecture
-
