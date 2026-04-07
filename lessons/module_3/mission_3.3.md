---
index: 16
module: module_3
task: processing_sensor_data
previous: conditional_logic
next: reading_multiple_sensors
---

# Mission 3.3 Processing Sensor Data

## Objective
Learn how to use comparison operators, understand Boolean values (`True`/`False`), and encapsulate threshold logic inside a custom Python function.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
In the last mission, you hardcoded a specific number directly into your `if` statement to stop the robot. But what if the lighting conditions in the testing facility change? You would have to hunt through hundreds of lines of code to change that number everywhere! 

Furthermore, the robot's main navigation computer doesn't care if the sensor reads `245` or `12`. It only needs a simple answer: *"Is there a line here? Yes or No?"* Today, we will introduce Booleans and Comparison Operators to give our rover clear, binary answers.

## Theory

### 1. Variables as Thresholds
A **threshold** is a specific numerical value that acts as a dividing line between two states (e.g., "White Floor" vs. "Black Line"). By storing this value in a variable at the very top of your program, you make your code easily adjustable.

```python
# If the lighting changes, you only change this ONE line at the top!
THRESHOLD = 200
```

### 2. Comparison Operators
To make decisions, Python needs to compare values. We do this using mathematical comparison operators:
* `>` : Greater than
* `<` : Less than
* `>=` : Greater than or equal to
* `<=` : Less than or equal to
* `==` : Equal to. **(Important: Notice the double equals! A single `=` assigns a value to a variable, while `==` compares two values to see if they are the same).**

### 3. Binary Decisions (Booleans)
When Python compares two numbers (e.g., `50 < 100`), the result is always a special data type called a **Boolean**. A Boolean can only have one of two values: `True` (Yes) or `False` (No). *Note: In Python, these must always start with a capital letter!*

### 4. Encapsulating Logic
We can build a custom function that reads a value, uses a comparison operator, and **returns** a Boolean. This separates the sensing from the acting. 

Here is an example of how this logic works for a collision system (do not copy this for your line sensor, this is just an example!):

```python
DANGER_DISTANCE = 10

def is_too_close(current_distance):
    if current_distance < DANGER_DISTANCE:
        return True   # Yes, it is too close!
    else:
        return False  # No, we are safe.
```
Now, whenever you need to know if the robot is about to crash, you simply call result = is_too_close(8)!

## Assignment
Your rover must perform an active scan of the lunar surface. Write a program that defines a scanning function, moves the rover forward in small steps, and prints an alert when it detects geological layers using the central sensors.

**Requirements:**
1. **The Function Definition:** Create a custom function named `detect_line` that accepts two parameters: `(distance, threshold)`. 
3. **The Scanning Loop:** Inside the function, create a `for` loop that repeats 15 times. In each iteration:
    * Move the robot forward by the `distance` parameter.
    * Read the values of **Sensor 3** and **Sensor 4**.
    * Use an `if` statement to check if Sensor 3 is greater than the `threshold`. If true, print: `"Sensor 3 : [value] Found geological layers!"`.
    * Do the same `if` check for Sensor 4.
    * Add a small delay at the end of the loop iteration.
4. **Execution:** At the bottom of your script, call your `detect_line()` function, passing in your `distance` and `threshold` variables.

## Conclusion
Excellent engineering! You have successfully built an active scanning algorithm. By combining movement commands, sensor readings, and comparison operators inside a single function, your rover can now map out specific features on the ground autonomously.

In the next mission, we will expand our logic to read the outer sensors, giving the rover full spatial awareness so it can follow a continuous path!
