##### References
- http://www.lihaoyi.com/post/StrategicScalaStylePrincipleofLeastPower.html


##### Tips while programming
- Complexity is your enemy.
  - Code that is hard to read.
  - Code that is hard to understand.
- Static typing so that refactoring need not be feared.

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
