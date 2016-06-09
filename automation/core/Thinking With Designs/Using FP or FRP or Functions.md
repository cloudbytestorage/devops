###### References
- http://www.slideshare.net/borgesleonardo/functional-reactive-programming-compositional-event-systems
- http://guide.elm-lang.org/
- http://fsharpforfunandprofit.com/
- https://www.infoq.com/presentations/fp-design-patterns
- http://blog.javaslang.io/functional-data-structures-in-java-8-with-javaslang/
- http://typelevel.org/cats/tut/freemonad.html
- http://degoes.net/articles/modern-fp



##### Belief
> A good programmer is one who reads others' code.
> A good author is one who reads others' books.
> A good hacker is one who steals others' ideas than copying the source.


##### Introduction
Readers may find this article to be a collage of information collected from
various references. The entire credit goes to these geniuses who articulated
their thoughts into above blog links. What I have tried here is to **connect the
dots** so that writing programs or thinking with designs in any language becomes
palatable. The sections will be very pragmatic & gear more towards logic than
theory. I shall try to explain the theory whenever I get the easiest yet effective
meaning.



##### Tips while programming
- Complexity is your enemy.
  - Code that is hard to read.
  - Code that is hard to understand.
- Static typing so that refactoring need not be feared.



##### What is FRP ?
- Functional Reactive Programming
- How is it different from  Reactive Programming ?
  - We shall get to know as I try to understand better.


##### Quotes that challenges us to understand more !!!
- Taming asynchronous workflows with functional reactive programming
- Taming asynchronous workflows with compositional event systems


##### Quotes that help us understand !!!

  > The goal of functional programming is not a world without side-effects or
  > mutability, but one where we don't have to directly deal with them.
  > ```Mario Fusco```


  > In modern FP, we shouldn’t write programs — we should write descriptions of
  > programs, which we can then introspect, transform, and interpret at will.
  > ```http://degoes.net/articles/modern-fp```


##### Imperative vs. Functional debate !!!
- On imperative programming:
  - It implements computations as a series of actions
  - These actions keep on modifying program state
- On functional programming:
  - It describes what we want to do.
  - It **does not talk about how** we want it to be done.
  - There is no variables with local state


##### Core principles of FP design
- Learn from mathematics.
- In a maths function the input & output values are unchanged.
- A maths function always gives same output for a given input value.
- A maths function has no side effects.
- **Types are not classes.**
- **Functions are things.**
  - It is a standalone thing, not attached to any class.
- Compose from top till bottom.


##### Benefits using Functions
- A pure function is easy to re-factor.
- It is lazily evaluated
- It can be cache-able i.e. memoization
- No order dependencies
- It can be executed parallelized.


##### Use types to **represent constraints**
```java
  // Types represent constraints on input & output.
  type Suit = Club|Diamond|Spade|Heart
  type String50 = //non-null, not more than 50 chars
  type EmailAddress = //non-null, must contain @
```

##### Types are cheap
- New types can be composed from existing types
- Use types to indicate errors
  - Output types as error codes
- Types can represent business rules

  ```java

    type StringTransformer = string->string
    type GetCustomer = CustomerId->Customer option

  ```

##### Use types instead of inheritance

  ```java

    type PaymentMethod =
    | Cash
    | Cheque
    | Card

    // vs. OO version
    interface iPaymentMethod {}
    class Cash implements iPaymentMethod {}
    class Cheque implements iPaymentMethod {}
    class Card implements iPaymentMethod {}
  ```

##### Use types for state machine


##### Monoid === Associativity
- This is not a Monad.
- It means you can combine elements from a set.
- This set can be used in a binary operation (i.e. arity = 2) in any order.
- As the computations can be executed in any order, they can be executed in parallel
- & the results can be combined
- ```NOTE``` When you talk of parallel executions make sure that the structures are immutable.
- **Associativity** comes in handy when we talk about parallelism.
- You can scatter the operations through cores of your computer & join the results.


##### Functor
- It represents a wrapper with an ability.
- The ability to apply a function to elements wrapped in the container
- Functions are applied to the container & not against the value directly


##### Monad
- Pure way to represent & manipulate computations
- In functional world **bind & return === monad**
- bind receives a wrapped value & return returns a wrapped value

##### Free Monad
- An approach to club the sequential computations in a data structure
  - Hence, it can be inspected
  - & can be interpreted later
- Lets us model arbitrary programs as a sequence of algebraic operations.
- Its called free as we get a monad for free.
- Build monad from any functor
- A practical way to:
  - stateful computations as data
  - recursive computations
  - build embedded DSL
  - retarget a computation to another interpreter




##### Function that can decompose an object === Un-apply
- Accept an instance & return the parts
- If you understand the value of toString & coercion you will recognize this as an important feature.
- The use cases I can think of are:
  - un-apply for logging,
  - un-apply to a json format for further serialization.


##### Throwing exceptions is a side-effect
- They break the control flow.
- Check the use of ```Try<T> @ javaslang```

##### What is a Persistent Data Structure ?
- It preserves the previous version of itself when being modified.
- Hence if is kind of immutable.
- Some of these structures also allow updates as well as queries on any version.
- Many operations perform small changes & thus full copy will not be efficient.
- Hence the copying needs to diff the versions & share as much as possible.


##### OCaml or F# in java
- https://engineering.vena.io/2016/05/30/ocaml-mimicry-in-java-jocaml/?utm_content=bufferaf1ed&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer
