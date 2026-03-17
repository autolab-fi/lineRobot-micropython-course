---
index: 24
module: module_4
task: color_classification
previous: color_sensor_basics
next: multiple_sensors
---

# Mission 4.4 Color Classification

## Objective
Learn how to process raw sensor data, understand color normalization, and write a custom Python function to classify RGB values into human-readable colors.

## Introduction
In the previous mission, your rover successfully scanned the terrain and printed raw RGB (Red, Green, Blue) values. However, raw numbers are hard for humans to read, and even harder for a robot to use for making decisions. 

If we want the rover to say "I found Green!" instead of "R:165 G:174 B:142", we need to teach its brain how to interpret those numbers. 

## Theory

### 1. The Illumination Problem
You might think we can just say: `if r > 150: print("Red")`. But there is a huge problem: **lighting changes**. 
If the rover drives into a shadow, the raw values for *all* colors will drop. The sensor might read `R:80 G:20 B:20`. The red value is low (80), but the object is still clearly red! 

To fix this, we don't look at the raw numbers. We look at the **proportions** (ratios).

### 2. Normalizing Data
To find the true color, we calculate what percentage of the total light belongs to each color. This is called **data normalization**.
1. First, we find the total amount of light: `total = r + g + b`
2. Then, we divide each color by the total: `r_ratio = r / total`

If `r_ratio` is `0.5`, it means 50% of all the light reflecting off the ground is red. This proportion stays the same whether the rover is in bright sunlight or deep shadow!

### 3. Creating a Custom Function
We will package this math into a custom **function**. A function is a reusable block of code that takes inputs, processes them, and `returns` an output.

```python
def detect_color_name(r, g, b):
    # Math goes here
    return "Red" # The output
```
## Assignment
Your task is to upgrade your Linear Scanner from the previous mission. You will create a custom Python function that uses math to convert raw RGB data into a specific color name ("Red", "Green", or "Floor"), and then apply it to your scanning loop.

**⚠️ WARNING: The Illumination Trap!** The grey lunar floor under the lab lights might reflect more red light than you expect (sometimes over 40% of the total light). 
* Do not just guess the numbers! 
* Look at the raw data logs from your Mission 4.3 scan and use a calculator to find the exact `r_ratio` of the floor versus the Red zone. 
* Set your `if r_ratio > ___` threshold high enough to ignore the floor (e.g., `> 0.5`), but low enough to detect the real Red zone.

**Requirements:**
1. Set up the hardware: Initialize the `Robot` and the `tcs3472` color sensor on the I2C bus.
2. Complete the `detect_color_name(r, g, b)` function:
    * Math: Calculate the `total` light, and then divide each color by the total to find `r_ratio`, `g_ratio`, and `b_ratio`.
    * Logic: Fill in the `if/elif` statements. *Hint: A good starting point for a dominant color is `0.3` (30%). For example, if it's red, `r_ratio` should be `> 0.3`.
3. Build the Smart Scanner: Add your previous scanning loop from Mission 4.3 below the function.
4. Call the function: Inside the loop, after reading the `r, g, b` values, pass them into your new function: `color_name = detect_color_name(r, g, b)`.
5. Print: Output the final color name and the raw values using an f-string: `Scan: {color_name} (Raw: R:{r} G:{g} B:{b})`.

## Conclusion
Congratulations! You have successfully built a color classification algorithm. Your rover can now adapt to the lighting conditions and accurately identify the "Red" and "Green" zones while ignoring the background noise of the lunar floor.

> **Important:** Save your completed `detect_color_name(r, g, b)` function. You will need to copy and paste this exact function into your next mission, where we will combine the color scanner with the line-tracking algorithm!