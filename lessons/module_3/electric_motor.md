# Lesson 10: Electric Motor

## Lesson objective

Learn about electric motors.

## Introduction

In this lesson, you will learn about electric motors and the basic principles of DC motors.

## Theory

### What is Electric motor?

An electric motor is a device that converts electrical energy into mechanical energy using a magnetic field.

There are various classifications of electric motors, but they are mainly classified by the type of power supply voltage:

- Direct Current (DC) motors
- Alternating Current (AC) motors: asynchronous and synchronous

And by the method of power transmission:

- Brushed motors
- Brushless motors

In this lesson, we will take a closer look at direct current motors, also known as DC motors. DC motors are brushed motors, and we will examine how they work without delving deeply into the physics and mathematics!

### Structure of an Electric Motor

![image](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_3/inside_motor.jpg?raw=True)

An electric motor consists of a stator and a rotor. The stator creates a constant magnetic field, which in our case is provided by permanent magnets. The rotor is the rotating part and consists of a shaft with windings on several coils.

### Principle of Operation

We can't disassemble the motor online, so let's look at the GIF animation of the working DC motor along with a short description:

\*![image](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_3/animation.gif?raw=True)

Voltage of different polarities is applied to the brushes, creating magnetic fields in the coil windings that cause the rotor to rotate and continually remagnetize as it reaches brushes with opposite potentials, keeping the rotor in motion as long as voltage is supplied.

### Gearbox in Electric Motors

An electric motor can also be equipped with a gearbox, which transfers the rotational motion from the motor shaft to the mechanism. A gearbox can increase the maximum torque from the motor shaft and reduce the rotational speed. In the case of a line-following robot, the gearbox increases torque to allow the robot to move despite its weight and to overcome obstacles. A gearbox typically consists of a set of gears. You can see the internal structure of a gearbox in the photo below:

![image](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_3/small_size_gearbox.jpg?raw=True)

For example, the robot on the stage uses motors with speed 178 RPM (Revolutions Per Minute).

## Assignment

Let's practice more with robot movement: write a program for the robot to reach a point on the map. However, remember that you will not be able to use the built-in robot movement functions. The functions: **move_forward_distance**, **move_backward_distance**, **turn_left**, **turn_right**, **move_forward_seconds**, and **move_backward_seconds** will not work.

Instead, use the manual motor control methods:

- **run_motors_speed(left_speed, right_speed)** to set the speed of the left and right motors
- **stop()** to stop the motors

![image](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_3/finish_point.jpg?raw=True)

## Conclusion

Congratulations! In this lesson, you learned about the structure of a simple electric motor. Electric motors are a fascinating area in robotics, with a wide variety of types, each having its own application.

## Links

\*MichaelFrey (https://commons.wikimedia.org/wiki/File:DCMotor3Pol.gif), „DCMotor3Pol“, https://creativecommons.org/licenses/by-sa/4.0/legalcode
