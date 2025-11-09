# Lesson 1: Line Sensor Reactive LEDs

## Lesson objective
Practise building Python lists from sensor readings, index the list to inspect specific positions, and connect the resulting logic to LED output and telemetry text.

## Introduction
Lists keep related data in order, making them ideal for processing an array of line sensor values. In this lesson you will read the Octoliner array into a list, use indexing to inspect the centre sensors, turn the outcome into LED feedback, and print one heartbeat line that records what the robot saw.

## Theory

### Lists collect ordered sensor data
Python lists store items in sequence. Converting the Octoliner reading to a list preserves the order of the eight sensors so index `0` remains the left edge and index `7` the right edge.

```python
from octoliner import Octoliner

sensor = Octoliner()
sensor.begin(i2c)
readings = list(sensor.analog_read_all())
print(readings)
```

### Indexing finds the centre of the line
Lists use zero-based indexing. The centre pair of the Octoliner sits at indexes `3` and `4`. Comparing these values with a threshold highlights whether the robot is lined up with the track.

```python
LINE_THRESHOLD = 120
line_seen = readings[3] < LINE_THRESHOLD or readings[4] < LINE_THRESHOLD
```

### Turning a decision into LED output
The boolean stored in `line_seen` can immediately control both indicator LEDs. Matching the physical lights to the logic helps confirm your list processing is correct.

```python
robot.set_led_state(line_seen, line_seen)
```

### Capturing the result in a status line
Logging the readings alongside the LED state creates a traceable heartbeat. A formatted string keeps the list together so the verifier can replay the logic.

```python
state = "on" if line_seen else "off"
message = f"LINE_LED:state={state};readings={readings}"
robot.publish(message)
```

## Assignment
Write a script that stores the eight Octoliner readings in a list, checks the centre indexes against a threshold to decide whether the line is beneath the robot, switches both LEDs on when the line is seen, and publishes a single message formatted as `LINE_LED:state=...;readings=[...]`.

Platform API:
- `sensor = Octoliner(); sensor.begin(i2c)` – initialise the line sensor hardware.
- `sensor.analog_read_all()` – fetch all eight readings at once.
- `robot.set_led_state(left_on: bool, right_on: bool)` – control the left and right indicator LEDs.
- `robot.publish(message: str)` – send text output to the MQTT log.

The assignment is marked complete when the `line_sensor_leds` verification_function reads your `LINE_LED:` line, confirms the LED state matches the sensor logic, and verifies the recorded readings justify the decision.

## Conclusion
Great work! You used lists to organise sensor data, indexed specific positions to make a line-detection decision, and tied that logic to both LED control and telemetry output. The next lesson will build on list skills to choreograph PWM fades with loops.
