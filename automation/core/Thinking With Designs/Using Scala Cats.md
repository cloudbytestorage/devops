##### References
- http://typelevel.org/cats/tut/freemonad.html


##### Free Monad
- cats-free module
- Free[_]
- A construction that allows to build very simple Monad from any functor
- Can compose the ADTs


##### Free Monad to build a key-value store DSL
- **Design**
  - DSL will be a sequence of operations
  - computation to be pure immutable value
  - separate the creation & execution of the program
  - support many different methods of execution
- **DSL's grammar**
  - put, get, delete
- **ADT for the DSL's grammar**
  - Algebraic Data Type refers to closed set of types
  - These types can be combined to build complex, recursive values

  ```java
    sealed trait KVStore[A]

    // put returns **nothing** i.e a Unit
    case class Put[T](key: String, value: T) extends KVStoreA[Unit]

    // get returns a **T value**
    case class Get[T](key: String) extends KVStoreA[Option[T]]

    case class Delete(key: String) extends KVStoreA[Unit]
  ```

- **Free your ADT**

  ```java
    - i.e. ADTs are lifted as functions via Free
    - use these functions that return Free structure
    - Hence, we use the monads to define, compose smart algorithms
  ```
