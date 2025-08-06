# **Lesson 2: Loops and Conditional Logic**

## **Lesson Objective**

Learn how to repeat actions using `for` and `while` loops.

---

## **Introduction**

Loops are essential for microcontrollers perform repeated actions. Using loops saves you from writing the same code over and over, making your programs more efficient and easier to maintain.

---

## **Theory**

### **For Loop**

Runs code a fixed number of times - perfect for iterating through sensors or creating patterns:

```python
# Blink LED 5 times
import machine
import time

led_pin = machine.Pin(2, machine.Pin.OUT)
for i in range(1, 6):
    led_pin.on()
    time.sleep(0.2)
    led_pin.off()
    time.sleep(0.2)
    print(f"Blink #{i}")
```

### **While Loop**

Runs code while a condition is true - good for reading sensors until a condition is met:

```python
# Wait until sensor detects object
import machine
import time

sensor_pin = machine.ADC(machine.Pin(36))
sensor_value = 0
threshold = 1000  # example threshold
while sensor_value < threshold:
    sensor_value = sensor_pin.read()
    time.sleep(0.01)
```

### **Combining Loops with If-Else**

You can make decisions inside a loop to respond differently to changing conditions:

---

## **Example Implementation**

```python
# Example: Blink LED based on potentiometer value
import machine
import time

led_pin = machine.Pin(2, machine.Pin.OUT)
pot_pin = machine.ADC(machine.Pin(36))

print("Loop Example")

while True:
    # Read potentiometer to set number of blinks (map 0-4095 to 1-10)
    pot_value = pot_pin.read()
    num_blinks = int((pot_value / 4095) * 9) + 1

    print(f"Blinking LED {num_blinks} times")

    # For loop to blink LED
    for i in range(1, num_blinks + 1):
        if i % 2 == 0:
            # For even counts, blink fast
            led_pin.on()
            time.sleep(0.1)
            led_pin.off()
            time.sleep(0.1)
            print("Fast blink (even count)")
        else:
            # For odd counts, blink slow
            led_pin.on()
            time.sleep(0.4)
            led_pin.off()
            time.sleep(0.1)
            print("Slow blink (odd count)")
    time.sleep(1)
```

---

## **Understanding the Logic**

1. The program reads an analog value from a potentiometer to determine how many times to blink.
2. The `for` loop runs the specified number of times.
3. Inside the loop, an `if-else` statement checks if the current count is even or odd.
4. For even counts, the LED blinks quickly; for odd counts, it blinks slowly.
5. After completing all blinks, the program waits 1 second and repeats.

---

## **Assignment: Reading Multiple Octoliner Sensors**

Your task is to create a program that reads values from all 8 Octoliner sensors (0-7) using a for loop and prints their values to the MQTT Console.

Complete the code below:

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
    # Use a loop to read and print values from all 8 sensors (0-7)

```

Your goal is to use a loop to iterate through each sensor (indices 0-7), read its value, and print both the sensor number and value to the MQTT Console.

Expected output should look like:

```
Sensor 0: 245
Sensor 1: 127
Sensor 2: 85
...and so on for all 8 sensors
```

---

## **Conclusion**

In this lesson, you learned how to use loops to efficiently perform repeated tasks on the ESP32. The `for` loop is particularly useful for handling multiple sensors or outputs in sequence, while combining loops with conditional statements allows your robot to make complex decisions based on changing sensor inputs.
