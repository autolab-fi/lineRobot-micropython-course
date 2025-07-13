---
index: 3
module: module_1
task: short_distance_race
previous: license_to_drive
next: maneuvering
---

# Lesson 3. Short distance race

## Objective

Explore functions for moving the robot a specific distance.

## Introduction

In the past two lessons, we've utilized only one function from the lineRobot library. It's now time to introduce additional functions for controlling the robot: moving backward and moving forward, where the parameter is not the number of seconds but the distance.

## Theory

In the previous lesson, you gained insight into **functions** and **parameters**. You used the **move_forward_seconds(seconds)** function, with the parameter representing the duration of robot movement in seconds. However, for precise control over the robot's position on the map, we need functions that allow movement based on distance in centimeters.

**robot.move_forward_distance(dist)** - A function for moving the robot forward by the number of centimeters specified by the parameter **dist**.
**robot.move_backward_distance(dist)** - A function for moving the robot backward by the number of centimeters specified by the parameter **dist**.

Robot directions
![robot_directions](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_1/directions.png?raw=true)

## Assignment

Write a program for the robot to move **backward 35** centimeters and then **forward 20** centimeters. Good luck!

## Conclusion

Congratulations! You have gained knowledge about two crucial functions of the library that will prove valuable in the upcoming lessons.
