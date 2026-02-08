---
index: 6
module: module_1
task: maneuvering
previous: python_variables_&_commands
next: sequential_navigation
---

# Mission 2.6 Maneuvering

## Objective

Master the robot's steering system by learning standard 90-degree turns and precision turning with specific angles.

## Introduction

In the previous missions, you learned to move forward and backward and how to store data in variables. But a robot that can only move in a straight line is not sufficient for free movement across the field.

In this mission, you will learn how to orient the robot in space. We will cover basic turns (for navigating grids) and precision turns (for complex paths).

## Theory

Below, the image represents the possible directions of the robot's movement.

![robot_directions](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_1/directions.png?raw=true)

### 1. Standard Turns (90 Degrees)
For simple navigation, like a maze or a city grid, we usually turn exactly 90 degrees.
* **`robot.turn_right()`** — Turns the robot 90 degrees to the right.
* **`robot.turn_left()`** — Turns the robot 90 degrees to the left.

As you can see, the turning functions don't require any parameters. It's sufficient to call them, and the robot will turn in place in the desired direction.

### 2. Precision Turns (Specific Angles)
Real-world paths are rarely perfect squares. Sometimes you need to turn just a little bit, or make a U-turn.
To do this, you can pass a **parameter** (an integer or float) to the turn functions.

* **`robot.turn_right_angle(degrees)`** — Turns right by the specified angle.
* **`robot.turn_left_angle(degrees)`** — Turns left by the specified angle.

### 3. Using Variables for Turns
Remember the variables from the last mission? You can use them here too! This makes your code readable and easy to change.

```python
turn_angle = 45
robot.turn_left_angle(turn_angle)
```

## Assignment

It's time to test the steering mechanism. You need to perform a sequence of maneuvers using both standard commands and variables.
Write code for the robot to **turn right, then turn left, and finally turn left again for 145 degree**.

## Conclusion

Congratulations! Now you can move the robot in any directions! This skill will prove very useful for you in the next lesson.
