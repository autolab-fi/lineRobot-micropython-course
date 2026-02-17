---
index: 27
module: module_3
task: intro_to_octoliner
previous: long_distance_race
next: electric_motor
---


## Introduction

In this lesson, you will learn how to...

## Task:

Task is simple, to read and print the value from either of the central sensors.

## Verification

The verification function checks code for:
has_sensor_3 = "analog_read(3)" in active_code
has_sensor_4 = "analog_read(4)" in active_code

and evaluates them agains numeric sensor values received from student code.

## Example student code

import machine
from octoliner import Octoliner
import time

# Initialize I2C (default ESP32 pins)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

#test sensor connection
#print("I2C devices found:", i2c.scan())

sensi = 255
#set sensitivity
octoliner.set_sensitivity(sensi)

#read
print(f"Sensor 3 : {octoliner.analog_read(3)}")
print(f"Sensor 4 : {octoliner.analog_read(4)}")