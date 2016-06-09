##### References
- http://learnyouahaskell.com/introduction#about-this-tutorial
- https://github.com/Frege/frege
- http://mariogarcia.github.io/functional-groovy/#_functional_patterns


##### Note
> I shall mention the syntax of Haskell in this article, unless i find these
> two languages need individual pages.

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

##### What are its differentiating features ?
- purely functional
- strong static type system
- global type inference
- lazy evaluation


##### Functor in Haskell
```Haskell

  class Functor f where
    fmap :: (a -> b) -> f a -> f b

  // can build a new instance of functor type
  // fmap method receives a function
  // fmap transforms an object of type a to another object of type b
  // It also receives a functor of type a & returns a functor of type b

```


##### ADT in Haskell
```



```
