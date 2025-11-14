# Lesson 2: LED Flash Counter with Loops

## Lesson objective
Build confidence using Python loops and timing to repeat LED actions.

## Introduction
Loops let you repeat a block of code without copying the same command over and over. When you pair a loop with a short delay, you can choreograph LED flashes that communicate what the robot just sensed. This lesson practises counting iterations, waiting between flashes, and mapping sensor readings to a visible signal.

## Theory

### Looping a set number of times
The built-in `range()` function is a quick way to run a loop a specific number of times. The loop counter can help you customise each pass if you need to.

```python
for count in range(3):  # Runs three times: 0, 1, 2
    print("Flash", count + 1)
```

### Pausing between loop iterations
`time.sleep(seconds)` suspends the program for the given number of seconds. Adding a delay inside the loop spaces out each LED change so you can see the flashes individually.

```python
import time

time.sleep(2)  # Wait two seconds before the next command
```

### Choosing a count from sensor readings
The Octoliner array returns eight values in order from the left sensor to the right sensor. By scanning the readings for the darkest value, you can identify which sensor is currently over the line and use that position to decide how many times to flash.

```python
from octoliner import Octoliner

sensor = Octoliner()
sensor.begin(i2c)
readings = list(sensor.analog_read_all())
line_index = readings.index(min(readings)) + 1  # Convert to a 1-based position
```

## Assignment
Write a program that:

- reads all eight Octoliner values into a list and determines which sensor (1 through 8) is over the line
- flashes both front LEDs on and off that many times, using a two-second pause between each flash
- ensures the pattern finishes after the chosen number of flashes so the count matches the detected sensor position
- passes when the `analog_led_fade` verification_function observes six flashes separated by roughly two-second intervals

## Conclusion
Great job! You used loops, timing, and list processing to turn sensor data into an LED signal. Next, you'll apply list logic directly to live sensor readings and document the outcome with telemetry text.
