##### Introduction
This post will focus on the ways to write better code using Groovy. It will try
to accommodate the design practices followed by some popular libraries or other
languages. It will explain the theory via examples & code snippets. One can use
this to compare a certain design with another design. This post will provide
suggestive ideas to write better code in Groovy.

Note - Many of the sections have been lifted outright from the references
mentioned below. The entire credit goes to these good folks.

##### References
- http://mariogarcia.github.io/functional-groovy/
- https://github.com/GPars/GPars
- https://www.infoq.com/presentations/gpars
- http://docs.groovy-lang.org/next/html/gapi/groovy/transform/Immutable.html

##### Closure
- Closure is a function.
- Typed closure is possible in Groovy.

```java

  Closure<?> = { -> }

```

- Closures can be declared in class fields, static fields & local variables.


##### Redefine operators via closures
```java

  Double calc() {
    def numbers = 1..10
    return numbers
      .collect(it * 2)
      .collect(it / 10)
      .sum()
  }

```

- Do you find things similar to **rx.Observable's** operators.


##### Efficient use of operators via closures
- NOTE: Here the collection is not iterated twice like above

```java

  Double cacl2() {
    def numbers = 1..10
    def mulBy2 = {it * 2}
    def divBy10 = {it / 10}
    def combine = mulBy2 >> divBy10 // execution is from left to right

    return numbers
      .collect(combine)
      .sum()
  }

```

- Alternative

```java

  Double calc3 (Integer... numbers) {    
    def operation =
      Calculations.divideByTen <<
      Calculations.twoTimes

      numbers.collect(operation).sum()
  }

```

- Alternative

```java

  Double applyFuncAndSum(Closure<Number>) fn, Integer... numbers{
    numbers.collect(fn).sum()
  }
```


##### Currying
- A way of transforming a function that takes multiple arguments.
- But wait !! This is no different from a normal function.
- However, with currying, the same function can be called as a chain of functions
  - where each function gets a piece of the arguments.
- Currying is a special case of partial application where
  - the original function with number of arguments
  - produces another function of smaller arity
- **Think about this !!!**
```
  Can we use currying feature :
    >> to achieve the rx.Observable's operator chaining ?
```


##### Combining closures
- Have look at below example:

```java

  def numbers = (1..1000)
  def result = numbers
    .findAll{ it % 2 == 0 }
    .findAll{ it > 100 }
    .sum()

```

- We know that above is **not efficient** as it loops multiple times.
- However, we cannot combine the closures like we did earlier.
- The solution lies in applying a **partial application / function**

```java

  Closure<Boolean> combiFilters(final Closure<Boolean>... filters){
    Closure<Boolean> filtersCombine = {
      Integer num, Closure<Boolean>... allFilters ->
        allFilters*.call(num).every()        
    }

    return filtersCombine.rcurry(filters)   // note the use of rcurry
  }

  def numbers = (1..1000)
  def even = { it % 2 == 0 }
  def over100 = { it > 100 }
  def byCriteria = combiFilters(even, over100)
  def result = numbers
    .findAll(byCriteria)
    .sum()

```

- Alternative readable version that **does not** make use of curry

```java

  Closure<Boolean> combiFilters(final Closure<Boolean>... filters) {
    return { Integer i ->
      filters*.call(i).every()
    }
  }

  def numbers = (1..1000)
  def even = { it % 2 == 0 }
  def over100 = { it > 100 }
  def byCriteria = combiFilters(even, over100)
  def result = numbers
    .findAll(byCriteria)
    .sum()

```

##### Iteration: Internal vs. External

```java

  // old style
  def names = ["hello", "world", "universe"]
  def namesUpper = []

  for(String name : names) {
    namesUpper << name.toUpperCase()
  }

  // streaming style
  namesUpper = []
  namesUpper.each{ name ->
    name.toUpperCase()
  }

  // groovy style - reusable
  namesUpper = []
  def upperWay = { String str -> str.toUpperCase() }
  namesUpper.collect(upperWay)

  // groovy style - non reusable
  namesUpper.collect(it.toUpperCase())

```


##### Re-usability by dividing the logic into filters & transformers

```java

  // a default Closure, used in internal iteration
  Integer sum(
    final Collection<Integer> source,
    final Closure<Boolean> filter = { it }) {
      return source.findAll(filter).sum()
  }

  // use - 1 --via method calls
  def nums = (1..100)
  def all = sum(nums)
  def over20 = sum(nums) {
    it > 20
  }

  // use - 2 --via method calls
  def nums = (1..200)
  def over20Filter = {
    it > 20
  }
  def result = sum(nums, over20Filter)

  // use - 3 --via closures calls
  def nums = (1..300)
  def over20Sum = this.&sum.rcurry { it > 20 }
  def result = over20Sum(nums)
```


##### Case for streams !!!
- How would you make the following code efficient ?

```java

  def numbers = (1..10)
  def mulBy2 = { it * 2 }
  def byEven = { it % 2 == 0 }
  def addThree = { it + 3 }

  def result = numbers
    .findAll(byEven)
    .collect(mulBy2 >> addThree)

```

