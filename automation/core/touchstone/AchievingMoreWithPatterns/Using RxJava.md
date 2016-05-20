#### Understanding RxJava
Most of these have been taken from the references mentioned in this article.
The entire credit goes to these good fellas. What I have tried to do is to
categorize them, to make it easy for my understanding.

##### References
- http://blog.danlew.net/2015/03/02/dont-break-the-chain/
- https://github.com/ReactiveX/RxJava/wiki/
- http://reactivex.io/documentation/observable.html
- http://blog.danlew.net/2015/07/23/deferring-observable-code-until-subscription-in-rxjava/
- http://blog.freeside.co/2015/01/29/simple-background-polling-with-rxjava/
- https://medium.com/@v.danylo/server-polling-and-retrying-failed-operations-with-retrofit-and-rxjava-8bcc7e641a5a#.ygzqdf1of
- http://stackoverflow.com/questions/34943734/using-of-skipwhile-combined-with-repeatwhen-in-rxjava-to-implement-server-po/34948978


##### Observer vs. Observable
- In ReactiveX an observer subscribes to an Observable
- An observer **reacts** to the item or sequence of items emitted by Observable
- This reaction pattern facilitates concurrent operations.
- In other words, this enables non-blocking code implementations.
- In ReactiveX many instructions may execute in parallel, &
	- many instructions may execute in parallel, &
	- their results are later captured by observers
- Rather than invoking methods:
	- A pattern is in-place to retrieve & transform the data.
	- This is done via an Observable.
	- A observer is subscribed against an Observable.
	- Alternatively, Observable sends notifications to its observers.


##### ReactiveX Observable vs. Builder pattern
- Most operators on an Observable return an Observable.
- This facilitates chaining of operators.
- Each operator in the chain modifies the Observable that results from previous operation.
- Observable operators do not operate on the Observable that originates the chain.
- In Builder pattern the **same** object gets modified during the build.
- In Builder pattern, the order of operators does not matter.
- In Observable the order of operators matters.

