# Lesson 3: Telemetry Heartbeat with Status Levels

## Lesson objective
Organise telemetry fields inside a Python dictionary, derive a health label from numeric thresholds, and format a complete STATUS heartbeat string.

## Introduction
When data points belong together, dictionaries provide named access that keeps related values readable. This lesson shows how to gather the STATUS telemetry fields, add a derived `health` key using conditional checks, and produce a single formatted heartbeat line.

## Theory

### Capturing the base telemetry
Begin by calling the helper functions that return the raw data. Each variable becomes a dictionary entry later.

```python
robot_name = robot.get_name()
speed_cm_s = robot.read_speed_cm_s()
battery_v = robot.read_battery_voltage()
is_ready = robot.is_ready()
```

### Classifying health from thresholds
A derived field summarises the numbers. This course uses three bands:

- `low` if the battery is below `7.0` volts or the speed is `0` cm/s.
- `warn` if the battery is below `9.0` volts, the speed is below `10` cm/s, or the robot is not ready.
- `ok` for all other cases.

```python
if battery_v < 7.0 or speed_cm_s == 0:
    health = "low"
elif battery_v < 9.0 or speed_cm_s < 10 or not is_ready:
    health = "warn"
else:
    health = "ok"
```

### Organising data with a dictionary
Dictionaries keep related telemetry together, making it easy to format the outgoing message and to adjust the structure in later modules.

```python
telemetry = {
    "name": robot_name,
    "speed": speed_cm_s,
    "battery": battery_v,
    "ready": is_ready,
    "health": health,
}
```

### Publishing the extended STATUS line
The verifier expects a single string beginning with `STATUS:` followed by the five key/value pairs separated by semicolons. Format carefully so the checker can parse each field.

```python
status_line = (
    f"STATUS:name={telemetry['name']};"
    f"speed={telemetry['speed']};"
    f"battery={telemetry['battery']};"
    f"ready={telemetry['ready']};"
    f"health={telemetry['health']}"
)
robot.publish(status_line)
```

## Assignment
Write a program that reads the robot name, speed, battery voltage, and readiness flag, computes the `health` label with the provided thresholds, stores everything in a dictionary, and publishes one string that begins with `STATUS:` and lists all five key/value pairs.

Platform API:
- `robot.get_name() -> str` – return the robot's configured name.
- `robot.read_speed_cm_s() -> float` – measure the current forward speed in centimetres per second.
- `robot.read_battery_voltage() -> float` – report the present battery voltage.
- `robot.is_ready() -> bool` – report whether the robot is ready for commands.
- `robot.publish(message: str)` – send a telemetry heartbeat to the MQTT log.

Completion is recorded when the `telemetry_heartbeat_health` verification_function reads your expanded STATUS line, confirms all numeric fields, and recomputes the `health` label to match your output.

## Conclusion
Excellent job! You kept related telemetry inside a dictionary, generated a health summary with conditional logic, and published a neatly formatted STATUS heartbeat. These dictionary skills pave the way for more advanced diagnostics in future lessons.
