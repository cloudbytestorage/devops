##### Algebraic Data Types
Think these as enums with values attached. You will not be allowed to miss out
any values of these enums by the complier.

##### References
- https://spin.atomicobject.com/2016/05/11/adts-monads-ruby/?utm_content=buffer2bf29&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer
-


##### Some Samples
- definition
```F#
type GearSpeed =
  | Park
  | LowGear of int * double
  | Drive of double
```
- values
```F#
  Park              // parked
  Drive 45.0        // drive, 45 mph
  LowGear (1, 10.0) // first gear, 10 mph
  Drive 55.2        // drive, 55.2 mph
  LowGear (2, 20.0) // second gear, 20 mph
```
- pattern matching with **compilation benefits**
```F#
  let isStopped aGearSpeed =
  match aGearSpeed with
  | Park -> true
  | _ -> false

  // will not compile, missing Park case
  let getSpeed aGearSpeed =
  match aGearSpeed with
  | LowGear (_, speed) -> speed
  | Drive speed -> speed
```
