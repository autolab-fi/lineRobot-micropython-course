---
index: 15
module: module_3
task: conditional_logic
previous: intro_to_octoliner
next: processing_sensor_data
---

# Mission 3.2 Conditional Logic & Reactive Behavior

## Objective
Learn how to use conditional statements (`if/else`) and the `break` command to create reactive behavior, allowing the rover to stop autonomously when a line is detected.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
In the previous mission, you successfully streamed data from the rover's optical sensor. However, the rover merely printed the numbers; it didn't *understand* them. 

Real autonomy requires the robot to change its plans on the fly based on what it sees. Today, we are giving the rover a "brain" by introducing conditional logic, enabling it to react to its environment in real-time.

## Theory

### 1. Conditional Statements
Conditional logic allows the robot to choose between different actions based on a specific rule. 

![Conditional_logic](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-3/conditional-logic.png?raw=true)

In Python, we use the `if` statement to check a condition. If the condition is `True`, the indented code underneath it will execute. We can also add an `else` statement as a fallback action if the condition is `False`.

```python
# Assuming we have already read the sensor value
if sensor_value > 200:
    print("Black line detected!")
else:
    print("Floor is clear.")
```

### 2. The `break` Operator
When you use a `while True:` loop, it runs forever. But what if the robot finds what it's looking for and needs to stop? 

The `break` command immediately destroys the loop it is inside and forces the program to move to the next section of the code. This is the ultimate "emergency stop" for repetitive tasks.

```python
while True:
    # ... doing some continuous task ...
    if condition_met:
        break # Exits the loop immediately!

print("Task finished.")
```

## Assignment
Write a reactive program where the robot drives forward, searches for a dark line using a central sensor, and stops the motors the exact moment it finds one.

**Requirements:**
1. Import the necessary libraries. 
2. Initialize your `Robot` object and the `Octoliner` sensor (remember to set the I2C pins `scl=machine.Pin(22), sda=machine.Pin(21)`).
3. Set the rover in motion forward at a low speed (e.g., 30%). *Hint: Moving too fast will cause the rover to skip over the line before the sensor can react!*
4. Create a continuous monitoring cycle (`while True:` loop) that constantly reads the value of **Sensor 3** and print values. Add a small delay inside the loop to prevent processor overload.
5. Implement conditional logic (`if` statement) inside your loop:
    * The exact moment the sensor's value indicating the black line (e.g. > 200 - we'll discuss it later), your program must cut power to the motors.
    * Immediately after stopping the motors, execute a `break` command to completely exit the monitoring loop.
6. Print a success message (e.g., `"Target found. Rover stopped."`) to the terminal once the loop has been broken.

## Conclusion
Brilliant! Your rover is now truly reactive. It can independently decide when to terminate a movement task based on its physical environment, rather than blindly following a timer. 

However, writing this entire `while/if/break` logic block every single time we want to check for a line will make our code very messy as missions get more complex. In the next mission, we will learn how to wrap this threshold logic into clean, reusable functions!
