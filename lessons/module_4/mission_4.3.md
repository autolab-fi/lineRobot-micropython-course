---
index: 23
module: module_4
task: color_sensor_basics
previous: telemetry_reporting
next: color_classification
---

# Mission 4.3 Color Sensor Basics

## Objective
Understand the RGB color model, initialize the TCS34725 color sensor via the I2C interface, and read raw color data from the lunar surface across multiple zones.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
Your rover is now fully capable of navigating and reporting its physical status. However, to conduct true scientific research, it needs to analyze the geological composition of the ground. 

Today, we are activating the rover's spectrometer: the **TCS34725 Color Sensor**. This hardware will allow your robot to distinguish between different types of minerals based on their color signatures. 

![Color_sensor](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-4/color_sensor.jpg?raw=true)

## Theory

### 1. How the Color Sensor Works (The RGB Model)
To understand how the robot "sees" color, we need to understand the **RGB model**. RGB stands for **R**ed, **G**reen, and **B**lue. 

![RGB](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-4/rgb_explanation.jpg?raw=true)

Instead of seeing "Yellow" or "Purple" like a human eye, the sensor measures the intensity of red, green, and blue light reflecting off the ground. By combining these three basic values, the computer can identify any color. 

### 2. The I2C Communication Bus
In Module 3, you connected the Octoliner using the **I2C** interface with pins `SDA=21` and `SCL=22`. You might be wondering: *how can we connect a new color sensor if the line sensor is already using those exact same pins?*

The magic of I2C is that it acts as a **communication bus**. Like a shared telephone line. Multiple sensors can connect to the exact same two wires! To prevent them from talking over each other, every sensor is manufactured with a unique internal "address".
* The Octoliner's default address is `42`.
* The TCS34725 Color Sensor's address is `0x29` (which is 41 in standard numbers).

Because their addresses are different, the rover's brain can talk to both of them on the same pins without any conflict. For now, we will just initialize the color sensor on this bus:

```python
import machine
from tcs3472 import tcs3472

# 1. Initialize the shared I2C bus
bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))

# 2. Connect the color sensor to the bus
color_sensor = tcs3472(bus)
```

### 3. Reading the RGB Data
Once the sensor is connected, reading the data is very straightforward. We use the `.rgb()` method, which reads the surface and returns three integers representing the Red, Green, and Blue intensity values (ranging from 0 to 255)

```python
# Read the color data
r, g, b = color_sensor.rgb()
print(f"Red: {r}, Green: {g}, Blue: {b}")
```

## Assignment
Mission Control has positioned the rover at the start of a straight testing corridor containing colored geological anomalies. 

You must program the rover to act as a **Linear Scanner**: it will take a series of short steps forward, stopping to scan and report the raw RGB values of the surface after each step.

**Requirements:**
1. Set up the hardware: initialize the `Robot` and the `tcs3472` color sensor on the I2C bus (`sda=21`, `scl=22`).
2. Use a `for` loop with the `range` function to make the rover perform 6 identical scanning steps.
3. Inside the loop:
* Read the color using the `.rgb()` method and print the result using an f-string: `Scan - R:<value> G:<value> B:<value>`.
* Сommand the rover to move forward by **10 cm**.
* Add a `time.sleep(0.5)` delay after the movement to let the sensor stabilize over the ground.

Once your rover completes the scan, look closely at the data printed in your terminal. *Did you notice how the R, G, and B values changed drastically when the rover drove over a colored zone compared to the normal ground?*

> **Important:** Save your code or keep this tab open! You will use this exact loop as the foundation for your next mission.


## Conclusion
Spectrometer online! You have successfully established an I2C connection with a new piece of hardware and extracted raw RGB data from multiple zones.

Right now, the rover is just printing numbers. In the next mission, we will teach the robot's brain how to understand these numbers and classify them into actual human-readable colors!