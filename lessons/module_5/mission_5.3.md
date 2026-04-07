---
index: 29
module: module_5
task: proportional_control
previous: upgraded_relay_controller
next: tuning_and_kick
---

# Mission 5.3 Proportional Control Logic

## Objective
Understand the mathematical concept of Proportional Control and write a P-controller algorithm to smoothly steer the rover based on the continuous Error gradient.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
Your Upgraded Relay Controller in the last mission was smart, but it still wobbled. Why? 
Because it still turned at a *fixed* speed, regardless of the situation. Whether the rover drifted 2 millimeters or 5 centimeters off the line, it applied the exact same turning force. 

Imagine driving a car on a highway. If you drift slightly from the center of your lane, you don't instantly yank the steering wheel all the way to the side! You make a *small* correction. If you drift significantly, you make a *larger* correction.

This natural driving logic is called a **Proportional Controller (P-Controller)**. The steering correction is directly proportional to the size of the error. Now we will teach rover to drive like a professional.

## Theory

### 1. The Amplification Problem
Our `track_line()` function gives us an Error value from `-1.0` to `1.0`. 
If the rover's base speed is `25`, and the Error is `0.5`, what happens if we just add the Error to the speed? The new speed becomes `25.5`. That tiny difference will not turn the robot at all!

To turn this small decimal Error into a strong motor command, we must amplify it by multiplying it by a constant number. In control theory, this amplifier is called the **Proportional Coefficient**, or *K_p*.

### 2. The Math of Steering
The formula for a Proportional Controller is beautiful in its simplicity. 

First, we calculate the required steering power *P* using our coefficient *K_p$*: **P = K_p * Error**

Next, we apply this steering power to the wheels. To turn smoothly, we *add P* to the left motor and *subtract P* from the right motor.
* **`left_speed = base_speed + P`**
* **`right_speed = base_speed - P`**

**Let's test the math:** Imagine the line drifts to the right (Error = `0.5`). Let's say our *K_p* is `30`, and `base_speed` is `25`.
1. Calculate Power: P = 30 * 0.5 = 15
2. Left Motor: 25 + 15 = 40
3. Right Motor: 25 - 15 = 10

Because the left wheel is now spinning at `40` and the right wheel at `10`, the rover smoothly arcs to the right, perfectly bringing the line back to the center! If the Error was smaller (e.g., `0.1`), the speed difference would be much smaller, resulting in a gentle, almost invisible correction.

## Assignment
Write a Proportional Control loop to navigate the track. You will replace your bulky `if/elif/else` steering blocks with just three elegant lines of mathematical code.

**Requirements:**
1. **Setup:** Initialize your hardware, including auto-calibration and the `math` library.
2. **Control Variables:** Before the loop, create two variables:
   * `base_speed = 30`
   * `kp = 10` (This is our starting guess for the Proportional Coefficient).
3. **The Loop:** Inside your `while True:` loop:
   * Read the `position` from the sensor.
   * Include the `NaN` Failsafe from the previous mission to protect the software.
   * If the data is valid (`else:`), perform the P-Controller math:
     * Calculate `P` by multiplying `kp` and `position`.
     * Calculate `left_speed` and `right_speed`. *(Note: Wrap your final math in `int()` like this: `int(base_speed + P)` to ensure the motor function receives whole numbers).*
     * Send the speeds to the motors using `run_motors_speed()`.
   * Keep the `time.sleep(0.05)` delay.

Execute the code! Watch closely. The rover should navigate the track much smoother than before, automatically adjusting its turn sharpness.

## Conclusion
Brilliant! You have successfully implemented a Proportional Controller. 

Look at your code: you replaced complicated logical conditions with pure, elegant mathematics. The rover now makes hundreds of tiny, calculated adjustments per second.

However, you might notice it still isn't *perfect*. Maybe it turns a little too sluggishly, or maybe it shakes a bit on the straightaways. In the next mission, we will learn how engineers **"Tune"** the *K_p* value to achieve flawless movement!

> **Important:** Save your standard P-Controller math. You will need to copy and paste this into your next mission.