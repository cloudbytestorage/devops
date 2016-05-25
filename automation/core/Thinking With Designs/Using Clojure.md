##### Using Clojure
This is an attempt to understand the benefits of LISP programming model. This
will provide a way to understand & then apply these programming practices
on our logic.

##### References
- http://clojure.org/reference/reader
- http://www.braveclojure.com/introduction/
- http://clojure.org/guides/spec


##### Code as Data === Data as Code
- Clojure program === Clojure data struture

##### Symbols
- ```/``` is used to separate the namespace from the name
- ```.``` is used one or more times to represent a fully qualified class name
- ```:``` is used to represent keywords.
  - e.g. :das, :person/name
- keyword beginning with ```::``` is resolved in current namespace.
  - e.g. in person namespace, ::name is read as :person/name
- Now compare the use of ```:``` with maps & sets
  - {:a 1 :b 2} __or__ {:a 1, :b 2}
  - #{:a :b :c}
- ```#``` used for sets
  - also used for invoking constructors

##### Constructors with vectors or maps
- Constructors can be invoked with vector representation.
- Constructors can be invoked with map representation.

##### Why we find Clojure logic to be so different than our usual Java logic ?
- Lets understand various Clojure basics which will remove above notion:
- ```macro characters```
  - `form                 => (quote form)
  - \a                    => a character literal
  - \newline              => a newline representation
  - ;                     => a line comment
  - @form                 => (deref form)
  - ^{:a 1 :b2} [1 2 3]   => attaches the 1st form with the next form
  - #`x                   => (var x)
  - #()                   => (fn [args] (..))
  - %n    designates the nth argument


#####
