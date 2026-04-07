---
index: 28
module: module_5
task: upgraded_relay_controller
previous: concept_of_error
next: proportional_control
---

# Mission 5.2 Upgraded Relay Controller

## Objective
Learn how to build an upgraded Relay (Bang-Bang) controller using the continuous Error variable, and implement a robust Failsafe using raw analog data.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
In Module 3, you built a Relay Controller by checking multiple individual sensors (Index 1, 3, 6) to decide whether to turn left or right. It worked, but the code was long and complex.

Now that we have the `track_line()` function, which gives us a single continuous Error value from `-1.0` to `1.0`, writing that same controller becomes incredibly simple. 

Before we jump into the advanced math of Proportional Control, we will use this Error value to rewrite our Bang-Bang logic. We will also build a safety net to prevent the robot from driving blindly if it loses the track!

## Theory

### 1. The "Memory" Feature of `track_line()`
The `track_line()` function has a feature: **Memory**. 
If the rover takes a corner too fast and the line completely disappears from all sensors, `track_line()` doesn't just output `0.0`. It remembers the *last known position* (e.g., `1.0` if it drove off to the right) and continues to return that value. 

This prevents the robot from suddenly stopping or jerking, but it creates a new problem: if the robot is lifted into the air or completely loses the track, it will blindly spin in circles forever, thinking the line is still there!

### 2. The Failsafe & the `max()` Function
To prevent blind driving, we need a Failsafe. We cannot trust `track_line()` if the robot is completely off the track. Instead, we must look at the raw analog data. 

You already know how to read the raw light levels of all 8 sensors:
```python
sensor_array = octoliner.analog_read_all()
```
This gives us a list of 8 numbers (from `0` to `1023`). But how do we quickly check if any of these sensors see the black line?

We can use Python's built-in `max()` function! It looks through a list and finds the highest number:

```python
# If the list is [100, 150, 800, 120, 90]
highest_value = max(sensor_array) # Returns 800
```

If the highest value in our sensor array is less than 700, it means even the "darkest" spot the sensor sees is still too bright. The robot is completely blind! We must trigger an Emergency Stop.

### 3. Thresholding the Error
Instead of asking "Does Sensor 1 see the line?", we now ask "Is the Error large enough?". 
We can create "zones" using simple math thresholds:
* If `position < -0.15`: The line is too far left. We need to steer left.
* If `position > 0.15`: The line is too far right. We need to steer right.
* `else`: The line is somewhere near the center (`0.0`). Drive straight!

## Assignment
You will write an upgraded autonomous line-following program. The rover must use raw analog data to catch tracking errors and steer itself using the new Error thresholds.

**Requirements:**
1. **Setup:** Make sure your sensitivity is set manually using `octoliner.set_sensitivity()`.
2. **The Tracking Loop:** Create a `while True:` loop. Inside the loop:
   * Read the raw data with `octoliner.analog_read_all()`
   * Read the position
3. **Failsafe Check:** First, check `if max(sensor_array) < 700:`. If True, print a critical error message, stop the motors, and `break` the loop.
4. **Steering Logic:** If the line is successfully detected (`else:`), use an `if / elif / else` block to check the `position` variable:
   * If `< -0.3`: Turn Left (e.g., Left: `5`, Right: `25`)
   * If `> 0.3`: Turn Right (e.g., Left: `25`, Right: `5`)
   * Otherwise: Drive Straight (e.g., `20`, `20`)

Watch how much cleaner your steering logic has become!

## Conclusion
Mission accomplished! You have successfully modernized your autonomous control system.

By using the raw analog data for your failsafe, your software is protected from driving blindly in circles. By using the Error value for steering, you reduced a massive block of individual sensor checks into just three clean lines of logic. 

However, the rover still wobbles because it uses hard, fixed-speed turns. In the next mission, we will finally use the Error value to calculate exactly *how hard* the robot needs to turn. Get ready for the Proportional Controller!