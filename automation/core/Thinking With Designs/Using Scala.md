##### References
- http://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html
- http://typelevel.org/cats/tut/freemonad.html#what-is-free-in-theory
- http://perevillega.com/understanding-free-monads


##### Introduction
Readers may find this article to be a collage of information collected from
various references. The entire credit goes to these geniuses who articulated
their thoughts into above blog links. What I have tried here is to **connect the
dots** so that writing programs or thinking with designs in any language becomes
palatable.


##### Immutability

```java

  // good
  val x = if(myBoolean) expr1 else expr

  // bad
  var x: ExprType = null
  if(myBoolean) x = expr1 else x = expr

```

- limit the scope of mutability. It should not leak across everywhere
- No double-mutability

  ```java

    // bad java
    ArrayList<Int> myList = new java.util.ArrayList<Int>()

    // good java
    final ArrayList<Int> myList = new java.util.ArrayList<Int>()

    // bad scala
    var myList = mutable.Buffer[Int]

    // good scala
    val myList = mutable.Buffer[Int]

  ```


##### From an OOPs approach to an ADT based one
```java

  object Orders {
    type Symbol = String
    type Response = String
    def buy(stock: Symbol, amount: Int): Response = ???
    def sell(stock: Symbol, amount: Int): Response = ???
  }

  // **versus**

  // A functor like
  sealed trait Orders[A]

  // a definition to buy
  // but cannot do anything other than acting as a placeholder
  case class Buy(stock: Symbol, amount: Int) extends Orders[Response]

  // a definition to sell
  case class Sell(stock: Symbol, amount: Int) extends Orders[Response]


```


##### More ADTs --Algebraic Data Type
```java

  /* Handles user interaction */
  sealed trait Interact[A]
  case class Ask(prompt: String) extends Interact[String]
  case class Tell(msg: String) extends Interact[Unit]

  /* Represents persistence operations */
  sealed trait DataOp[A]
  case class AddCat(a: String) extends DataOp[Unit]
  case class GetAllCats() extends DataOp[List[String]]

  /* Audit related operations */
  sealed trait Audit[A]
  case class UserActionAudit(user: UserId, action: String, values: List[Values])
    extends Audit[Unit]
  case class SystemActionAudit(job: JobId, action: String, values: List[Values])
    extends Audit[Unit]

  /* Messaging related */
  sealed trait Messaging[A]
  case class Publish(channelId: ChannelId, source: SourceId, messageId: MessageId, payload: Payload)
    extends Messaging[Response]
  case class Subscribe(channelId: ChannelId, filterBy: Condition) extends Messaging[Payload]

```


##### Optimizing your scala code
- http://www.lihaoyi.com/post/MicrooptimizingyourScalacode.html



##### Designing a DSL
- https://scalerablog.wordpress.com/2016/05/30/scala-one-language-to-rule-them-all-ii/




##### Akka Streams
- http://www.measurence.com/tech-blog/2016/06/01/a-dive-into-akka-streams.html



##### Akka & Distributed, Concurrent, Fault Tolerant systems
- https://blog.eero.com/eero-at-scale-4636deef418c#.qtjarvghv



##### Binary Encoding
- http://www.martinseeler.com/developing-efficient-bianry-file-protocol-with-scodec-and-akka-streams.html
