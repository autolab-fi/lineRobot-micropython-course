---
index: 12
module: module_2
task: encoder_theory
previous: for_loops
next: while_loops
---

# Mission 2.5 Encoder Theory

## Objective
Learn about encoders and their purpose in precise robot movement.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
Until now, the robot seemed to "just know" how far it traveled. But in reality, it was counting invisible pulses. In this lesson, we will bypass the "smart" library functions and look at the raw feedback from the wheels. By using manual motor control, we can see exactly how the sensors react to every move.

## Theory

### 1. What is an Encoder?
An encoder is a sensor that measures rotation. In robotics, we commonly use "rotary encoders" - devices that track how far something has rotated.

There are two main types:
1. **Absolute Encoders**: These tell you the exact position of rotation (like a compass showing North).
2. **Incremental Encoders**: These count steps of rotation (like counting your footsteps).

![Encoders](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-2/encoders.gif?raw=true)

Our platform is a differential drive robot based on the ESP32 microcontroller and MicroPython. It is specifically equipped with two DC motors with encoders – JGB37-520 178.

### 2. Getting Encoder Values
We will measure the rotation of the robot's wheels in degrees:
* Full wheel rotation forward = +360°
* Full wheel rotation backward = -360°

You will be able to use the following methods:
```python
robot.encoder_degrees_left()   # Get left wheel rotation in degrees
robot.encoder_degrees_right()  # Get right wheel rotation in degrees
robot.reset_left_encoder()     # Reset left encoder to 0
robot.reset_right_encoder()    # Reset right encoder to 0
robot.stop_motor_left()       # Stops left motor WITHOUT resetting the encoder
robot.stop_motor_right()      # Stops right motor WITHOUT resetting the encoder
```

### 3. The `math` Library and Pi (π)
To calculate real-world distances based on wheel rotation, we need to use the mathematical constant Pi (π). Instead of manually typing `3.14`, Python provides a built-in `math` library that contains the highly precise value of Pi.
To use it, you must import the library at the top of your script and access it using `math.pi`:

```python
import math
print("The value of Pi is:", math.pi)
```

### 4. Distance and Rotation
For a wheel with radius R, one full rotation covers a distance of L = 2 × π × R (the wheel's circumference). Our robot's wheels have a radius of **3.21 cm**, so one full rotation is approximately **20.2 cm**.


## Assignment: The Calibration Challenge
Your task is to find the perfect "pulse" for your robot to make it drive almost exactly one full wheel rotation and calculate the distance traveled.

**Requirements:**
1. **Reset:** At the very beginning of your code, reset both encoders to **0**.
2. **Calibration:** Experiment with the PWM value and the `time.sleep` duration to get the encoder readings for both wheels between **310 and 360 degrees**.
3. **Stopping:** **Do not use `robot.stop()`**. Instead, use `robot.stop_motor_left()` and `robot.stop_motor_right()` to keep the encoder data visible.
4. **Distance Calculation:** Use the math library to calculate how many centimeters the robot traveled based on the left wheel's degrees.
5. **Output:** Print the final encoder degrees and the calculated distance to the console.

**Hint:** To calculate distance, remember that a full 360° turn equals the wheel's circumference (2 × π × radius). Your distance is just a fraction of that circumference based on the angle you measured.

**Distance Formula:**
```python
radius = 3.21  # Robot wheel radius in cm
distance = (encoder_degrees / 360) * (2 * math.pi * radius)
```

## Conclusion

Congratulations! You have successfully calibrated your system and bridged the gap between raw sensor data and real-world measurements.

By reading the encoders directly, you've seen that the robot is no longer just "guessing" time—it is actually measuring its physical displacement. Understanding this feedback loop is what separates a simple toy from a precise autonomous machine. In the next mission, we will use While Loops to make the robot monitor these values automatically and stop exactly at a target distance!
