# **Lesson 1: Relay, P, and PI Controllers**

### Objective

Understand how different types of controllers work — Relay, Proportional (P), and Proportional-Integral (PI). Learn how each improves performance for a line-following robot.

### 1. **Relay Controller**

A relay controller is the simplest type of control system. It just turns motors fully left or right based on which side of the line the robot is on. It doesn't care how far the robot is from the center — it only knows left or right.

**Control rule:**

```
If error > 0 → turn full right
If error < 0 → turn full left
```

**Formula:**

```
u(t) = max_speed  if error > 0
u(t) = min_speed  if error <= 0
```

This results in a zigzag movement. The robot overcorrects and keeps switching directions.

---

## **Programming the Line Following Algorithm to use a Relay Controller**

This code will:

1. Read sensor values from all 8 sensors.
2. Decide the robot's movement based on sensor readings.
3. Move forward, turn left, turn right, or stop.

### **Code Implementation**

```python
import machine
from octoliner import Octoliner
from lineRobot import Robot
import time

# I2C setup (adjust pins if needed)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner(i2c)
robot = Robot()
speed = 30

# Black threshold for detection
MY_BLACK_THRESHOLD = 100

# Set sensor sensitivity
octoliner.set_sensitivity(230)

while True:
    # Read all sensor values
    sensor_values = [octoliner.analog_read(i) for i in range(8)]
    robot.run_motors_speed(speed, speed)

```

---

## **Understanding the Logic**

### **Sensor Detection and Movement**

The robot determines movement based on which sensors detect the black line.  
Below is a flowchart for a clear understanding:

![Flow](https://github.com/pranavk-2003/line-robot-curriculum/blob/assignments/images/module_7/FC.png?raw=True)

1. **If middle sensors (3 OR 4) detect the line** → Move forward.
2. **If left sensors (0 OR 1 OR 2) detect the line** → Turn left.
3. **If right sensors (5 OR 6 OR 7) detect the line** → Turn right.
4. **If no sensor detects the line** → Stop.

---

## **Assignment**

Modify the program to:

1. Write a program to make the robot line follow.
2. Fine-tune motor speeds for smoother movement.
3. Experiment with different thresholds to improve accuracy.
4. Ensure the robot successfully crosses both checkpoints to complete the Assignment.

---

## **Conclusion**

In this lesson, you have learned how to implement a basic **line-following algorithm** using an **Octoliner IR sensor array**. Understanding how to read sensor values and adjust movement based on input is fundamental to developing more advanced autonomous navigation systems.
