---
index: 27
module: module_5
task: concept_of_error
previous: data_logging
next: failsafe_protocols
---

# Mission 5.1 The Concept of Error

## Objective
Understand the limitations of a Relay (Bang-Bang) controller and introduce the concept of "Error" as a continuous gradient using the advanced `track_line()` function.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
Welcome to Module 5, Recruit!
In Module 3, you built your first autonomous line follower. It successfully navigated the track, but the ride wasn't exactly smooth. The rover wobbled back and forth aggressively. That algorithm is known as a **Relay Controller** (or "Bang-Bang").

Why did it wobble? Because its "brain" only knew three rigid states: "Line is Left," "Line is Right," or "Line is Center." If the line drifted 1 centimeter to the left, the robot steered hard left. If the line drifted 5 centimeters to the left, the robot... steered exactly the same hard left.

To achieve a smooth, professional ride, the rover needs to know not just *where* the line is, but *how far* it has drifted. Today, we introduce the foundational concept of precision robotics: **The Error**.

## Theory

### 1. What is "Error"?
In control theory, **Error** is the mathematical difference between where you *want* to be (the Target) and where you *actually* are (the Current State).
For our lunar rover, the Target is to keep the tracking line perfectly centered under the sensor array. The Error is the physical distance the line has drifted to either side.

### 2. The `track_line()` Function
Calculating the exact center of a line using 8 separate sensors requires complex math (like calculating a weighted average). Fortunately, the Octoliner library has a built-in method that performs this calculation for us instantly!

Instead of reading an array of 8 raw numbers and using `elif` statements, we can use the `track_line()` function:

```python
position = octoliner.track_line()
```

This function returns a single decimal number (`float`) representing the exact position of the line:
* **`-1.0`**: The line is far to the **left** (under sensor 0).
* **`0.0`**: The line is perfectly in the **center**.
* **`1.0`**: The line is far to the **right** (under sensor 7).

This continuous gradient—smoothly transitioning from `-1.0` to `1.0`- is exactly what we need. This value is our **Error**!

## Assignment
Mission Control requires a structural scan of a basaltic fracture (the black line). To prevent the rover from twisting off the track during the scan, the engineering team has provided a skeleton for a `diagnostic_sweep(speed_left, speed_right)` function. 

You must complete the core logic of this function and then execute the mission sequence.

**Requirements:**
1. **Setup:** Initialize your `Robot`, the I2C bus, and the `Octoliner` (don't forget to set the sensitivity).
2. **Complete the Function:** Inside the `diagnostic_sweep` `for` loop, replace the `# TODO` comments with actual code:
   * Read the line position using `octoliner.track_line()` and save it to a variable.
   * Print the result using a string format (e.g., `"Error: -0.45"`).
3. **The Mission Sequence:** Below the function, program the following path:
   * Call `diagnostic_sweep()` to swing **Left** (Left motor: `-15`, Right motor: `15`).
   * Drive the rover straight forward by **30 cm**.
   * Call `diagnostic_sweep()` to swing **Right**.

Watch the live video feed as the robot rotates over the line and observe the terminal. You should see the printed numbers transition smoothly from `-1.0` (or close to it) to `1.0`.

## Conclusion
Excellent! You have successfully observed the continuous gradient of the line's position. 

The robot now sees the world not just in rigid black and white ("Yes/No"), but in highly precise shades of grey ("How much?"). This smooth Error value is the absolute foundation of advanced robotics.