##### Introduction
This is all about understanding the essence of functional programming. At the
end of this article we shall see if we understood how logic built using functional
techniques are effectively managed than that of imperative programming model. We
shall also understand the differences between functional, reactive, compositional
etc programming models.


###### References
- http://www.slideshare.net/borgesleonardo/functional-reactive-programming-compositional-event-systems
- http://guide.elm-lang.org/
- http://fsharpforfunandprofit.com/
- https://www.infoq.com/presentations/fp-design-patterns
- http://blog.javaslang.io/functional-data-structures-in-java-8-with-javaslang/


##### What is FRP ?
- Functional Reactive Programming
- How is it different from  Reactive Programming ?
  - We shall get to know as I try to understand better.


##### Quotes that challenges us to understand more !!!
- Taming asynchronous workflows with functional reactive programming
- Taming asynchronous workflows with compositional event systems


##### Quotes that help us understand !!!
- from ```Mario Fusco```
> The goal of functional programming is not a world without side-effects or
> mutability, but one where we don't have to directly deal with them.


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


##### Benefits using Types
- Use types to **represent constraints**
```java
  // Types represent constraints on input & output.
  type Suit = Club|Diamond|Spade|Heart
  type String50 = //non-null, not more than 50 chars
  type EmailAddress = //non-null, must contain @
```

- Types are cheap
```java
  // New types can be composed from existing types
```

- Use types to indicate errors
```java
  // Output types as error codes
```

- Types can represent business rules
```java
  type StringTransformer = string->string
  type GetCustomer = CustomerId->Customer option
```

- Use types instead of inheritance
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

- Use types for state machine


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
