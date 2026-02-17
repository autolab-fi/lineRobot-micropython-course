---
index: 28
module: module_3
task: processing_sensor_data
previous: intro_to_octoliner
next: alarm
---

## Introduction

In this lesson, you will learn how to...

## Task:
"here students will ask to do 15 “for” cycles: move_forward for 1 cm, scan with 2 sensors. Need to check that we found “geological layers” in the line and check the own function "



This version of the Processing sensor data task requires the student to output a specific text when sensor values indicate black line:

"Found geological layers" + sensor value
example:
        if sensor_3 > threshold:
            print(f"Sensor 3 : {sensor_3} Found geological layers!")

This message is referenced against robot position + offset from sensor to position  measuring point.

If these three points are made, the evaluation function returns: Success, the amount of detections at correct position and amount of total sensor triggers.

Most of these parameters can be changed from configuration variables in the verification function.

The use of for loops is not validated at the moment, as they can be used in various ways and at the making of this function its not clear wether the student has example syntax to complete or how they are to proceed.

## Testing

This task has been tested with sensor sensitivity of 243 and sensor trigger threshold of.

Here's an example of "student code" that was used for testing.

## Student Code:

#Imports
from lineRobot import Robot
import machine
import time
from octoliner import Octoliner


# Initialize I2C (default ESP32 pins)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

#test sensor connection
#print("I2C devices found:", i2c.scan())

robot = Robot()

sensi = 243

threshold = 900

dist = 1
speed = 50 ##Percentage!!

def detect_line(sensitivity, distance, threshold):
    octoliner.set_sensitivity(sensitivity)
    #print(f"Sensitivity: {sensitivity}\nSensor 3: {octoliner.analog_read(3)}\nSensor 4: {octoliner.analog_read(4)}")
    found_minerals = False

    for i in range(0,15):

        robot.move_forward_distance(distance)
        values = octoliner.analog_read_all()
        sensor_3 = octoliner.analog_read(3)
        sensor_4 = octoliner.analog_read(4)
        #print(sensor_3, sensor_4)
        if sensor_3 > threshold:
            print(f"Sensor 3 : {sensor_3} Found geological layers!")
        if sensor_4 > threshold:
            print(f"Sensor 4: {sensor_4} Found geological layers!")


        time.sleep(0.1)


detect_line(sensi, dist, threshold)
