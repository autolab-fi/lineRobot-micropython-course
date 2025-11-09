# Lesson 1: Line Sensor Reactive LEDs

## Lesson objective
Understand how Python lists store ordered data and how to apply them in your robot programs.

## Introduction
Lists are Python's flexible containers for ordered values. They let you group readings, configuration numbers, or status text so the items stay in sequence. Once you can gather data in a list and access positions by index, you can reuse the same pattern for sensors, LED patterns, or any other structured information.

## Theory

### Creating and viewing lists
A list literal surrounds comma-separated items with square brackets. You can mix data types, although keeping similar values together makes processing easier.

```python
numbers = [10, 20, 30, 40]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "two", 3.0, True]
```

### Accessing and updating elements
List indexes start at `0`. Use the index inside square brackets to read or assign a value.

```python
first_number = numbers[0]      # 10
third_fruit = fruits[2]        # "cherry"
fruits[1] = "blueberry"        # Update the second item
```

### Expanding and reducing a list
Lists grow or shrink as you work. `append()` adds an item to the end, `insert()` places one at a chosen position, and `pop()` removes and returns an item.

```python
fruits.append("orange")        # Add to the end
numbers.insert(1, 15)          # Insert at index 1
removed = numbers.pop(2)       # Remove index 2
```

### Using list values in decisions
Looping over a list lets you check each value and react.

```python
temperatures = [23, 19, 25, 30]

for temp in temperatures:
    if temp > 25:
        print("High temperature alert")
    else:
        print("Temperature normal")
```

These techniques transfer directly to robot code: you can gather sensor samples in a list, inspect individual positions, and turn that decision into visible feedback.

## Assignment
Write a program that reads all eight Octoliner values into a list, evaluates the centre positions to decide whether the line is under the robot, mirrors that decision on both LEDs, and prints one heartbeat string in the format `LINE_LED:state=...;readings=[...]`. The assignment is complete when the `line_sensor_leds` verification_function receives your `LINE_LED:` line, confirms the LED state matches the list logic, and sees readings that support the decision.

## Conclusion
Nice work! You explored how lists organise ordered values and applied indexing to drive the robot's indicator lights. The next lesson keeps building list confidence while adding loops and PWM for smooth LED animation.
