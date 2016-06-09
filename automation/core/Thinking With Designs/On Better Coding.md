##### References
- https://www.infoq.com/news/2016/06/programmers-write-better-code
- file:///C:/Users/amit/Downloads/QConLondon2016-SylvanClebsch-UsingPonyforFintech.pdf
- http://tutorial.ponylang.org/
- https://tech.esper.com/2014/07/30/algebraic-data-types/


##### Belief
> A good programmer is one who reads others' code.
> A good author is one who reads others' books.
> A good hacker is one who steals others' ideas than copying the source.


##### Introduction
Readers may find this article to be a collage of information collected from
various references. The entire credit goes to these geniuses who articulated
their thoughts into above blog links. What I have tried here is to **connect the
dots** so that writing programs or thinking with designs in any language becomes
palatable.


##### Some analysis of good projects
> They also realized some projects where successful and wanted to know how to
> extract the goodness and make it applicable on a wider scale. For me, some of
> the standout points were the realizations that software development is iterative,
> experimental/learning focused, practitioner lead, and best done in small teams.

> One of the biggest challenges we have with software development is taming complexity
> as the size of an application grows. The more coupling we have between objects,
> components, modules, or systems, the more we experience many consequences. These
> consequences include but are not limited to difficulty of modification,
> propagation of failure, inability to scale because of contention, and performance issues
> due to dependent actions. Low and loose coupling in time, space, and implementation
> are essential to scale and resilience. Coupling is well illustrated by Connascence
> whereby a change in one module/component causes a change in another.


##### Algebraic Data Types
- Made up of 2 components:
  - Products
  - Variants
- **Products** are also known as
  - Tuples
  - Records
  - Structs
- **Variants** are also known as
  - Tagged Unions
  - Sums
  - Coproducts
- This is an expressive basis for modeling different domains.
- We can have multiple constructors each with multiple arguments.

> The ability to construct above with ease & further using them during logic building
> is what makes the difference. In Java, you would probably create classes along with
> interfaces to create Products. This is a huge programming effort before we can
> go for logic building. The notion of Variants seems to be a herculean task in
> Java & similar languages. Imagine creating a type which can either be property A
> or property B. Avid readers would have got the context by comparing with either,
> MayBe, etc operators. Variants can be any of multiple possibilities.



##### Emulating variants in C - An example
```code
  enum Tag { Left; Right }

  struct Either {
    enum Tag tag;
    union {
      int left;
      char* right;
    }
  }
```

##### Emulating variants in c & java
- In c language, idea is to check the tag every time you read the value.
  - They are called as tagged unions.
  - Disadvantage - Susceptible to human errors.
- In Java, the visitor design pattern serves a similar role.
  - refer - [Visitor Pattern](http://mishadoff.com/blog/clojure-design-patterns/#visitor)
  - Disadvantage - Lot of coding to get the business modeling right.

> If you reflect on the Visitor pattern, we need to change the Visitor contract,
> the moment we add **new types** of visitors. This forces the compile time static
> checks & we are near to the concept of pattern matching with variants. The
> visitor pattern exists because languages like Java use only single dispatch.


##### Pattern matching vs. If Else -- Elixir way
```Elixir

  defmodule Test do
    def fib(0), do: 1
    def fib(1), do: 1
    def fib(n) do
      fib(n-1) + fib(n-2)
    end
  end
```

##### So you think golang is cool. Really !!
- http://crufter.com/2014/12/01/everyday-hassles-in-go/
- http://yager.io/programming/go.html
- http://bravenewgeek.com/go-is-unapologetically-flawed-heres-why-we-use-it/


##### Using memory effectively
- http://developers.redhat.com/blog/2016/06/01/how-to-avoid-wasting-megabytes-of-memory-a-few-bytes-at-a-time/?utm_content=buffer6b32b&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer


##### Interesting Language - Elixir
- http://www.evanmiller.org/elixir-ram-and-the-template-of-doom.html?utm_campaign=elixir_radar_47_com_banner_webinar_phoenix&utm_medium=email&utm_source=RD+Station
