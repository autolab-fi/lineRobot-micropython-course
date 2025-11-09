# Lesson 3: Telemetry Heartbeat with Status Levels

## Lesson objective
Explore how Python dictionaries organise named values and use them to summarise robot telemetry.

## Introduction
Dictionaries pair keys with values so you can label each piece of information you collect. In robotics they help group related telemetry, configuration settings, or status flags in one structure. By learning how to create dictionaries and derive new entries from existing data, you can craft clear reports that computers and humans can read.

## Theory

### Building a dictionary
Create a dictionary with curly braces and `key: value` pairs. Keys are usually strings, and values can be any data type.

```python
telemetry = {
    "name": "Explorer",
    "speed": 18.5,
    "battery": 9.4,
}
```

### Reading and updating dictionary entries
Use the key inside square brackets to access or modify a value. Adding a new key is as simple as assigning to a fresh label.

```python
robot_name = telemetry["name"]      # "Explorer"
telemetry["speed"] = 20.0           # Update existing entry
telemetry["ready"] = True           # Add a new entry
```

### Deriving new information
Dictionaries can store computed values alongside raw readings. Conditional logic lets you transform numbers into human-friendly labels.

```python
battery_v = telemetry["battery"]

if battery_v < 7.0:
    telemetry["health"] = "low"
elif battery_v < 9.0:
    telemetry["health"] = "warn"
else:
    telemetry["health"] = "ok"
```

### Formatting a status string
Once the dictionary contains all fields, format a single line that lists each key/value pair. Consistent formatting keeps automated checkers happy.

```python
status_line = (
    f"STATUS:name={telemetry['name']};"
    f"speed={telemetry['speed']};"
    f"battery={telemetry['battery']};"
    f"ready={telemetry.get('ready', False)};"
    f"health={telemetry['health']}"
)
robot.publish(status_line)
```

## Assignment
Write a program that gathers the robot name, speed, battery voltage, and readiness flag, computes a `health` label using the thresholds `low` (battery below 7.0 volts or speed 0), `warn` (battery below 9.0 volts, speed below 10, or not ready), and `ok` otherwise, stores everything in a dictionary, and publishes one line starting with `STATUS:` that lists all five fields. The lesson is complete when the `telemetry_heartbeat_health` verification_function receives your STATUS heartbeat, confirms the numeric data, and recomputes the health label to match your output.

## Conclusion
Excellent work! You organised telemetry with dictionaries, derived a readable health summary, and produced a consistent heartbeat message. Those skills prepare you for richer diagnostic reporting in later modules.
