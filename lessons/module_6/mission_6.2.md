---
index: 33
module: module_6
task: hardware_safety_net
previous: art_of_debugging
next: code_clinic
---

# Mission 6.2 The Hardware Safety Net

## Objective
Learn how to protect your robot from unexpected hardware glitches and crashes using the `try-except` block.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
In the previous mission, you fixed logic bugs in your code. But what happens when your code is perfect, but the physical world fails?

Imagine your rover is driving through a dark lunar crater. A shadow falls over the color sensor, and for a split second, it reads absolute darkness: `R: 0, G: 0, B: 0`. In Module 4, you wrote a color normalization function that calculates `total = r + g + b` and then divides by the total (`r / total`).

If the total is `0`, Python will attempt to divide by zero. This triggers a `ZeroDivisionError`, immediately crashing the entire program and leaving the rover permanently stranded. We cannot allow a one-second sensor glitch to end a billion-dollar mission. Today, we build a safety net.

## Theory

### Graceful Degradation (The `try-except` block)
In software engineering, we use a concept called **Exception Handling**. Instead of letting Python crash when an error occurs, we can "catch" the error and tell the robot what to do instead.

We do this using a `try-except` block:
1. **`try:`** Python will *attempt* to execute the dangerous code inside this block.
2. **`except:`** If a specific error happens, Python will instantly jump to this block instead of crashing.

```python
r = 0
total = 0

try:
    # Python tries to do this math...
    ratio = r / total 
    
except ZeroDivisionError:
    # If a ZeroDivisionError happens, it jumps here and survives!
    print("WARNING: Math failed, but I am still alive!")
    ratio = 0.0 # Assign a safe default value
```

## Assignment
In this mission, we are performing a **Stress Test**. Since our lunar facility does not have naturally occurring pitch-black craters, Mission Control is **simulating** a sensor blackout by injecting raw data directly into your code. 

The rover will rotate, but instead of reading live data, it will process a pre-defined list of coordinates (`scans`) that includes several "Shadow Zones" (zeros). 

Currently, the program crashes as soon as it encounters the first injected zero due to a `ZeroDivisionError`. You must implement a safety net to ensure the diagnostic completes.

**Requirements:**
1. Locate the division calculations inside the `detect_color_name` function.
2. Wrap the math logic inside a `try:` block.
3. Add an `except ZeroDivisionError:` block to catch the crash.
4. Inside the `except` block:
   - Print a warning: `"CRITICAL: Sensor Blind!"`.
   - `return "Unknown"` as a safe default value.
5. Run the code. The robot must successfully cycle through all **10 injected data points** during its rotation without crashing.

## Conclusion
Incredible work! You have successfully implemented **Graceful Degradation**. 

By using "Data Injection" to simulate a failure, you proved that your code can handle the worst-case scenario. The math broke, but the rover stayed "alive". This resilience is what separates simple toys from professional, space-grade autonomous systems.