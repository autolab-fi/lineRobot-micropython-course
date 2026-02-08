---
index: 5
module: module_1
task: python_variables_commands
previous: directional_movement
next: maneuvering
---

# Mission 2.5 Python Variables & Commands

## Objective

Learn to store data using variables, perform basic arithmetic, and use these variables to control the robot and report its status.

## Introduction

In previous missions, you typed specific numbers directly into the command like `robot.move_forward_distance(20)`. This works for simple tasks, but what if your program becomes huge and you need to change that distance in ten different places?

In this mission, we introduce **Variables**. Think of them as labeled boxes where you can store information. instead of memorizing the number "20", you label a box "distance" and put "20" inside. When you need the number, you just ask for the box.

## Theory

### 1. What is a Variable?
A variable is a name attached to a value. In Python, you create a variable by giving it a name and using the `=` sign.

```python
distance = 50
```
Now, whenever Python sees the word `distance`, it treats it as the number `50`.

### 2. Data Types
Computer programs use different types of data. Today we focus on two:

* **Integer (`int`):** Whole numbers without a decimal point. used for counting or simple steps.
    * Example: `speed = 20`
* **Float (`float`):** Floating-point numbers (decimals). Used for precise measurements.
    * Example: `precise_distance = 15.5`

### 3. Arithmetic and Parameters
You can do math with variables!
```python
x = 10
y = 5.5
result = x + y  # result is now 15.5
```

Most importantly, you can pass variables into robot functions instead of raw numbers.
```python
step = 30
robot.move_forward_distance(step)
```

### 4. The `print()` function
Robots need to talk back to us. The `print()` command writes text to the console (the output window). You can print text and variables together by separating them with commas.

```python
dist = 100
print("The robot traveled", dist, "cm")
```
*Output: The robot traveled 100 cm*

## Assignment

Let's make the robot smarter. Instead of writing numbers inside the functions, you will define them at the top of your program.

**Task Requirements:**
1. Create a variable (float) for backward movement - `20.5`.
2. Create a variable (int) for forward movement - `15`.
3. Use these variables to make the robot move **backward** and then **forward**.
4. Calculate the total distance traveled (backward + forward) and save it in a new variable.
5. Print the message: `"Total distance:", <your_variable>, "cm"`.

**Example structure:**
```python
from lineRobot import Robot
robot = Robot()

# Create variables
back_dist = 15.5
# ... create other variables ...

# Move using variables
robot.move_backward_distance(back_dist)
# ... next command ...

# Calculate and Print
total = back_dist + ...
print("Total distance:", total, "cm")
```

Good luck, programmer!

## Conclusion

Great job! You are no longer just giving orders; you are writing dynamic code. Variables are the building blocks of all complex software. In the next mission, we will use them to perform complex turns!
