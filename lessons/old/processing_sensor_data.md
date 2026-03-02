---
index: 28
module: module_3
task: processing_sensor_data
previous: intro_to_octoliner
next: alarm
---

## Introduction

In this lesson, you will learn how to process sensor data over multiple iterations and detect features in the environment.

## Task

Students are asked to complete 15 `for` loop cycles, moving forward 1 cm each cycle while scanning with sensors 3 and 4. The goal is to detect "geological layers" (black line) and report findings with sensor values.

## Verification

The verification function checks for the following:

- Student code outputs a message containing `"Found geological layers"` along with the sensor value that triggered it
- The message is cross-referenced against robot position with a sensor-to-position offset applied
- At least 2 valid detections at the correct position are required to pass

On success, the evaluation returns: the number of detections at the correct position and the total number of sensor triggers.

> **Note:** For loop structure is not validated at this time, as students may implement it in various ways.

Most evaluation parameters (position tolerance, sensor threshold, time limit, etc.) can be adjusted from the configuration block at the top of the verification function.

## Testing

Tested with:
- Sensor sensitivity: `243`
- Sensor trigger threshold: `900`

## Example Student Code

```python
# Imports
from lineRobot import Robot
import machine
import time
from octoliner import Octoliner

# Initialize I2C (default ESP32 pins)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

# Test sensor connection
# print("I2C devices found:", i2c.scan())

robot = Robot()

sensi = 243
threshold = 900
dist = 1
speed = 50  # Percentage

def detect_line(sensitivity, distance, threshold):
    octoliner.set_sensitivity(sensitivity)
    found_minerals = False

    for i in range(0, 15):
        robot.move_forward_distance(distance)
        values = octoliner.analog_read_all()
        sensor_3 = octoliner.analog_read(3)
        sensor_4 = octoliner.analog_read(4)

        if sensor_3 > threshold:
            print(f"Sensor 3 : {sensor_3} Found geological layers!")
        if sensor_4 > threshold:
            print(f"Sensor 4: {sensor_4} Found geological layers!")

        time.sleep(0.1)

detect_line(sensi, dist, threshold)
```
