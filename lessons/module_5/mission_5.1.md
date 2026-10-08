---
index: 27
module: module_5
task: concept_of_error
previous: color_classification
next: upgraded_relay_controller
---

# Mission 5.1 The Concept of Error

Starting settings for this exercise: `sensitivity = 245`.
Sensitivity is the Octoliner setup value (0–255); the detection threshold is a separate value applied to analog readings. Check the readings if lighting or sensor position changes.

## Objective
Understand the limitations of a Relay (Bang-Bang) controller and introduce the concept of "Error" as a signed position estimate using the advanced `track_line()` function.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
Welcome to Module 5, Recruit!
In Module 3, you built your first autonomous line follower. It successfully navigated the track, but the ride wasn't exactly smooth. The rover wobbled back and forth aggressively. That algorithm is known as a **Relay Controller** (or "Bang-Bang").

Why did it wobble? Because its "brain" only knew three rigid states: "Line is Left," "Line is Right," or "Line is Center." If the line drifted 1 centimeter to the left, the robot steered hard left. If the line drifted 5 centimeters to the left, the robot... steered exactly the same hard left.

To achieve a smooth, professional ride, the rover needs to know not just *where* the line is, but *how far* it has drifted. Today, we introduce the foundational concept of precision robotics: **The Error**.

## Theory

### 1. What is "Error"?
In control theory, **Error** is the mathematical difference between where you *want* to be (the Target) and where you *actually* are (the Current State).
For our research rover, the Target is to keep the tracking line perfectly centered under the sensor array. Here, the error is a normalized line-position reading, not a distance in centimetres.

### 2. The `track_line()` Function
The Octoliner library converts the pattern across its eight sensors into a signed line-position estimate. You can read this estimate with a built-in method.

Instead of reading an array of 8 raw numbers and using `elif` statements, we can use the `track_line()` function:

```python
position = octoliner.track_line()
```

This function returns a single decimal number (`float`) representing the estimated position of the line:
* **`-1.0`**: The line is far to the **left** (under sensor 7).
* **`0.0`**: The line is perfectly in the **center**.
* **`1.0`**: The line is far to the **right** (under sensor 0).

This value is our **Error**. In this library it changes in steps, such as `0`, `0.25` and `0.5`, rather than continuously. If a sensor pattern is not recognized, `track_line()` keeps the previous valid value. A repeated value alone does not prove that the line is still visible; the next mission adds a check of the raw sensor readings.

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

Watch the live video feed as the robot rotates over the line and observe the terminal. Observe how the sign and magnitude change as the sensor crosses the line. Values may repeat or change in steps; a short sweep does not have to cover the full range from `-1.0` to `1.0`.

## Conclusion
Excellent! You have successfully observed a numerical estimate of the line's position.

The robot now sees the world not just in rigid black and white ("Yes/No"), but in a signed estimate ("Which side, and how far across the sensor array?"). This signed Error value is the foundation for the feedback controllers in the next missions.
