# Lesson 3: Telemetry Heartbeat with Status Levels

## Lesson objective
Reuse the module 6 STATUS telemetry fields, compute a health label from current robot data, and publish the expanded heartbeat in a single line.

## Introduction
Operators monitoring the remote lab robot need both raw telemetry and a quick “is everything okay?” indicator. In this lesson you will collect the name, speed, battery voltage, and readiness flag just like in module 6, classify the robot's overall health with a few threshold checks, package everything in a dictionary, and publish one STATUS heartbeat that includes the new field.

## Theory

### Capturing the base telemetry
Start by reading or defining the familiar STATUS values. The dashboard helper exposes convenience calls that mirror the module 6 API so your code stays short.

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
Task: Gather the four core telemetry values, derive the `health` field using the thresholds above, and publish a single STATUS line that contains all five entries.

Platform API:
- `robot.get_name() -> str` – return the robot's configured name.
- `robot.read_speed_cm_s() -> float` – measure the current forward speed in centimetres per second.
- `robot.read_battery_voltage() -> float` – report the present battery voltage.
- `robot.is_ready() -> bool` – report whether the robot is ready for commands.
- `robot.publish(message: str)` – send a telemetry heartbeat to the MQTT log.

Verification: The `telemetry_heartbeat_health` verification_function listens for the expanded STATUS line, checks that the numeric fields are present, and recomputes the health classification. Your submission succeeds when the published `health` value matches the verifier's thresholds.

## Conclusion
Excellent job! You extended the STATUS heartbeat with a derived health indicator while keeping the data structured in a dictionary. This workflow mirrors real-world telemetry design and prepares you for richer diagnostics in upcoming modules.

## Links
- [MicroPython Dictionaries](https://docs.micropython.org/en/latest/tutorial/data_types.html#dictionaries)
