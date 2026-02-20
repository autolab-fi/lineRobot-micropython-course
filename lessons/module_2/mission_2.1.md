---
index: 1
module: module_2
task: electric_motors
previous: sequential_navigation
next: differential_drive
---
# Mission 2.1 Electric Motors

## Objective
Learn about electric motors, gearboxes, and how to manually turn them on and off to reach a specific target.

## Introduction
In Module 1, you learned how to drive the rover using built-in commands. But to truly master robotics, you need to understand the hardware. In this lesson, you will learn about the basic principles of DC motors and see how electrical energy transforms into physical movement!

## Theory

### 1. What is an Electric Motor?
An electric motor is a device that converts electrical energy into mechanical energy using a magnetic field. There are various types of motors, but for our rover, we use Direct Current (DC) brushed motors.

![inside_motor](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-2/inside_motor.jpg?raw=true)

An electric motor consists of two main parts:
* **Stator:** The stationary outer part that creates a constant magnetic field, which in our case is provided by permanent magnets.
* **Rotor:** The rotating inner part that consists of a shaft with wire windings on several coils.

### 2. Principle of Operation
When voltage of different polarities is applied to the brushes, it creates magnetic fields in the coil windings. This causes the rotor to rotate as it constantly pushes against and pulls towards the stator's magnets. It keeps the rotor in motion as long as voltage is supplied.

![motor_animation](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-2/animation.gif?raw=true)

### 3. Gearbox in Electric Motors
Raw electric motors spin very fast but don't have much pushing power (torque). If we connected wheels directly to the motor shaft, the robot wouldn't be able to move its own weight! 

To fix this, an electric motor can be equipped with a **gearbox**. 

![small_size_gearbox](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-2/small_size_gearbox.jpg?raw=true)

A gearbox transfers the rotational motion from the motor shaft to the mechanism. It consists of a set of gears that greatly increase the maximum torque while reducing the rotational speed. Our rover's geared motors run at a steady **178 RPM** (Revolutions Per Minute).

### 4. Manual Motor Control
Until now, you used built-in functions that handled all the complex logic for you. Now, you will control the raw power directly using these methods:
* **`robot.run_motors_speed(left_speed, right_speed)`**: Sets the speed of the left and right motors simultaneously. The speed is given as a percentage, ranging from `-100` to `100`.
* **`robot.stop()`**: Cuts power to the motors.

**Important Rule:** The `run_motors_speed` function turns the motors on and leaves them running! To make the robot move for a specific duration and then stop, you need to use the `time.sleep(seconds)` command. This command "pauses" the program for the specified number of seconds while the motors continue to spin, after which you can call `robot.stop()`.

## Assignment
Let's practice more with robot movement: write a program for the robot to reach a point on the map. 

However, you will not be able to use the built-in robot movement functions. The functions: `move_forward_distance`, `move_backward_distance`, `turn_left`, `turn_right`, `move_forward_seconds`, and `move_backward_seconds` will **not** work.

**Requirements:**
1. Use `run_motors_speed(left_speed, right_speed)` to start moving towards the finish point.
2. Use `time.sleep()` to wait for the exact amount of time needed to reach the target.
3. Use `stop()` to stop the motors once the robot is on the point.

![finish_point](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-2/finish_point.jpg?raw=true)

*Hint: You will need to run the code multiple times, adjusting your `time.sleep()` value until the robot stops exactly on the target!*

## Conclusion
Congratulations! In this lesson, you learned about the structure of a simple electric motor. Electric motors are a fascinating area in robotics, with a wide variety of types, each having its own application. Next, we will look at how having two separate motors allows us to steer the robot!