# **Lesson 3: Arrays and Sensor Data History Analysis**

## **Lesson Objective**

Understand how to use arrays to store and analyze sensor data.

---

## **Introduction**

Arrays allow you to store multiple values under one name. For robotics applications, arrays are perfect for handling multiple sensor readings, storing historical data, or tracking patterns over time. Instead of creating separate variables for each measurement, arrays group them together, making it easier to loop through and analyze data.

---

## **Theory**

### **What is an Array?**

An array is a fixed-size collection of elements of the same type.  
Example:

```python
sensor_values = [325, 410, 102, 890, 512, 78, 210, 455]
```

### **Accessing Elements**

You can access array items using indexes (starting from 0).  
`sensorValues[0]` → 325 (first sensor)  
`sensorValues[3]` → 890 (fourth sensor)

### **Looping Through Arrays**

Use a `for` loop to process all elements.

```python
for i in range(8):
    message = f"Sensor {i}: {sensor_values[i]}"
    print(message)
```

---

## **Example Implementation**

```python
# Sample light sensor readings
light_levels = [855, 230, 990, 470, 600, 120]
bright_count = 0

# Process the array with a loop
for i in range(6):
    if light_levels[i] > 500:
        bright_count += 1
        message = f"Sensor {i} detects bright light"
        print(message)

# Print count of bright sensors
print(f"Number of bright sensors: {bright_count}")

# Wait 3 seconds before repeating (if in a loop)
# time.sleep(3)
```

---

## **Understanding the Logic**

1. The program has an array of 6 light sensor readings.
2. A loop checks each reading using an `if` condition.
3. If the value is greater than 500, it's considered "bright" and counted.
4. Each bright sensor is reported, and the total count is displayed.
5. This same approach can be used to process any type of sensor data.

---

## **Advanced Array Techniques**

### **Storing Multiple Measurements**

```python
# Store three sets of sensor readings
first_measurement = [0] * 8
second_measurement = [0] * 8
third_measurement = [0] * 8

# Take readings at different positions
for i in range(8):
    first_measurement[i] = octoliner.analog_read(i)
# Move robot and take more readings...
```

### **Processing All Stored Data**

```python
# Send all measurements systematically
import time
for i in range(8):
    print(first_measurement[i])
    time.sleep(0.1)  # Prevent message loss
    print(second_measurement[i])
    time.sleep(0.1)
    print(third_measurement[i])
    time.sleep(0.1)
```

---

## **Assignment: Sensor Data Collection and Analysis**

For this assignment, you'll create a program that:

1. Uses arrays to store sensor readings from three different robot positions
2. Moves the robot between measurements to collect varied data
3. Systematically sends all collected data via MQTT

Complete the code below:

```python
import machine
from octoliner import Octoliner
from lineRobot import Robot
import time

# Initialize I2C (default ESP32 pins)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(245)
robot = Robot()

# 1. Create three arrays to store 8 sensor readings each
# 2. Take first set of sensor readings
# 3. Move robot forward for 10cm and take second set of readings
# 4. Move robot forward again by 10cm and take third set of readings
# 5. Use loops to send all 24 values systematically using print() with delays(100ms)
```

### **Expected Behavior:**

- The robot should collect 24 total sensor values (8 sensors × 3 positions)
- Values should be sent systematically using print() with proper delays(100ms)
- The verification system will check whether the sensor outputs are as expected.

---

## **Conclusion**

Arrays are essential for organizing and processing multiple related values in robotics. By combining arrays with movement commands and systematic data collection, you can create programs that gather comprehensive sensor data over time and space. This approach is fundamental for advanced robotics applications like mapping, pattern recognition, and environmental analysis. The ability to store, organize, and systematically process sensor data using arrays is a crucial skill for any robotics programmer.
