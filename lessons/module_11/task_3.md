---
index: 37
module: module_11
task: visual_telemetry
previous: perimeter
next: debugging
---
# Task 3 Visual Telemetry
## Objective
Demonstrate your ability to combine `while True` loops, conditional logic, sensor reading, and GPIO hardware control.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Assignment
Your rover is approaching a dangerous lunar crevasse (represented by a black line). It must drive forward cautiously, detect the edge, execute an emergency stop, and send a visual confirmation signal back to the base using its onboard LED.

**Requirements:**
1. **Hardware Setup:** Initialize the I2C bus, the `Octoliner` sensor, and configure the onboard LED on Pin 15 as an Output (`machine.Pin.OUT`).
2. **Active Monitoring:** Create a `while True:` loop to move forward and continuously read the central sensors (Index 3 and/or 4).
4. **Emergency Stop:** Inside the loop, use an `if` statement. If the sensor value indicates the black line, immediately stop the motors and `break` out of the loop.
5. **Visual Signal:** After exiting the loop, write code to make the LED blink exactly **3 times** (turn on, wait 1 second, turn off, wait 1 second).

## Conclusion
Excellent! You have successfully closed the loop between environmental sensing and hardware feedback. Your rover can now save itself from hazards and communicate its status!