- The above code has 2 iterations. Can it be reduced ?
- Yes. But the resulting code may not be readable & reusable.
- However, what if this ugly code is abstracted away into a reusable class ?
  - Well the JDK 8 Stream API is somewhat similar.
  - The main idea is **lazy evaluation**.
  - Something similar to builder pattern.
- Some advanced streaming requirements:
  - combine more than one stream
  - combine more than one filter
  - combine more than one transformer



##### Using [groovy-stream](http://timyates.github.io/groovy-stream/) lib

```java

  def result = Stream
    .from(1..10)
    .filter { it % 2 == 0 }
    .map { it * 2 }
    .collect()

  // Iterator
  def iter = [hasNext: {true}, next: { x++ }] as Iterator
  def iStream = Stream.from(iter)
  iStream.until{ it > 2 }.collect()

  // More overloaded versions
  def counter = Stream.from({ x++ }).using(x: 1)
  counter.take(2).collect()

  // from another Stream
  def aliterStream = Stream.from(iStream)
```


##### Closures & others
- Closures & state

```java

  // wrong way
  def state = new State(discount:50)
  def closure = { price ->
      price * (state.discount / 100)
  }

  // Why?
  // invoking closure(100) after mutating state gives different values
  // This goes against the mathematics function's principles.

  // correct way
  def closure = { State st ->
      return { price ->
          price * (st.discount / 100)
      }
  }

```


##### Groovy class with pretty toString
- This is a kind of un-apply method i.e. decomposing the object into its properties.

```java

  String toString() {
     _toString().replaceAll(/\(/, '(\n\t').replaceAll(/\)/, '\n)').replaceAll(/, /, '\n\t')
  }

```


##### Groovy class with @Immutable annotation
- Class is automatically made final.
- Properties of the class must be of an immutable type.
- Properties become private final with backing getters.
- A **map based constructor** is provided i.e. you can set properties by name.
- A **tuple style constructor** is provided i.e. set properties in the same order as declaration.
- equals, hashcode & toString methods are provided.
- You can **avoid the need for 2 classes**:
  - Typically, we would want an entity class as well as its builder class.
  - Instead go for the single @Immutable Entity Class.


##### Groovy & Sequence Comprehensions
- To learn more about this go through below:
  - [Javaslang](http://www.javaslang.io/)  
  - [jOOL](https://github.com/jOOQ/jOOL)
  - [RxJava](http://reactivex.io/)
- In short, one does not like to iterate over multiple collections over multiple loops.
  - In addition, this tends to introduce many local mutating state variables.
  - NOTE: Mutation is not bad but one needs to delegate it:
    - to the underlying libraries, or
    - to the language itself.


##### From template pattern to just closure functions

```java

  // a probable template pattern in java
  abstract class Make {
    protected abstract String step1(String input);
    protected abstract String step2(String input);

    public final String make(String input){
      String output = step1(input);
      return step2(output);
    }
  }

  // in groovy, the template becomes a higher order function
  Closure<String> make = {
      Closure<String> step1,
      Closure<String> step2,
      String input ->
        step2(step1(input))        
  }

```

- The stress should be given to **higher order function**.
- Template pattern has suddenly become functional with all functional goodies.


##### From strategy pattern to just closure function

```java

  List<Program> findPrograms(List<Program> progs, Closure<Boolean> strategy) {
    progs
      .findAll(strategy)
      .asImmutable()
  }

```

- The stress here is again on **function** i.e. a closure function than a pattern.


##### Handling nulls
- The null value in groovy is not null of java.
- null.getClass() == org.codehaus.groovy.runtime.NullObject
- **How does it help ?**

```java

  // collections are safe
  List<String> doSomething(List<String> words) {
      return words
          .findAll { it.startsWith('j') }
          .collect { it.toUpperCase() }
  }

  // usage
  def cities = null
  def names = ['john', 'jeronimo', 'james']

  def citiesResult = doSomething(cities)
  // citiesResult == []

  def namesResult = doSomething(names)
  // namesResult == ['JOHN', 'JERONIMO', 'JAMES']

```

- Should developers use **findAll** & **collect** to avoid **NullPointerException** ?
- NOTE: **Anything** in groovy can use **collect() & hence method chain** !!!
- Groovy provides the **elvis** operator for providing default values.
- Groovy also provides **Optional** pattern


##### Groovy & Option

```java

  Option<ImmutableVideo> result =
    Option
      .from(video)
      .map { ImmutableVideo v ->
          new ImmutableVideo(
              name: "${v.name}-processed",
              type: v.type)
      }

```


##### Monad === a way to represent & manipulate computations
- Monad via **with** & safe operator **?.**
```java

  // a custom Monad example
  def map(Object o, Closure func){
    o?.with(func)
  }

  def result =  map(input) {String xyz ->    
    ...
  }

  // collect that transforms each item in a collection into something else
  // seems like a Monad isn't ?
  def result = input.collect { String xyz ->
    ...
  }

  // combinations are also possible
  def result = input.collect { String xyz ->
    map(xyz) { String xyz ->
      ...
    }
  }
```


##### MayBe Monad
- MayBe object has two children: Maybe.Just & Maybe.Nothing


##### Either Monad
- Can represent a correct or error

##### Try & TryOrElse Monad
-
