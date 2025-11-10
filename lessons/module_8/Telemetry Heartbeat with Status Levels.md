# Lesson 1: Telemetry Heartbeat with Status Levels

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
speed = telemetry["speed"]
ready = telemetry.get("ready", True)

if battery_v <= 5.0 or speed == 0:
    telemetry["health"] = "low"
elif battery_v < 9.0 or speed < 10 or not ready:
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
print(status_line)
```

## Assignment
Write a program that:

- builds a telemetry dictionary with sensible defaults (for example, name, readiness flag, speed above 10, and `battery=10`) and prints a `STATUS:` line whose health field resolves to `ok`
- simulates one volt of battery drain each second while calling `robot.move_forward_seconds(4)` so the robot drives forward for four seconds
- updates the same dictionary to reflect the new battery level of 6.0 volts, recomputes the health label as `warn`, and prints a second `STATUS:` line
- completes the lesson only when both outputs are received in order: the first with `battery=10` and `health=ok`, the second with `battery=6` and `health=warn`

## Conclusion
Excellent work! You organised telemetry with dictionaries, derived a readable health summary, and produced a consistent heartbeat message. Those skills prepare you for richer diagnostic reporting in later modules.
