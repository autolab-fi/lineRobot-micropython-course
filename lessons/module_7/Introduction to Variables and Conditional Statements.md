# **Lesson 1: Introduction to Variables and Conditional Statements**

## **Lesson Objective**

Learn how to declare and use variables in programming, and apply conditional logic using `if`, `else if`, and `else` statements to make decisions.

---

## **Introduction**

Variables are essential in microcontroller programming for storing information like sensor readings, motor speeds, and system states. In robot programming, we use conditional statements to make decisions based on these variables, creating intelligent behavior.

---

## **Theory**

### **What are Variables?**

Variables are named storage locations in the memory:

- `motor_speed = 200` # stores a motor speed value
- `battery_level = 3.7` # stores the battery voltage
- `is_on_line = True` # stores whether the robot detects a line

### **What is an If-Else Statement?**

It enables your robot to make decisions based on conditions:

```python
if condition1:
    # code runs if condition1 is true
elif condition2:
    # code runs if condition1 is false but condition2 is true
else:
    # code runs if all conditions above are false
```

### **Comparison Operators**

- `==` equal to
- `!=` not equal to
- `>` greater than
- `<` less than
- `>=` greater than or equal to
- `<=` less than or equal to

---

## **Example Implementation**

```python
import machine
import time

led_pin = machine.Pin(2, machine.Pin.OUT)
sensor_pin = machine.ADC(machine.Pin(36))

print("Sensor Monitoring Started")

while True:
    # Read sensor value
    sensor_value = sensor_pin.read()

    # Make decision based on threshold
    if sensor_value > 2000:
        led_pin.on()
        print("Sensor value HIGH")
    else:
        led_pin.off()
        print("Sensor value LOW")

    time.sleep(0.1)  # Small delay for stability
```

---

## **Understanding the Logic**

1. The program reads an analog sensor value.
2. The `if` statement compares this value against a threshold (2000).
3. If the value is above the threshold, the LED turns ON and "Sensor value HIGH" is sent.
4. Otherwise (`else`), the LED turns OFF and "Sensor value LOW" is sent.

---

## **Assignment: Line Detection**

In this assignment, you'll use two of the Octoliner sensors to detect line positions and send appropriate messages to the MQTT dashboard.

Your task is to:

1. Read all the sensor values (sensor 0 to sensor 7)
2. Compare all the sensor values
3. Use if-else if-else logic to determine different conditions
4. Send different messages based on which sensors detect the line

Complete the code below by adding the conditional logic:

```python
import machine
from octoliner import Octoliner
import time

# Initialize I2C (default ESP32 pins)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(245)

while True:
    # Read values from all sensors (0 - 7)
    sensor_values = [octoliner.analog_read(i) for i in range(8)]

    # YOUR CODE HERE:
    # Add if-elif-else statements to determine which sensor(s) detect the line
    # Remember: Values greater than 200 indicate the sensor is on the line
    # Print appropriate messages
    found = False
    for idx, value in enumerate(sensor_values):
        if value > 200:
            print(f"SENSOR {idx} ON LINE")
            found = True
    if not found:
        print("NO SENSORS ARE ON THE LINE")
    time.sleep(0.1)
```

### Expected Output

Your code should detect and report one of the following condition:

- Only return the messages for respective sensors that are ON the line
- If only sensor 5 is on the line: "SENSOR 5 ON LINE"
- If only sensor 6 is on the line: "SENSOR 6 ON LINE"
- This should be done for all the sensors.
- If none of the sensors detect the line: "NO SENSORS ARE ON THE LINE"

---

## **Conclusion**

In this lesson, you learned how variables store different types of data and how conditional statements make decisions based on those values. The `if-else if-else` structure lets you create more complex logic for your robot to respond to different sensor combinations, which is essential for creating responsive robot behavior.
