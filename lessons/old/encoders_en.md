---

index: 1
module: module_5
task: encoder
previous: electric_motor
next: odometer

# Lesson 1: Encoder

## Lesson objective

Learn about encoders and its purpose in robot movement.

## Introduction

In previous lessons, we controlled the robot's movement using time and motor speed. However, this method isn't very precise because motors can behave differently depending on battery level, surface friction, and mechanical variations. To make our robot move more accurately, we need to measure how much each wheel actually turns. This is where encoders come in!

## Theory

### What is an Encoder?

An encoder is a sensor that measures rotation. In robotics, we commonly use "rotary encoders" - devices that track how far something has rotated. There are two main types:

1. **Absolute Encoders**: These tell you the exact position of rotation (like a compass showing North)
2. **Incremental Encoders**: These count steps of rotation (like counting your footsteps)

### Getting Encoder Values in Our Robot

In this lesson we will measure the rotation of the robot's wheels in degrees, where:

- Full wheel rotation forward = +360°
- Full wheel rotation backward = -360°
  Each wheel has its own encoder, so we will measure the rotation of each wheel separately. Left encoder for the left wheel and right encoder for the right wheel.

You will be able to use the following methods in MicroPython:

```python
robot.encoder_degrees_left()   # Get left wheel rotation in degrees
robot.encoder_degrees_right()  # Get right wheel rotation in degrees
robot.reset_left_encoder()     # Reset left encoder to 0
robot.reset_right_encoder()    # Reset right encoder to 0
```

### Distance and Rotation

For a wheel with diameter D, one full rotation covers a distance of π \* D. Our robot's wheels have a diameter of 3.5 cm, so:

- One full rotation = 3.5 \* π ≈ 11 cm

This relationship helps us convert between rotation degrees and actual distance traveled.

## Assignment

Write a program that demonstrates encoder measurements by:

1. Moving the robot forward exactly one wheel rotation
2. Then moving backward one rotation
3. Printing encoder values at three points:
   - Start position (after reset)
   - After forward movement
   - After backward movement

Use our new methods to get the encoder values for left and right wheels accordingly. Print the values and compare them at different robot's moving stages.

```python
from lineRobot import Robot
import time

robot = Robot()

# Reset encoder values
robot.reset_left_encoder()
robot.reset_right_encoder()

# Read start position values
print("START POSITION")
print("LEFT:")
# print(robot.encoder_degrees_left())  # TODO: this line should be done by student
print("RIGHT:")
# print(robot.encoder_degrees_right())  # TODO: this line should be done by student

# Move forward
robot.move_forward_distance(3.5 * 3.14159)  # one rotation forward (wheel diameter * pi)
print("FORWARD MOVEMENT POSITION")
print("LEFT:")
# print(robot.encoder_degrees_left())  # TODO: this line should be done by student
print("RIGHT:")
# print(robot.encoder_degrees_right())  # TODO: this line should be done by student

time.sleep(0.5)

# Move backward
robot.move_backward_distance(3.5 * 3.14159)  # one rotation backward (wheel diameter * pi)
print("BACKWARD MOVEMENT POSITION")
print("LEFT:")
# print(robot.encoder_degrees_left())  # TODO: this line should be done by student
print("RIGHT:")
# print(robot.encoder_degrees_right())  # TODO: this line should be done by student
```

## Conclusion

You've learned about encoders - sensors for precise robot movement. Understanding how they work and how to read their values is crucial for advanced robot control. In the next lesson, we'll use encoders to build an odometer that tracks the robot's total distance traveled!
