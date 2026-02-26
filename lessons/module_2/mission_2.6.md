---
index: 6
module: module_2
task: while_loops
previous: encoder_theory
next:
---

# Mission 2.6 While Loops

## Objective
Understand the fundamental logic of **While Loops** compared to For Loops, and use active sensor monitoring to stop a robot with precision.

## Introduction
Imagine walking towards a wall with your eyes closed. You decide to take exactly 10 steps.
* If your steps are too long, you hit the wall.
* If your steps are too short, you don't reach it.

This is how `for` loops work — they are "blind."

To stop exactly at the wall, you need to keep your eyes open and say: *"I will keep walking **while** the distance is greater than 0."*
In this mission, you will program this "Active Vision" logic.

## Theory

### 1. The Logic: Blind vs. Active
In programming, choosing the right loop changes how the robot thinks.

* **The `for` Loop (The Counter):** Used when you know the *number of repetitions* in advance.
    * *Logic:* "Repeat 5 times."
    * *Risk:* The robot doesn't know if the world changed during those 5 times.
* **The `while` Loop (The Observer):** Used when you want to repeat an action **until a condition changes**.
    * *Scenario:* A robot approaching an obstacle.
    * *Logic:* We don't know if the obstacle is 1 meter or 5 meters away. We only know we must stop *before* hitting it.
    * *Code:* "Keep moving **while** `distance_to_wall > 10`."

![for_vs_while](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-2/for_vs_while.jpeg?raw=true)


### 2. The Cycle of Monitoring
A `while` loop checks the condition before every single step.
1.  **Check:** Is the distance still safe? (`distance > 10`)
2.  **Act:** If `True`, keep the motors running.
3.  **Repeat:** Go back to step 1.

If the condition becomes `False` (distance less then 10 cm), the loop breaks immediately, and the code moves to the next commands.

## Assignment: Don't Hit the Wall
**The Scenario:** You are in a testing tunnel. There is a wall exactly **20.5 cm** away.
Your navigation computer is damaged, so you cannot use high-level functions like `move_forward()` (they reset encoders). You must fly "manual" using raw motor commands

**Your Task:** Drive **20 cm** and stop. If you overshoot by just 0.5 cm, you hit the wall.


**Requirements:**
1.  **Math:** Calculate the `target` degrees for **20 cm** ($D = 3.5$ cm) and reset the encoders.
2.  **Manual Start:** Turn on both motors at **Low Speed (around 150)**.
    * *Why Low Speed?* With high speed we cannot check the data asap, so robot will hit the wall.
3.  **The Loop:** Create a `while` loop that runs as long as some condition, that you need for the task (in this task you need to check only one encoder for simplification).
    * Inside the loop, **print** the encoder value to monitor progress.
    * **Crucial:** Add `time.sleep(0.02)` inside the loop. This small delay prevents the processor from "choking" on data and keeps the readings stable.
4.  **Manual Stop:** Immediately after the loop, turn off the motors using `stop_motor_left()` and `stop_motor_right()`.

## Conclusion

Mission Accomplished! You have successfully programmed an active control loop.

You learned that while loops allow the robot to react to the physical world, rather than just blindly following a timer. This "Sense -> Check -> Act" cycle is the foundation of all autonomous robotics.