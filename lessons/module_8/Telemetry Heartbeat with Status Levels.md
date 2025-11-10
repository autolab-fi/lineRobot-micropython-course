# Lesson 1: Telemetry Heartbeat with Status Levels

## Lesson objective
Understand how Python dictionaries store related information with named keys.

## Introduction
Dictionaries pair keys with values so you can label the data you gather. They make it easy to keep related facts together, update individual pieces, and look them up by name. In this lesson you will practise building small telemetry dictionaries and turning their contents into readable status summaries.

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

if battery_v < 6:
    telemetry["health"] = "critical"
elif battery_v < 9:
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

- creates three dictionaries named `robot1`, `robot2`, and `robot3`, each containing a `name` field and a `battery` field with values `3`, `8`, and `10` respectively
- uses if/elif/else logic to add a `status` field to each dictionary so that batteries below `6` read as `critical`, batteries below `9` read as `warn`, and all higher values read as `ok`
- prints one line per robot using `print(f"{data['name']} status={data['status']} battery={data['battery']}")` so the output lists the name first, followed by the computed status and the battery value
- passes the checker only when the output shows `robot1 status=critical battery=3`, `robot2 status=warn battery=8`, and `robot3 status=ok battery=10` (in any order)

## Conclusion
Excellent work! You organised telemetry with dictionaries, derived a readable health summary, and produced a consistent heartbeat message. Those skills prepare you for richer diagnostic reporting in later modules.
