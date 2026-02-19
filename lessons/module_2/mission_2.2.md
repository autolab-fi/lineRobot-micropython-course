---
index: 2
module: module_2
task: differential_drive
previous: electric_motors
next: defining_functions
---
# Mission 2.2 Differential Drive

## Objective
Learn about Differential Drive kinematics and examine the main challenges related to manual motor control using raw PWM values.

## Introduction
In the previous mission, you learned how electric motors work and how to turn them on using percentage speeds. But how does the robot actually steer? In this lesson, we will study the kinematics of the robot and learn how to control each wheel independently using raw hardware signals.

## Theory

### 1. Robot Kinematics
Let's consider the features of the robot from a kinematics perspective. The rover is equipped with a **differential drive**. This means it features two primary wheels controlled independently, allowing it to maneuver by varying the speed and direction of each wheel.


This setup provides high maneuverability, enabling the robot to rotate on the spot.

### 2. The Drifting Challenge
Differential drive offers great capabilities, but it also introduces challenges. Because of physical and mechanical issues (like microscopic gear inaccuracies, contamination, weight distribution, or surface friction), one motor might run slightly slower than the other — even with the exact same voltage applied!

If you just turn both motors on at exactly the same power, the robot might curve instead of driving straight. Achieving a perfect straight line requires you to manually adjust and balance the speeds of the individual motors.

### 3. Controlling Motors with Raw PWM
In the `lineRobot` library, you already used `run_motors_speed()` which takes percentages (-100 to 100). However, for precise individual tuning, we can use **raw PWM (Pulse Width Modulation)** values directly on the microchip.

* **`robot.run_motor_left(pwm_value)`**: Sends a raw PWM signal to the left motor. The value ranges from `-1023` to `1023`. Positive values rotate the wheel forward, negative values rotate it backward.
* **`robot.run_motor_right(pwm_value)`**: Works exactly the same way for the right motor, taking values from `-1023` to `1023`.

**IMPORTANT!** These functions only *start* the motors; they do not stop them. To stop the individual motors, you can use **`robot.stop_motor_left()`** and **`robot.stop_motor_right()`**, or just use the general **`robot.stop()`** to cut power to both.

## Assignment
In this lesson, we encourage you to experiment with the differential drive and fix the hardware drift!

Write a program that makes the robot drive straight for **3 seconds with a deviation of no more than 10 degrees**.

**Requirements:**
1. You **cannot** use the built-in library functions like `move_forward_distance`, `move_forward_speed_distance`, or `move_forward_seconds`.
2. Use the individual `run_motor_left()` and `run_motor_right()` functions.
3. Stop the motors afterward.

*Hint: You will likely have to run the program multiple times, adjusting the left and right raw PWM values individually (for example, 500 and 460) to achieve a perfectly straight line!*

## Conclusion
Congratulations! You learned about your robot's kinematics and encountered the first challenges of working with physical systems. By manually balancing the motors using raw PWM, you've taken a huge step toward advanced robotics. Next, we will wrap these commands into our very own custom functions!