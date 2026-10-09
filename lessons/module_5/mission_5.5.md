---
index: 31
module: module_5
task: adaptive_speed
previous: proportional_control
next: art_of_debugging
---

# Mission 5.5 Adaptive Speed 

## Objective
Make the rover race-ready by implementing an Adaptive Speed algorithm that automatically slows down before corners using the `abs()` function.

![Advanced](https://img.shields.io/badge/Difficulty-Advanced-red)

## Introduction
Your Proportional Controller is stable, but it has a flaw: it drives at a constant `base_speed`. 
If you set the speed to `30`, the robot easily navigates sharp corners, but crawls agonizingly slowly on straightaways. If you increase the speed to `80`, it flies down the straights but crashes on the first sharp turn because it's going too fast to steer!

Think about real racing drivers. They don't press the gas pedal identically the whole track. They accelerate on the straights and hit the brakes *before* entering a turn. Today, we will teach your rover to do exactly that.

## Theory
### 1. Absolute Error (`abs`)
To know *when* to brake, the robot needs to know if it's approaching a turn. 
Our Error ranges from `-1.0` to `1.0`. We don't care if the turn is left or right; we only care about the *size* of the Error. 

Python has a built-in function called `abs()` (Absolute Value) that removes the minus sign:
* `abs(-0.8)` becomes `0.8`
* `abs(0.0)` stays `0.0`

### 2. The Adaptive Speed Formula
Instead of a fixed `base_speed`, we will calculate a `dynamic_speed` every single loop using this formula:
`dynamic_speed = max_speed - (braking_force * abs(position))`

* On a straight line (`position = 0.0`), the robot drives at the full `max_speed`.
* On a sharp turn (e.g., `position = 1.0`), the robot subtracts the full `braking_force` from its speed, safely slowing down to execute the turn!

## Assignment
Upgrade your P-Controller to the ultimate Adaptive Speed Controller!

**Requirements:**
1. **Setup:** Use your code from Mission 5.3 (without the Kick timer).
2. **New Variables:** Remove `base_speed`. Create two new variables before the loop:
   * `max_speed = 40`
   * `braking_force = 20`
3. **Adaptive Math:** Inside the loop, before calculating `P`:
   * Calculate `dynamic_speed` using the formula with `abs(position)`.
4. **The P-Controller:**
   * Calculate `P` as usual (`kp * position`).
   * Calculate `left_speed` and `right_speed` using your new `dynamic_speed` instead of a fixed base speed. Don't forget to use `int()`!
6. **Execute:** Send the speeds to the motors. Watch your robot fly down the straights, dynamically brake for the corners, and **complete one full lap!**

**The Tuning Challenge (Optional):**
Once your rover is successfully completing lap, it’s time to push the physics to the limit! Remember that the absolute maximum power the motors can accept is `100`. 

Try experimenting with extreme parameters and observe how the rover reacts:
* **The Steering Test:** Compare small changes to `kp` while keeping the starting maximum speed. Observe how smoothly the rover follows the bends.
* **The Braking Test:** Change `braking_force` in small steps and compare the speed on straights with the speed through corners.
* Keep the line-loss stop enabled during every experiment. Finish a stable lap with the supplied settings before changing the speed.
