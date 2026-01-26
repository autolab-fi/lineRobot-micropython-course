---
index: 3
module: module_1
task: license_to_drive
previous: test_drive
next: directional_movement
---

# Mission 1.3. License to drive

## Objective

Understand the structure of a Python robotics program and write your own code to control the robot.

## Introduction

In this lesson, we are granting you the driver's license. Today, you will be writing the program on your own without the instructor's help. However, first, let's cover some important programming concepts that will help you control the robot effectively.

## Theory

To write a complete program, we need a specific "recipe" with three ingredients. We already know one (Creation), now let's learn the others: **Import** and **Command**.

### 1. Import (Getting the tools)
Before we can build anything, we need tools. In Python, code is organized into **libraries**.
The line:
```python
from lineRobot import Robot
```
tells Python to open the `lineRobot` library and take out the `Robot` tool. Without this, the computer won't know what a "Robot" is.

### 2. Command (Action and Parameter)
Once we have our robot object, we can give it orders using **functions**. A function is a specific instruction.
```python
robot.move_forward_seconds(3)
```
Notice the structure:
* **`robot.`**: We specify *who* performs the action.
* **`move_forward_seconds`**: The command (Function).
* **`(3)`**: The **Parameter**.

**Parameters** are the specific details of the command. In this case, `3` tells the function *how long* to move. 

## Assignment

It is time to drive on your own!
Write a program for the robot to make it drive straight for 5 seconds. You can refer back to the previous lesson to recall how to set the robot in motion. Good luck!

## Conclusion

Congratulations! You have successfully analyzed the anatomy of a robotics program. You now understand how to import tools, create a robot object, and use parameters to control its behavior. Keep your license safe; you'll need it for the complex maneuvers ahead!