---
index: 3
module: module_2
task: defining_functions
previous: differential_drive
next: for_loops
---
# Mission 2.3 Defining Functions

## Objective
Learn what a function is and how to create your own custom functions in MicroPython.

## Introduction
In programming, a **function** is a named, reusable block of code that performs a specific task. You can think of it as a recipe or a mini-program inside your main program. 

We have already used built-in functions created by other programmers, such as `print()`, `time.sleep()`, or `robot.run_motors_speed()`. But what if you need a specific maneuver that doesn't exist in the library? In this lesson, you will learn how to write your very own custom functions!

## Theory

### 1. Why Use Functions?
Imagine you need the robot to perform a special "dance" maneuver multiple times. Writing the individual motor commands, sleep times, and stop commands over and over makes your code huge and hard to read. By grouping these commands into a custom function, you can perform the whole dance later with just one short line of code.

### 2. Creating a Function (`def`)
In Python, you define a function using the `def` keyword, followed by the function's name and parentheses. 

Here is an example of a function that makes the robot move forward and then wait:

```python
from lineRobot import Robot
import time

robot = Robot()

# Defining the function
def move_forward_and_wait():
    robot.run_motors_speed(50, 50)
    time.sleep(2)
    robot.stop()
    time.sleep(1)

# Calling the function
move_forward_and_wait()
```

**Notice two important things:**
* **Indentation:** The code inside the function is indented (shifted to the right). This tells Python which commands belong inside the function.
* **Defining vs Calling:** Defining a function doesn't run it automatically. You have to **call** it by writing its name with parentheses (like `move_forward_and_wait()`) at the bottom of your script to actually execute the code!

### 3. Adding Parameters
Functions become even more powerful when you give them **parameters** (inputs). This allows the function to behave differently depending on the values you pass to it.

```python
def custom_move_forward(speed, seconds):
    robot.run_motors_speed(speed, speed)
    time.sleep(seconds)
    robot.stop()
        
# Now you can use it with any speed and time!
custom_move_forward(60, 3)  # Moves at 60% speed for 3 seconds
custom_move_forward(100, 1) # Moves at 100% speed for 1 second
```

### 4. Returning Values
Some functions perform an action (like moving), while others calculate something and **return** a result back to you using the `return` keyword.

```python
def add_numbers(num1, num2):
    result = num1 + num2
    return result

total = add_numbers(5, 10) # The variable 'total' will store the number 15
```

## Assignment
Write a program that makes the robot turn approximately **180 degrees** by creating your own custom function.

**Requirements:**
* **Do not** use built-in navigation functions (like `turn_left`, `turn_right`, or `move_forward_distance`).
* Define a custom function.
* Inside your function, use manual motor control methods (`run_motors_speed` or raw PWM) and `time.sleep()`.
* Call your function at the end of the script to execute the maneuver.


**Hint:** Because our robot uses a differential drive, it can rotate on the spot. To do this, one wheel must spin forward while the other spins backward at the same time!

## Conclusion
Congratulations! You are no longer just a driver; you are now extending the robot's core software. Custom functions are the building blocks of advanced programming. Next up, we will learn how to repeat these functions automatically!