##### So many operators !!!
- At times it will be daunting to figure out all the available operators.
- Below [link](http://reactivex.io/documentation/operators.html) will help:
```
 http://reactivex.io/documentation/operators.html
```


##### Understand RxJava through code snippets
- combineLatest
```java

	// example 1
	Observable.<A, B, R> combineLatest(observableA, observableB, combineFunc)
		.toBlocking()
		.forEach(actionFunc);

	// example 2
	Observable.<A, B, R> combineLatest(observableA, observableB, combineFunc)		
		.subscribe(actionFunc);

	// where
	// A, B & R are java classes
	// Func2<A, B, R> combineFunc = new Func2<A, B, R>() {...}
	// Action1<R> actionFunc = new Action1<R>() {...}
	// combines the latest emitted value from each source observable & emit the
	// resulting value via the combineFunc.

	// signature & implementation
	public static final <T1, T2, R> Observable<R> combineLatest(
			Observable<? extends T1> o1,
			Observable<? extends T2> o2,
			Func2<? super T1, ? super T2, ? extends R> combineFunction) {
				return combineLatest(
					Arrays.asList(o1, o2),
					Functions.fromFunc(combineFunction));
	}
```


##### A positive side-effect. The code is clear in its intent.
- One can verify the intent of the code by just browsing the code
- In other words, you can see how data is transformed through a series of operators:
```java
	Observable.from(someSource)
		.map(data -> manipulate(data))
		.subscribeOn(Schedulers.io())
		.observeOn(AndroidSchedulers.mainThread())
		.subscribe(data -> doSomething(data));    
```
- Above shows the use of subscribeOn() and observeOn() to process data in a worker thread.
- Finally use of subscribe() on the main thread.

##### How to implement a custom sequence operator ?
- Create a class that implements ``` Operator<T> ```.
- Use it via lift method.
- In case of Groovy or Xtend, one can create extensions for the custom operators.
  - Creating extensions help in providing fluent API to an Observable instance.
```java
	// Xtend
	Observable.just("Foo").myOperator
	// vs. Java
	Observable.just("Foo").lift(new MyOperator)
```

##### What naming conventions should be followed to build a custom operator ?
- Refer the source code of Observable.java
```java
	// refer to these code snippets

	public final Observable<T> take(final int count) {
		return lift(new OperatorTake<T>(count));
	}

	public final Observable<T> single() {
			return lift(OperatorSingle.<T> instance());
	}
```

##### Are there any best practices to implement a custom operator ?
- If possible create new operator by composing existing ones.
- Refer the source code of Observable.java
```
 first() is implemented as ``` take(1).single() ```.
 first(predicate) is implemented as ``` takeFirst(predicate).single() ```.
 takeFirst(predicate) is implemented as ``` filter(predicate).take(1) ```.
```
- Refer to operators exposed in other language implementations of ReactiveX.
	- It may be possible that your requirement is build in other language(s).
	- If yes, then implement the same in your preferred language.


##### What are the best practices of error handling in a custom operator ?
- If operator accepts functions, e.g. predicates then:
  - these may be the source of exceptions.
- These exception should either be:
  - caught & notified to subscribers via onError() call.
	- or rethrow them if fatal.
- Refer the source code of ``` OperatorFilter<T>.java ```.
```java

 //Below is OperatorFilter<T>.FilterSubscriber<T>'s onNext() implementation:

 public void onNext(T t) {
	 boolean result;

	 try {
		 result = predicate.call(t);
	 } catch (Throwable ex) {
		 Exceptions.throwIfFatal(ex);
		 unsubscribe();
		 onError(OnErrorThrowable.addValueAsLastCause(ex, t));
		 return;
	 }

	 if (result) {
		 actual.onNext(t);
	 } else {
		 request(1);
	 }
 }
```


##### How to implement a custom transformational operator ?
- Create a class that implements ``` Transformer<T, R> ```.
- Use this new transformer via compose method.


##### Observable & comparison of its creational operators
```java
	// Assume a POJO with a instance variable value has below method

	public Observable<String> valueObservable() {	// (1)
		return Observable.just(value);
	}

	// vs.

	public Observable<String> valueObservable() {	// (2)
	  return Observable.create(subscriber -> {
	    subscriber.onNext(value);
	    subscriber.onCompleted();
	  });
	}

	// vs.

	public Observable<String> valueObservable() {	// (3)
		return Observable.defer(() -> Observable.just(value));
	}

```
- (1) Makes sense if valueObservable is invoked after setting the value.
- (2) valueObservable emits current value upon subscription (not creation).
- (3) None of code inside defer is executed until subscription.


##### Compare Observable's just vs. from
- Observable.just([1, 2, 3, 4, 5]) vs. Observable.from([1, 2, 3, 4, 5])
- Observable.just will emit the entire array as a single item
- Observable.from will emit each value within the array


##### Does null have any role to play in Observable ?
- A null is a valid value that can be emitted by an Observable.
- Imagine using null value as the criteria to complete streaming of events.
- If we want the Observable to not emit any values, then we need to use Empty operator.


##### Case for using flatMap operator
- Consider below piece of code
```java
	// verbose code

	Observable.from(1, 2, 3, 4)
		.map(id -> xyzService.getOrderItems(id))
		.map(orderItems ->
			orderItems.stream()
			.map(item -> item.handled())
			.collect(Collectors.toList()))
		.subscribe(orderItems -> {
			for(OrderItem item : orderItems){
				system.out.println(item.toString())
			}
		})
```
- Now compare above with below piece of code
```java
	// cleaner and flatter code via flatMap
	// flatMap turns the collection of items into an Observable item & joins to
	// the original stream

	Observable.from(1, 2, 3, 4)
		.map(id -> xyzService.getOrderItems(id))
		.flatMap(Observable::from)
		.subscribe(orderItem -> system.out.println(orderItem.toString()));
```
- If you want to preserve the ordering of upstream Observable in the downstream:
	- then use concatMap instead of flatMap


##### How to fit ReactiveX's Observables with existing types / libraries ?
- It will be convenient to have Observable types throughout the lifespan of a stream.
- Observable operators with its functional power can create
	- readable,
	- dry &
	- testable code
- Iterables can be thought of as synchronous Observables.
- Futures can be thought of as Observable that emit a single item.
- Rx implementations allow us to convert certain language specific objects into Observables.
- In RxJava from operator can convert below into a Observable.
	- A Future into Observable,
	- An Iterable into Observable,
	- An Array into Observable.
- [RxJavaAsyncUtil](https://github.com/ReactiveX/RxJavaAsyncUtil) can do below:
	- actions into Observables,
	- callables into Observables,
	- functions into Observables,
	- runnables into Observables
- [RxJavaString](https://github.com/ReactiveX/RxJavaString) can do below:
	- Convert a stream of characters or a Reader into an Observable
	- The Observable emits byte arrays or Strings.


##### Which one to use: Observer or Subscriber ?
- Observer is a mechanism to receive push based notifications from Observables.
- Subscriber is same as an Observer & also permits manual unsubscribing.
- Subscriber extends from an Observer.
- Subscriber has back pressure semantics // TODO write more


##### Should we check isUnsubscribed() in the subscriber implementations ?
- It is good practice to check the observer’s isUnsubscribed state
- so that Observable can stop emitting items or
- doing expensive calculations when there is no longer an interested observer.
- Also check for try catch blocks in the subscriber's implementation code.


##### Example of polling using RxJava
- Assume a REST service that returns a job id after execution a request.
- The status of request needs to be polled every X seconds to verify if the request:
	- succeeded or
	- failed or
	- is in-progress
```java
	// TODO provide the sample code
	// TODO https://medium.com/@v.danylo/server-polling-and-retrying-failed-operations-with-retrofit-and-rxjava-8bcc7e641a5a#.wmncikjbs
```


##### TODO
- Notification is an object that is sent to an Observable
	- It can be a T, or a Throwable or a Kind
- BlockingObservable is used for testing or demo purpose. Not for prod use.
- AbstractOnSubscribe helps you build Observable sources
	- one at a time
	- supports un-subscription and backpressure
- SubscriptionState features counters that may help implement a state machine
- SyncOnSubscribe
	- Provides a generic way to fill data by iterating over a potential stateful function.
		- e.g. reading data of a channel, a parser, etc.
	- If data comes from an asynchronous/potentially concurrent source then consider using below:
		- AsyncOnSubscribe<T>
- AsyncOnSubscribe
	- Fill data to an Observable from a source
	- The source is typically asynchronous (RPC, external services, etc)
	- Improvement over Observable.create(OnSubscribe)
	- This variant of OnSubscribe allows for asynchronous processing of requests
	- Provides means to manage back pressure
