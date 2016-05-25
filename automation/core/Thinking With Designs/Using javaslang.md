##### References
- http://blog.javaslang.io/functional-data-structures-in-java-8-with-javaslang/
- http://blog.javaslang.io/synchronizedthis/

##### Queues @ javaslang
```java

  Queue<Integer> queue = Queue.of(1, 2, 3);

  // = (1, Queue(2, 3))
  Tuple2<Integer, Queue<Integer>> dequeued = queue.dequeue();

  // = Some((1, Queue()))
  Queue.of(1).dequeueOption();

  // = None
  Queue.empty().dequeueOption();

  // = Queue(1)
  Queue<Integer> queue = Queue.of(1);

  // = Some((1, Queue()))
  Option<Tuple2<Integer, Queue<Integer>>> dequeued = queue.dequeueOption();

  // = Some(1)
  Option<Integer> element = dequeued.map(Tuple2::_1);

  // = Some(Queue())
  Option<Queue<Integer>> remaining = dequeued.map(Tuple2::_2);

```

##### Streams in Java 8 vs. javaslang
```java

  // = ["1", "2", "3"] in Java 8
  Arrays.asList(1, 2, 3)  
    .stream()
    .map(Object::toString)
    .collect(Collectors.toList())

  // = Stream("1", "2", "3") in Javaslang
  Stream.of(1, 2, 3).map(Object::toString)

```
- The debate is not preference over a particular syntax but rather below:
> The comparison is about expressions that return a value over statements that
> return nothing.

##### Statements add noise & deviate the logic from being cohesive
```java
  String join(String... words) {  
    StringBuilder builder = new StringBuilder();
    for(String s : words) {
        if (builder.length() > 0) {
            builder.append(", ");
        }
        builder.append(s);
    }
    return builder.toString();
  }

  //vs.

  String join(String... words) {  
    return List.of(words)      
      .intersperse(", ")
      .fold("", String::concat);
  }

  // vs.

  List.of(words).mkString(", ");
```

##### Maps in Javaslang
- The **Map uses Tuple2** which is already a part of javaslang.
```java

  // = (1, "A")
  Tuple2<Integer, String> entry = Tuple.of(1, "A");

  Integer key = entry._1;  
  String value = entry._2;

  // Check how easy it is to return multi-valued return types
  // = HashMap((0, List(2, 4)), (1, List(1, 3)))
  List.of(1, 2, 3, 4).groupBy(i -> i % 2);

  // = List((a, 0), (b, 1), (c, 2))
  List.of('a', 'b', 'c').zipWithIndex();
```


##### Designing by reading javaslang code
- A ```coding pattern``` common in javaslang !!!
```java

  // a possible Javaslang Future implementation

  interface Future<T> {

      static <T> Future<T> of(CheckedSupplier<T> computation) {
          // ...
      }

      Option<Try<T>> getValue();

      boolean isComplete();

      void onComplete(Consumer<? super Try<T>> action);

  }

```
- Contract via java interface & java generic type T.
- Creation via static factory.
- Get value if present.
- Flag to check status of computation.
- Registration of asynchronous callback.


##### What is structural pattern matching ?
- Do not confuse this with pattern matching.
- It allows to de-construct object hierarchies.
- It allows to use different object with similar structures to be used as function parameters.


##### Structural pattern matching in javaslang
- **$()** - wildcard pattern
- **$(value)** - equals pattern
- **$(predicate)** - conditional pattern
- @Patterns & @Unapply help in decomposing the objects.
- A set of default predicates are available in javaslang.
- A helper function exists to perform side-effects.
