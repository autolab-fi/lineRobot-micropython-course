---
index: 26
module: module_4
task: data_logging
previous: multiple_sensors
next: concept_of_error
---

# Mission 4.6 Post-Mission Report

## Objective
Transform the rover into a silent data-collection probe. It must drive autonomously for 30 seconds, memorize all color anomalies in its RAM, and print a formatted summary report when the mission ends.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
In Mission 4.5, your rover reacted to anomalies in real-time. But deep space probes operate differently: they collect data silently to save power, store it in their memory, and transmit a giant data log back to Earth only when the scanning run is complete. 

Now, you will remove the LED reactions and upgrade your rover's "brain" using a Python **List** and a **Timer**.

## Theory

### 1. Logging Data to a List
A list `[]` is perfect for storing a history of events. Every time we find a new anomaly, we use the `.append()` command. 

This command takes new data and always adds it to the **end** of the list. This is extremely useful for data logging because it automatically keeps our records in chronological order (from the first anomaly found, to the last).

```python
# EXAMPLE: Logging engine data
engine_log = [] 

while True:
    # ... inside the loop ...
    if engine_is_hot:
        # Save the time, temperature, and speed together as one item!
        engine_log.append([time, temp, speed])
```

### 2. Time-Limited Missions (The Timer Pattern)
In Mission 4.2, you used `time.time()` as a stopwatch to measure how long a movement took. Today, we will use that same tool to actively control our rover's "brain"! 

By constantly checking the stopwatch *inside* the `while True` loop, we can make the robot automatically `break` the loop and stop scanning after a specific duration.

Here is an example of using the stopwatch to create a 5-second action timer:

```python
import time

# EXAMPLE: 5-second action timer
drive_time = 5 
start_time = time.time() # Start the stopwatch

while True:
    # Constantly check how much time has passed
    elapsed_time = time.time() - start_time 
    
    if elapsed_time > drive_time:
        print("Time is up!")
        break # Exit the loop!
```

## Assignment
Upgrade your code from Mission 4.5. Remove the "show-off" features (LEDs and stopping on Blue) and replace them with a robust, time-based data-logging system. 

Your rover must drive autonomously for exactly **30 seconds**, memorize all color anomalies in its RAM, and print a formatted summary report when the time is up.

**Requirements:**
1. Setup Memory: Create an empty list.
2. Setup Timer: Create a variable `mission_duration` set to 30, and record the `start_time`.
3. Time Check: Inside the `while True` loop, calculate `elapsed_time`. If it exceeds `mission_duration`, stop the robot and `break` the loop.
4. Silent Logging: If the color changes and is not "Floor", `.append()` the color data `[current_color, r, g, b]` to your list.
5. Print the Report: At the very bottom of your code (completely outside the loop), write a `for` loop to go through your `anomaly_log` and print a professional mission report!

## Conclusion
Incredible work! You have successfully transformed your rover from a simple line-following machine into a fully autonomous scientific probe. 

Think about what you just achieved: your robot can now drive independently, track its own mission time, filter out "noise" (like the lunar floor), memorize valuable data using Python lists, and transmit a formatted professional report. This is exactly how real space agencies gather data from other planets!

Take a moment to celebrate this massive milestone. Next stop: Module 5, where we will learn about Proportional Mathematics (P-Controllers).