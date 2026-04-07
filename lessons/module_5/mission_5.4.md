---
index: 30
module: module_5
task: tuning_and_kick
previous: proportional_control
next: adaptive_speed
---

# Mission 5.4 Tuning & The "Software Kick"

## Objective
Understand the effects of the Proportional Coefficient (*K_p*) on system stability, tune it for optimal performance, and implement a "Software Kick" to test the controller's recovery capabilities.

![Advanced](https://img.shields.io/badge/Difficulty-Advanced-red)

## Introduction
In the last mission, you built a working Proportional Controller. But as you probably noticed, guessing the *K_p* value (like `10`) doesn't always result in a perfect ride. 

In professional robotics, writing the formula is only 10% of the work. The other 90% is **Tuning** - finding the mathematically perfect coefficient for your specific hardware. 

Furthermore, a good navigation system must be resilient. What happens if the rover hits a lunar rock or slips on loose dust? Today, we will tune our *K_p* and inject a fake "physical shock" into the system to see if the rover can survive it!

## Theory

### 1. The Tuning Balance (Understeer vs. Oversteer)
When tuning *K_p*, you are looking for the perfect balance between two extremes:
* **Too Low (Understeering):** The robot's reactions are too weak. It drives very smoothly on straight lines, but when it reaches a sharp turn, it doesn't steer hard enough and drives off the track.
* **Too High (Oversteering):** The robot's reactions are too aggressive. It aggressively overcorrects every tiny error, resulting in a violent wobble (oscillation). If *K_p* is way too high, it might shake itself completely off the line!

### 2. The "Software Kick"
To truly test if your *K_p* is tuned perfectly, the robot must be able to recover from a sudden physical disturbance. 

Since we cannot physically kick the rover in the simulation, we will program a **Software Kick**. Using the `time.time()` stopwatch logic you learned in Module 4, we will force the robot to violently twist to the side for a split second every 5 seconds. 

If your *K_p* is tuned well, the P-Controller will instantly recognize the massive Error and snap the robot back onto the line. If it's tuned poorly, the kick will permanently derail the rover!

## Assignment
Your task is to integrate a 5-second interval timer into your P-Controller. When the timer triggers, apply a sharp motor movement, then let the P-Controller recover.

**Requirements:**
1. **Setup:** Use your P-Controller code from Mission 5.3.
2. **The Timer Setup:** Before the `while True:` loop, create a variable `last_kick_time = time.time()` to start your stopwatch.
3. **The Kick Logic:** Inside your loop, before calculating the Proportional Math, calculate the `elapsed_time`.
   * Use an `if` statement to check if the elapsed time is greater than `5` seconds.
   * If true: Print `"KICK!"`, force the motors to twist sharply (e.g., `robot.run_motors_speed(40, -40)`), pause for `0.15` seconds to let the physical twist happen, and finally **reset** your `last_kick_time` to the current time!
4. **The P-Controller:** If it's not time to kick (`else:`), perform your standard Proportional math and steer the rover.
5. **The Tuning Challenge:** Run the code. Observe how the rover handles the kicks. Adjust your `kp` variable up or down until the rover drives smoothly AND successfully recovers from every kick!

## Conclusion
Incredible engineering! You have successfully stress-tested an autonomous control system. 

By observing the recovery after the Software Kick, you saw firsthand how mathematical formulas translate into physical resilience. You now know how to diagnose understeering and oversteering, and how to find the optimal *K_p*.

Your rover is now incredibly stable. In our final mission of this module, we will make it *fast* by introducing Adaptive Speed!
