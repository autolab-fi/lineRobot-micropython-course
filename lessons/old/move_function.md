# Lesson 9: Movement Function

## Lesson Objective

Learn how to write your own functions.

## Introduction

In this lesson, you will learn how to write your own functions in MicroPython.

## Theory

In Lesson 2, "License to Drive," you were introduced to the concept of functions. Now, you can write your own functions to make your code more compact, readable, and easier to maintain.

### Types of Functions

Functions can return values, such as numbers, characters, strings, etc. To specify the type of data a function returns, you need to indicate the function's type. Let's explore functions that return values and those that do not.

### Functions Returning Values

Example of a function that returns a value in MicroPython:

```python
def sum(num1, num2):
    result = num1 + num2  # calculated sum of the parameters
    return result  # return value of the variable result
```

The **sum(a, b)** function in the example takes numbers **num1** and **num2** as parameters and returns their sum.

Example of using the function:

```python
a = 5
b = 10
c = sum(a, b)  # value of the variable c is 15
```

In this code, variables **a** and **b** are initialized, their sum is calculated, and the result is stored in variable **c**.

Functions that return values must have a **return** statement, which ends the function's execution and returns the specified value.
Examples:

```python
...
return 0
```

This function returns 0.

```python
...
return 'L'
```

This function returns a **str** data type, specifically the character **'L'**.

### Functions Not Returning Values

In the previous section, you learned about functions that return values. However, there are also functions that do not return anything. In MicroPython, such functions simply do not use a return statement or return `None`.

Example:

```python
from lineRobot import Robot
import time

robot = Robot()

def move_robot_forward_backward(seconds_move, seconds_pause):
    robot.move_forward_seconds(seconds_move)
    time.sleep(seconds_pause)
    robot.move_backward_seconds(seconds_move)
```

The **move_robot_forward_backward** function takes the parameter **seconds_move**, which tells the robot how long to move forward and backward, and the parameter **seconds_pause**, which specifies the pause before the robot moves backward.

How to use this function:

```python
move_robot_forward_backward(3, 1)
```

In this code, we called the function **move_robot_forward_backward**, so the robot will move forward for 3 seconds, then stop, and move backward for 3 seconds.

Remember: You should write **move_robot_forward_backward(3, 1)** instead of ~~robot.move_robot_forward_backward(3, 1)~~.

## Assignment

Write a program that makes the robot turn approximately 180 degrees.

You can use the function **run_motors_speed** to set the speed of the left and right motors, and **stop** to stop the motors. The functions **move_forward_distance**, **move_backward_distance**, **turn_left**, **turn_right**, **move_forward_seconds**, and **move_backward_seconds** will not work for this task.

### Hint

We recommend writing your own movement function. You can design it to accept several parameters, such as separate speeds for the motors and time, or just the execution time with fixed speeds.

## Conclusion

Congratulations! In this lesson, you learned how to write your own function, allowing you to organize your code more efficiently.
