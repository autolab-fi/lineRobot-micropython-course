# Sandbox

## Objective

Here you can test different functions of the robot. The robot will execute your code for up to 20 seconds.

## Robot Description

This is a differential drive robot based on the ESP32 microcontroller and MicroPython.
The robot is equipped with:

* Two DC motors with encoders – JGB37-520 178.
* An 8-channel line sensor connected via the I2C interface.
* Two white LEDs.
* A TCS34725 color sensor.

Several library files for working with sensors and motors are pre-installed on the robot.

## Code Examples

### Robot Movement

```python
from lineRobot import Robot

# Initialize robot object
robot = Robot()
# Turn left by 45 degrees
robot.turn_left_angle(45)
# Move forward by 20 cm
robot.move_forward_distance(20)
```

### Reading Data from the Line Sensor

```python
import machine
from time import sleep
from octoliner import Octoliner

# Initialize I2C with appropriate pins for your board
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)

# Create Octoliner instance with default address (42)
octoliner = Octoliner()

# Initialize Octoliner with the I2C interface
octoliner.begin(i2c)
octoliner.set_sensitivity(230)

for i in range(20):
    # Read raw sensor values
    raw_values = octoliner.analog_read_all()
    print("Raw values:", raw_values)
    sleep(0.5)
```

### Color Sensor

```python
import machine
from tcs3472 import tcs3472
import time

bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
tcs = tcs3472(bus)

for i in range(20):
   print("Light:", tcs.light())
   print("RGB:", tcs.rgb())
   time.sleep(1)
```

### Controlling LEDs

```python
import machine
import time

# Initialize LED pins
led_left = machine.Pin(15, machine.Pin.OUT)
led_right = machine.Pin(2, machine.Pin.OUT)

# Blink both LEDs
for i in range(20):
    led_left.on()
    led_right.on()
    time.sleep(1)
    led_left.off()
    led_right.off()
    time.sleep(1)
```

## Useful Links

* Source file for the `lineRobot` library – *[link](https://github.com/autolab-fi/micropython-lineRobot-firmware/blob/master/ports/esp32/docs/lineRobot.md)*
* Source file for the TCS34725 library – *[link](https://github.com/autolab-fi/micropython-lineRobot-firmware/blob/master/ports/esp32/docs/color_sensor.md)*
* Source file for the line sensor library – *[link](https://github.com/autolab-fi/micropython-lineRobot-firmware/blob/master/ports/esp32/docs/line_sensor.md)*

## Conclusion

In this sandbox environment, you can freely experiment with your code and explore how the robot responds to your commands. This is a great way to practice motor control, sensor data reading, and interaction with hardware using MicroPython. Try combining the examples and creating your own mini-programs!
