---
index: 20
module: module_3
task: logical_operators
previous: simple_line_follower
next: python_lists
---

# Mission 3.7 Upgrading Vision (Logical Operators)

## Objective
Learn how to use `or` and `and` logical operators to combine multiple conditions, eliminating blind spots and detecting complex track features like intersections.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
In the previous mission, your rover successfully drove itself! However, relying on only three "scout" sensors has a major flaw: **blind spots**. If the track has a sharp turn, the line might slip between the scouts, causing the rover to lose the path. 

Furthermore, Mission Control needs the rover to automatically stop when it reaches an **intersection** (a horizontal line crossing the track). Today, we will upgrade the rover's "brain" using logical operators so it can process complex patterns!

## Theory

### 1. The `or` Operator (Fixing Blind Spots)
The `or` operator checks if **at least one** condition is True. We will use it to group our 8 sensors into solid zones. If *any* sensor in a zone sees the line, the rover will react:
* **Center Zone:** Sensor 3 `or` Sensor 4
* **Left Zone:** Sensor 0 `or` Sensor 1 `or` Sensor 2
* **Right Zone:** Sensor 5 `or` Sensor 6 `or` Sensor 7

```python
# Example of the new Center Zone logic:
if sensor_data[3] > threshold or sensor_data[4] > threshold:
    robot.run_motors_speed(speed, speed)
```

### 2. The `and` Operator (Detecting Intersections)
The `and` operator requires ALL conditions to be True.
If the rover is driving over a standard line, only the center sensors see black. But if it hits a perpendicular intersection line, both the far-left sensor (Index 0) AND the far-right sensor (Index 7) will see black at the exact same time!

```python
# Example of an intersection check:
if sensor_data[0] > threshold and sensor_data[7] > threshold:
    print("Intersection reached!")
```

## Assignment

Upgrade your autonomous line-following algorithm. Use `or` to create robust steering zones.

## Conclusion
Module 3 complete! Outstanding work!

By applying the or and and operators, you have created a highly reliable Relay Controller. It can handle sharp turns without blind spots and even recognizes complex track markings like intersections.

You have officially mastered the fundamentals of autonomous robotics. Take a moment to watch your rover conquer the track and stop perfectly at the crossroad. Get ready for Module 4!
