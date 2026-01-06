# Lesson 3: Coordinate Navigation Log

## Lesson objective
Interpret a target coordinate on a mapped grid, drive the robot to that point, confirm arrival, and publish a navigation log that includes the mineral found in Lesson 2.

## Introduction
Mission Control now transmits exact `(x, y)` coordinates on the exploration map. Your rover must read the grid, plot a route, and verify when it reaches the destination. When you arrive, you will report both the final position and the mineral the scanner detected earlier.

## Theory

### Drawing and reading the coordinate grid
Overlay an OpenCV grid with labelled axes on the map to make the coordinate frame clear. Mark both the starting pose and the target so you can visualise the route.

### Planning and executing the drive
Reuse helpers from the fog-of-war sweep to move along straight lines or short turns until the robot is within a tolerance radius of the target coordinate. Keep the motion repeatable so the arrival check is reliable.

### Confirming arrival and logging results
Compare the robot’s pose to the target point after each movement burst. When the error falls below your tolerance, stop the robot and print or publish a structured navigation log that includes the mineral type saved from Lesson 2.

### Loading the grid asset
A background grid is available to support your overlay:

```python
GRID_PATH = "images/module_9/coordinate_grid.png"
# Display this in your dashboard or mix it with your plotted poses.
```

## Assignment
Write a program that:

- Loads the coordinate grid image so you can align your overlay and target marker.
- Accepts a target `(x, y)` coordinate, marks it on the grid, and plots the robot’s current pose.
- Drives toward the target using simple straight segments and turns until the pose is within your chosen tolerance.
- Stops and prints a navigation log that includes the final pose and the mineral detected during the scanner sweep in Lesson 2.

## Conclusion
By translating coordinates into motion, confirming arrival, and reporting mission data, you closed the loop between mapping, scanning, and navigation. This workflow prepares your rover for more complex multi-step missions.
