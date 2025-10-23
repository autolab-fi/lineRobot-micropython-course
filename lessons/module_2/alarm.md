---
index: 7
module: module_2
task: alarm
previous: headlights
next: None
---

# Lesson 7: Robot's alarm

## Lesson objective

Strengthen your understanding of the GPIO interface.

## Introduction

In this lesson, you will write a classic program to make an LED blink. This will help you become more confident in working with the GPIO interface.

## Theory

### LED

In the previous lesson, you learned about GPIO and LEDs. Now, let's take a closer look at how LEDs are connected.

![image](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_2/alarm_1.png?raw=true)

An LED has two contacts - anode and cathode. The anode is the longer one and it is connected to pin 15, while the cathode is connected to the ground. Electric current can only flow through the LED in one direction, from the anode to the cathode. When we send a high signal to pin 15, electric current flows through the LED from the anode to the cathode. When we send a low signal, the electric current doesn't flow. Remember, current flows through the LED only from the anode to the cathode.

### LED Blink

You already know how to turn on an LED using the **on()** function. In this lesson, let's write a more advanced program. We'll not only turn on the LEDs on the robot but also turn them off by sending a low logic signal to the pin. To make the LEDs blink, you need to create pauses between switching signals on the LED pins so that the microcontroller doesn't execute them instantly. The easiest way to pause a program is with the function **time.sleep()**.

The **time.sleep(seconds)** function pauses the program before executing the next command. This function takes a number as an argument, which represents the duration of the pause seconds.

Example:

```cpp
from lineRobot import Robot
import machine
import time

robot = Robot()

robot.move_forward_distance(20)
time.sleep(3)
robot.move_forward_distance(20)
```

When this program runs, the robot will move forward 20 centimeters, pause for 3 seconds, and then move backward.

## Assignment

Write a program for the robot to turn on the LEDs for 1 second, then turn them off for 1 second, and repeat this indefinitely.

Remember, the LEDs are connected to pins are connected to pins 15 and 2.

## Conclusion

Congratulations! Now you know how to control logical signals using the GPIO interface in a more complex manner!
