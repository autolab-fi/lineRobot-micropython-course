---
index: 17
module: module_3
task: arrays_and_elif
previous: processing_sensor_data
next: led_feedback_system
---

# Mission 3.4 Arrays and Spatial Logic

## Objective
Learn how to read all 8 sensors at once using arrays, extract specific data using indices, and use `elif` statements to determine the line's position.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
Until now, you have been reading a single sensor using `analog_read(index)`. But to follow a path, the rover needs full spatial awareness to know if the line is drifting to the left or to the right.

Today, you will learn how to capture a complete snapshot of the ground using an "array" of data, and how to make complex decisions using a new programming tool: the `elif` statement.

## Theory

### 1. Arrays and Indices
Instead of reading 8 sensors one by one, we can read them all simultaneously using `octoliner.analog_read_all()`. This command returns an **array** (a list) containing 8 numbers.

In Python, an array is enclosed in square brackets `[]`. Every item inside has an **index** (its position), starting from exactly `0`.


```python
#          [Sens0, Sens1, Sens2, Sens3, Sens4, Sens5, Sens6, Sens7]
data_array = [245,   240,   210,    85,    90,   240,   245,   250]

# You can extract a specific number by putting its index in brackets:
center_value = data_array[3] # This extracts '85'
```

### 2. IR Sensor Configuration

The Octoliner sensor array consists of 8 sensors, each providing an analog value that indicates the intensity of reflected IR light.

![IR Sensor Logic](https://github.com/pranavk-2003/line-robot-curriculum/blob/assignments/images/module_7/IR_sensor_array.png?raw=True)

- **Central sensors (3 & 4)** → Move straight
- **Left sensors (0,1,2)** → Guide right turns
- **Right sensors (5,6,7)** → Guide left turns

To check an entire zone, we would normally need to check all three of its sensors. However, to keep our very first navigation program simple, we will pick just **one specific sensor from each zone** to act as our primary "scout":
* **Left Scout:** Index 1
* **Center Scout:** Index 3
* **Right Scout:** Index 6

### 3. The `elif` Statement
To check multiple conditions in a specific order, we use the `elif` (Else If) statement. 

Python checks conditions from top to bottom. As soon as it finds a `True` condition, it executes that specific block and **skips the rest**. Here is an example of how this structure looks when checking different collision sensors (do not copy this for your assignment!):

```python
if front_radar < safe_distance:
    print("Obstacle ahead! Stop!")
elif back_radar < safe_distance:
    print("Obstacle behind! Stop!")
elif side_radar < safe_distance:
    print("Obstacle on the side!")
else:
    print("All clear. Proceed.")
```

## Assignment
Mission Control needs to map a long, dark basaltic mineral vein on the lunar surface. Write a geological survey program that performs a step-by-step scan of the ground. The rover must make 5 stops (moving 5 cm at a time) and report the exact position of the mineral vein at each stop.

**Requirements:**
1. **Setup:** The hardware is initialized in the template. Define a `threshold` variable. 
2. **Scanning Cycle:** Create a loop.
3. **Action:** Inside the loop, first move the rover forward and add a delay to let the instruments settle.
4. **Read Data:** 
    * Read all 8 sensors at once and save the result to a variable named `sensor_data`.
    * Extract the values for index `1`, index `3`, and index `6` from `sensor_data` and save them into three separate variables (e.g., `left_scout`).
5. **Analyze & Report:** * Use an `if / elif / else` structure to check your variables.
    * Print `"Vein: Center"`, `"Vein: Left"`, `"Vein: Right"`, or `"No minerals"` accordingly.
6. **Shutdown:** After the loop finishes, print `"Survey complete."`

## Conclusion
Brilliant work! You have successfully learned how to process arrays, extract specific data points by their index, and control the rover in discrete, scientific steps. By combining this with `elif` statements, you have built the foundational "brain" of an autonomous tracking system. 

> **Important:** Save your code or keep this tab open! You will use this exact scanning loop as the foundation for your next mission.

Right now, Mission Control has to read text in the terminal to know where the mineral vein is. In the next mission, we will learn how to use the rover's GPIO pins to turn on physical warning LEDs when the rover loses the trail!
