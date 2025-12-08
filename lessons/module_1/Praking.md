---
index: 6
module: module_1
task: Parking
previous: long_distance_race
next: draw
---
# Lesson 15. Parking

## Objective

Drive the robot through a short sequence of movements and park it in a specific spot.

## Introduction

You already know how to move the robot forward, backward, and turn it. This lesson puts those skills together. You’ll guide the robot through a small route and stop it exactly where it needs to be.

## Theory

This is like any other program, just a list of steps to take in order. But for a robot, everything is time based. Each action affects the next one.

Parking is a perfect example of this. The robot must be in the correct location and orientation to be considered successful. But it can go straight and then turn and then move - what I'm saying is it essentially condenses movement into easier pieces of the puzzle. Also, using the compass rose pieces to differentiate movements are also helpful.
## Assignment
``` python
from lineRobot import Robot
robot=Robot()
robot.move_distance()
robot.turn_left()
```
You must program it so it can go in this route and park correctly, directionally.


You can refresh your memory of the library functions by revisiting the previous lessons.

## Conclusion

You are awesome! You've gained insight into the concept of a program and it's executor.