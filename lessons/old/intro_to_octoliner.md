---
index: 27
module: module_3
task: intro_to_octoliner
previous: long_distance_race
next: electric_motor
---

## Introduction

In this lesson, you will learn how to read sensor values from the Octoliner sensor board.

## Task

Read and print the value from either of the central sensors.

## Verification

The verification function checks that the student code contains references to the correct sensors:

```python
has_sensor_3 = "analog_read(3)" in active_code
has_sensor_4 = "analog_read(4)" in active_code
```

These are then evaluated against numeric sensor values received from the student code.

## Example Student Code

```python
import machine
from octoliner import Octoliner
import time

# Initialize I2C (default ESP32 pins)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

# Test sensor connection
# print("I2C devices found:", i2c.scan())

sensi = 255

# Set sensitivity
octoliner.set_sensitivity(sensi)

# Read and print sensor values
print(f"Sensor 3 : {octoliner.analog_read(3)}")
print(f"Sensor 4 : {octoliner.analog_read(4)}")
```
