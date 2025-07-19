# Lesson 1: Monitoring Robot Data with print

## Lesson Objective

Learn how to use the `print` function to monitor and debug robot behavior by displaying real-time data.

---

## Introduction

When working with robots, it's essential to understand what's happening internally. The `print` function allows you to send data from your robot to be displayed on your screen, making debugging easier and helping you understand your robot's behavior better.

---

## Theory

### What is print?

`print` is a special function that sends text messages from your robot to the user interface. These messages appear in a console overlay on your screen.

### When to Use print

- Display sensor readings
- Track loop iterations
- Show calculated values
- Debug conditional statements
- Monitor robot state changes

### Basic Syntax

There are three main ways to use print in MicroPython:

```python
print("Your message here")         # Text only
print(variable_name)              # Variable value
print(f"Speed: {speed}")           # Text + variable (using f-string)
```

---

## Code Implementation

```python
from lineRobot import Robot
import time

print("Robot starting up...")

# Setting up variables
motor_speed = 150
print(f"Initial motor speed: {motor_speed}")

# Show robot information
robot = Robot()
print(f"Battery level: {robot.get_battery_percentage()}%")

while True:
    # Read a sensor
    light_value = robot.read_light_sensor()

    # Print the value
    print(f"Light sensor: {light_value}")

    # Small delay to avoid flooding messages
    time.sleep(1)
```

---

## Understanding the Logic

1. In `setup()`, we send initial messages showing the robot is starting
2. We display the initial settings like motor speed
3. In `loop()`, we continuously read a sensor value
4. We use `print` to send the value to our console
5. A delay prevents too many messages from being sent at once

---

## Assignment

Create a program that demonstrates all three ways of using the `print` function:

1. Create and initialize the following variables:

   - An integer called `motorSpeed` with a value of 150
   - A string called `robotStatus` with the value "Ready"
   - A float called `temperature` with a value of 25.5

2. In the `setup()` function:

   - Use `print` with text only to display "Robot diagnostic starting"
   - Use `print` with a variable only to display the value of `robotStatus`
   - Use `print` with combined text and variable to display "Motor speed set to: [motorSpeed]"
   - Use `print` with combined text and variable to display "Temperature: [temperature] C"

Your code structure should look like this:

```python
# Initialize variables
motor_speed = 150
robot_status = "Ready"
temperature = 25.5

# 1. Use print with text only
print("Robot diagnostic starting")
# 2. Use print with variable only
print(robot_status)
# 3. Use print with text + variable (motor speed)
print(f"Motor speed set to: {motor_speed}")
# 4. Use print with text + variable (temperature)
print(f"Temperature: {temperature} C")
```

Make sure your program demonstrates all three ways of using `print` to send information.

---

## Conclusion

The `print` function is a powerful tool for monitoring your robot's behavior in real-time. By displaying key values and state information, you can better understand how your code affects the robot's actions and quickly identify issues. Mastering the different formats of `print` will help you create more informative debug outputs for your future robot projects.
