---
index: 4
module: module_1
task: directional_movement
previous: license_to_drive
next: python_variables_&_commands
---

# Mission 1.4 Directional Movement

## Objective

Explore functions for moving the robot a specific distance.

## Introduction

In the past two lessons, we've utilized only one function from the lineRobot library. It's now time to introduce additional functions for controlling the robot: moving backward and moving forward, where the parameter is not the number of seconds but the distance.

## Theory

In the previous lesson, you gained insight into **functions** and **parameters**. You used the **move_forward_seconds(seconds)** function, with the parameter representing the duration of robot movement in seconds. However, for precise control over the robot's position on the map, we need functions that allow movement based on distance in centimeters.

**robot.move_forward_distance(dist)** - A function for moving the robot forward by the number of centimeters specified by the parameter **dist**.
**robot.move_backward_distance(dist)** - A function for moving the robot backward by the number of centimeters specified by the parameter **dist**.

Robot directions
![robot_directions](../../images/module-1/robot_directions.png)

## Assignment

Write a program for the robot to move **backward 35** centimeters and then **forward 20** centimeters. Good luck!

## Conclusion

Congratulations! You have gained knowledge about two crucial functions of the library that will prove valuable in the upcoming lessons.
