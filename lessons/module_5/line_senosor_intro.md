# **Lesson 1: Line Sensor and Black Line Detection**

## **Objective**

This lesson focuses on understanding how an Octoliner sensor detects black lines. You will learn the working principle of IR line sensors, explore challenges associated with black line detection, and implement a program to process sensor readings. By the end of this lesson, you will be able to detect black lines efficiently and use this data for robotics applications.

---

## **Introduction**

In this lesson, we will use an IR line sensor array to detect and follow a black line. The robot will read sensor values, determine the line's position, and adjust its movement accordingly.

---

## **Theory**

A line-following robot uses an array of infrared (IR) sensors to detect the track. These sensors measure reflected IR light, distinguishing between black (low reflection) and white (high reflection).

### **How IR Sensors Work**

Infrared sensors operate by emitting infrared light and detecting the amount of reflection. When placed over a white surface, a significant amount of IR light is reflected back to the sensor. However, a black surface absorbs more infrared light, resulting in lower reflection detected by the sensor. This principle is used to differentiate between the black line and the surrounding surface.

![IR Sensor Working](https://github.com/pranavk-2003/line-robot-curriculum/blob/assignments/images/module_7/IR's.png?raw=True)

### **IR Sensor Configuration**

The Octoliner sensor array consists of 8 sensors, each providing an analog value that indicates the intensity of reflected IR light.

![IR Sensor Logic](https://github.com/pranavk-2003/line-robot-curriculum/blob/assignments/images/module_7/IR_sensor_array.png?raw=True)

- **Central sensors (3 & 4)** → Move straight
- **Left sensors (0,1,2)** → Guide left turns
- **Right sensors (5,6,7)** → Guide right turns

### **Line Detection Mechanism**

- If the middle sensors detect the line, the robot moves forward.
- If the left sensors detect the line, the robot turns left by reducing the left motor speed.
- If the right sensors detect the line, the robot turns right by reducing the right motor speed.
- If no sensors detect the line, the robot stops or searches for the line.

### **Challenges in Line Following**

1. **Sensor Calibration**
   - The reflectivity of different surfaces varies, so sensor thresholds must be carefully tuned.
2. **Speed Control**
   - Sudden turns can cause instability, requiring smooth speed adjustments.
3. **Noise Filtering**
   - The sensor readings may fluctuate due to variations in ambient light or minor surface irregularities. Filtering techniques may be required to stabilize the readings.

---

## **Programming the Line Sensor**

The Octoliner sensor consists of 7 independent IR sensors, each capable of detecting IR reflection. In this section, we will read values from the sensor and determine whether a black line is detected. The process involves initializing the sensor, reading data from all 7 sensors, comparing these readings to a predefined threshold, and finally displaying the results. The program will run continuously in a loop, checking the sensor values and determining whether a black line is present.

The following example code initializes the Octoliner sensor, sets its sensitivity, and reads values from a single sensor and all sensors. The data obtained can then be used to decide whether the sensor detects a black or white surface.

```cpp
import machine
from octoliner import Octoliner
import time

# Initialize I2C with appropriate pins for your board (default ESP32 pins)
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)

# Create Octoliner instance (default address 42)
octoliner = Octoliner()

# Initialize Octoliner with the I2C interface
octoliner.begin(i2c)
octoliner.set_sensitivity(245)  # Adjust sensitivity if needed

while True:
    # Read data from the only one sensor
    value1 = octoliner.analog_read(0)
    print("Sensor 0 value:",value1)
    time.sleep(0.5)
    # Read data from the all sensors
    values = octoliner.analog_read_all()
    print("All sensor values:",values)
    time.sleep(0.5)
```

This code is a starting point and can be expanded to process all sensor readings effectively. The black threshold value may need adjustment based on the environment and surface properties.

---

## **Assignment**

Your task for this assignment is to write code that performs the following steps:

1. Read all the values from the Octoliner and print to console.
2. Move the robot forward by 25 cm.
3. Read all the values from the Octoliner sensors again and print to console.

This will help you observe how the sensor reading changes before and after the robot moves. Use this logic to understand sensor behavior and experiment with different sensitivity levels if

## **Conclusion**

Congratulations! You have successfully explored how IR sensors work and how they can be used for black line detection. This foundational knowledge is essential for building autonomous robots capable of following a predefined path. In the next lesson, we will learn how to use sensor data to control a robot’s movement, allowing it to follow a line autonomously.

By continuing to experiment with sensor readings and adjusting threshold values, you will gain a deeper understanding of sensor-based navigation. These skills will be useful in advanced robotics applications, including PID-controlled line followers, maze-solving robots, and autonomous navigation systems. Keep refining your code, and happy coding!
