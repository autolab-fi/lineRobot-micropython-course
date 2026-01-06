---
index: 6
module: module_1
task: Parking
previous: long_distance_race
next: draw
---
# Lesson 15. Parking

## Objective

Program the robot to drive along a short route and park at a specific position and direction.

## Introduction

So far, you have learned how to move the robot forward, backward, and turn it.
In this lesson, you will combine those actions to complete a real task: parking.

Parking is not about one single move. It is about doing the right moves in the right order so the robot ends up exactly where it should be.

## Theory

A robot program is simply a sequence of instructions:

- move forward

- turn left or right

- move again

Each instruction changes the robot’s position and direction.
Because of this, small errors early in the program can affect the final result.

For this lesson, how you move is flexible, but where you end is not.

The parking task is considered successful only if:

- the robot reaches the correct final position

- the robot is facing the correct direction

The robot may take any valid route to get there.
## Assignment
Write a program that:

1. Starts from the default reset position

2. Drives the robot through a short route using movement commands

3. Stops with the robot parked in the correct spot and orientation

You must use the robot movement functions you learned earlier, such as:

- moving forward by a distance

- turning left or right

The verification system will not check your commands directly.
It will only check the robot’s final position and angle.

If the robot is close enough to the required parking spot and direction, the task passes.

## Conclusion
Great job reaching this lesson.
Parking combines planning, sequencing, and precision.
Once you understand this, you understand how real robot programs work.

You are awesome! You've gained insight into the concept of a program and it's executor.
