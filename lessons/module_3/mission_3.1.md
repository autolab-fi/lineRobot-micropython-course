---
index: 14
module: module_3
task: intro_to_octoliner
previous: while_loops
next: conditional_logic_reactive
---

# Mission 3.1 Introduction to Octoliner Sensor

## Objective
Understand the working principle of Infrared (IR) line sensors, establish an I2C connection, and read data from a single central sensor.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
Welcome back, Recruit! Up to this point, your rover has been driving "blind," relying entirely on internal motor encoders to estimate its position. But the lunar surface is unpredictable. To achieve true autonomy, the rover needs "eyes" to observe the ground beneath it.

Today, we are activating the rover's primary optical system: the Octoliner sensor.

## Theory

### 1. How IR Sensors Work
The robot is equipped with an 8-channel line sensor connected via the I2C interface. 

These sensors operate by emitting infrared light downward and detecting how much of it bounces back:
* **White Surfaces:** A light surface reflects a significant amount of IR light back to the sensor. The sensor's circuitry registers this strong reflection as a **low** numerical value.
* **Black Surfaces:** A dark surface absorbs most of the infrared light, resulting in a much lower reflection. The sensor detects very little reflection, which triggers a **high** numerical value in our system.

![IR Sensor Working](https://github.com/pranavk-2003/line-robot-curriculum/blob/assignments/images/module_7/IR's.png?raw=True)

This sharp difference in values is what allows the robot to differentiate between a black track and the surrounding floor.

### 2. Establishing the Connection (I2C)
Before we can ask the sensor what it sees, we must establish a communication channel. The Octoliner communicates with the ESP32 microcontroller using a protocol called **I2C**. Think of I2C as the language the "brain" and the "eyes" use to talk to each other.

To set this up, we initialize the I2C bus with specific communication pins (`SCL` and `SDA`):

```python
import machine
from octoliner import Octoliner
import time

# Initialize I2C with appropriate pins for your board
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000) 

# Create Octoliner instance (it has a default address of 42)
octoliner = Octoliner()

# Initialize Octoliner with the I2C interface
octoliner.begin(i2c)

# Set sensor sensitivity (0-255)
octoliner.set_sensitivity(245)
```

Notice the `set_sensitivity(245)` command at the end of the setup. This adjusts how strongly the sensor reacts to infrared light on a scale from 0 to 255; you might need to tweak this number depending on the ambient lighting in your testing facility to get clear readings.

### 3. Reading the Central Sensor
While the Octoliner has an array of 8 sensors (indexed from 0 to 7), looking at all of them at once can be overwhelming. For now, we will focus solely on Sensor 3, which is located near the center of the rover.

You can get the numerical value from this specific sensor using the `analog_read(index)` function.

## Assignment
Your task is to activate the optical array and stream data from the central sensor back to Mission Control. Do not initiate any movement commands.

**Requirements:**
1. Import the necessary libraries (`machine`, `Octoliner`).
2. Initialize the I2C connection and the `octoliner` object using the code snippet provided in the theory section.
3. Read and print the value of Sensor 3.

*Experiment:* Try to move your robot and observe how the printed numbers differ compared to an another surface!

## Conclusion
Sensor array online! You have successfully established an I2C connection and retrieved raw optical data from the rover. You should now clearly see how the numerical values change depending on the surface.

However, robots don't understand "high numbers" and "low numbers" inherently. In the next mission, we will learn how to use programming logic to make the robot stop exactly when it sees the line!