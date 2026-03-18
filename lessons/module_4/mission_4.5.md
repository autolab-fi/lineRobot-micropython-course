---
index: 25
module: module_4
task: multiple_sensors
previous: color_classification
next: data_logging
---

# Mission 4.5 Working with Multiple Sensors

## Objective
Combine the Octoliner and the Color Sensor in a single program. The rover must autonomously follow a black line while simultaneously scanning the ground, using an LED to signal anomalies without stopping.

## Introduction
Up until now, your rover has been doing one job at a time: either following a line blindly or scanning colors while driving straight. Real Lunar rovers perform multiple tasks simultaneously. 

Now is a major integration time. You will take your line-following algorithm from Module 3 and merge it with your smart color scanner from Mission 4.4!

## Theory

### 1. Sharing the Brain (The I2C Bus)
Remember how both the Octoliner and the Color Sensor use the I2C pins (`sda=21, scl=22`)? Because they have different hardware addresses, you only need to create **one** I2C bus and pass it to both sensors:

```python
# Create one shared bus
shared_bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))

# Connect both sensors to the same bus!
octoliner.begin(shared_bus)
color_sensor = tcs3472(shared_bus)
```

### 1. The Spam Problem (State Tracking)
Your line-following program runs inside a fast `while True` loop. If you just add a `print(color_name)` command inside that loop, the rover will print "Red" hundreds of times while driving over a single red square!

To fix this, we need to teach the rover to remember the last color it saw, and only print a message when the color changes. We do this by creating a memory variable outside the loop:

```python
last_color = "Floor"

while True:
    current_color = # ... detect color ...
    
    if current_color != last_color:
        print(f"New color detected: {current_color}")
        # React to the color here!
        
    last_color = current_color # Update memory for the next loop
```

## Assignment
Merge your systems! Program the rover to follow the track. If it sees a Green zone, it must turn on its LED (Pin 15) while continuing to drive. If it sees a Blue zone, the mission is complete, and it must stop permanently.

**Requirements:**
1. Hardware: Initialize the shared I2C bus, Octoliner, Color Sensor, and the LED on Pin 15.
2. Function: Copy your completed `detect_color_name(r, g, b)` function from Mission 4.4 and paste it into your code.
    * *Hint*: For your first test run, you might need to adjust your thresholds for Green and Blue, as the black line might interfere with the sensor. To see exactly what the robot sees, add a temporary print statement inside your function right after calculating the ratios: `print(f"R: {r_ratio} | G: {g_ratio} | B: {b_ratio}")`
3. * **Scanner Logic:** Inside the `while True` loop, read the color and use the "Spam Filter" (`last_color`) logic.
    * If Green: Turn LED ON.
    * If Blue: Stop the robot and `break` the loop.
    * If Floor: Turn LED OFF (so it turns off when leaving the Green zone).
4. Line Following: Below the color logic, add your line-following `if/elif` block.


## Conclusion
Congratulations! You have just programmed a truly multi-tasking robot. By using a shared I2C bus and a non-blocking LED signal, your rover can navigate complex terrain while simultaneously scanning for scientific anomalies. 

> **Important:** Save your entire script. In the final mission of this module, we will upgrade this code to turn the rover into a silent, data-gathering probe that generates a massive post-mission report!