# Lesson 1: Line Sensor Reactive LEDs

## Lesson objective
Collect Octoliner sensor readings into a Python list, decide whether the robot is centred over the line, and drive the status LEDs while reporting the result through MQTT.

## Introduction
In the remote lab you can read the Octoliner line sensor array and light the robot's front LEDs from your MicroPython script. This lesson shows how to capture all eight sensor values, use list indexing to decide if the line is under the robot, mirror that decision on the LEDs, and publish a single heartbeat line that documents both the readings and the LED state.

## Theory

### Reading the Octoliner array
The Octoliner library exposes `analog_read_all()` so you can snapshot all eight channels in one call. Wrapping the result in `list()` keeps the values ordered from left (index `0`) to right (index `7`).

```python
from octoliner import Octoliner

sensor = Octoliner()
sensor.begin(i2c)
readings = list(sensor.analog_read_all())
print(readings)
```

### Checking the centre sensors
A dark line typically produces lower readings than the surrounding floor. Comparing the centre pair (indexes `3` and `4`) against a threshold such as `120` lets you detect whether the robot is still aligned with the track.

```python
LINE_THRESHOLD = 120
line_seen = readings[3] < LINE_THRESHOLD or readings[4] < LINE_THRESHOLD
```

### Driving indicator LEDs
Create a small dictionary to describe the desired LED states so both channels follow the same decision. The dashboard exposes `robot.set_led_state(left_on, right_on)` to toggle the hardware.

```python
led_state = {
    "left": "on" if line_seen else "off",
    "right": "on" if line_seen else "off",
}
robot.set_led_state(line_seen, line_seen)
```

### Publishing a diagnostic heartbeat
The verifier watches MQTT for a single summary line that begins with `LINE_LED:`. Include both the logical state and the raw readings so the checker can compare your code's decision with the sensor data.

```python
message = "LINE_LED:state={state};readings={values}".format(
    state=led_state["left"],
    values=readings,
)
robot.publish(message)
```

## Assignment
Task: Program the robot to read the Octoliner array, decide whether the centre sensors see the line, mirror that decision on both LEDs, and publish one MQTT line containing the LED state and the eight readings.

Platform API:
- `sensor = Octoliner(); sensor.begin(i2c)` – initialise the line sensor.
- `sensor.analog_read_all()` – return a tuple of eight raw readings.
- `robot.set_led_state(left_on: bool, right_on: bool)` – turn each indicator LED on (`True`) or off (`False`).
- `robot.publish(message: str)` – send a text heartbeat to the dashboard MQTT log.

Verification: Your code will pass when the `line_sensor_leds` verification_function receives a line starting with `LINE_LED:`, confirms the `state` field matches the actual LED logic, and validates that the printed readings support the decision.

## Conclusion
Great work! You now have a repeatable way to read the Octoliner, reason about its centre channels with lists, and drive both LEDs and telemetry from the same logic. The next lesson will build on this by exploring loops and PWM to create smooth LED animations.

## Links
- [Octoliner MicroPython Library](https://github.com/Robopoly/octoliner-micropython)
