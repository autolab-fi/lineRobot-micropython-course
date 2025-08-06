# Lesson 8: Differential drive

## Lesson objective

Lear about Differential Drive Control of a Robot

## Introduction

In this lesson, we will study the kinematics of the robot and examine the main issues related to motor control on the robot.

## Theory

### Robot Kinematics

Let's consider the features of the robot from the kinematics perspective: The robot in the images is equipped with differential drive, featuring two primary wheels controlled independently, allowing it to maneuver by varying the speed and direction of each wheel. This setup provides high maneuverability, enabling the robot to rotate on the spot.

![image](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_3/robot_image.png?raw=True)

### Challenges

As mentioned earlier, differential drive offers great capabilities for a robot, but it also introduces numerous challenges that can be addressed through software and sensors. For instance, it's necessary to synchronize the motors' movements so they run at the same speed despite mechanical issues: one motor might run slower than the other, even with the same voltage applied, due to gear inaccuracies, contamination, or other things. How can we synchronize the motors and control their speeds in such cases? Achieving this requires implementing control laws to manage the motors' movements.

### Controlling Motor

In the **lineRobot** library, functions for controlling the motors are already written, and they can be used to control the motors individually.

The function **run_motor_left(speed)** is used to send a signal to the motors, with the speed parameter specified as a percentage. The speed can be either negative or positive, ranging from -1023 to 1023. When the parameter is greater than 0, the left wheel will rotate forward, and if the parameter is less than 0, the wheel will rotate in the opposite direction. IMPORTANT! These functions only start the motors; they do not stop them. To stop the motors, you can use specified function or provide 0 as parameter for the funtion **run_motor_left(0)**.

The function **run_motor_right(speed)** works similarly for the right motor.

To stop the motors, you can also use the functions **stop_motor_right()** and **stop_motor_left()**.

## Assignment

In this lesson, we encourage you to experiment with the differential drive of the robot: write a program that makes the robot drive straight for 3 seconds with a deviation of no more than 10 degrees. You will not be able to use the **move_forward_distance**, **move_forward_speed_distance**, or **move_forward_seconds** functions from the library. You will likely have to send the program multiple times, adjusting the motor speeds to achieve the desired result.

### Hint

We recommend reviewing the previous lesson to remember the **time.sleep** function, which will help you turn on the robot's motors for exactly 3 seconds and then turn them off.

## Conclusion

Congratulations! You learned more about your robot and encountered the first challenges of working with physical systems. In the upcoming lessons, you will learn about writing control laws to fully manage the robot's movement and ensure smooth and even motion.
