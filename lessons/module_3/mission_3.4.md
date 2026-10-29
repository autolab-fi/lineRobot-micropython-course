---
index: 17
module: module_3
task: arrays_and_elif
previous: processing_sensor_data
next: led_feedback
---

# Mission 3.4 Arrays and Spatial Logic

**Completion:** Pass **Check in simulator** or **Verify on robot**.

Read the three zones independently. A wide line or a crossing can activate several zones at once; no zone has priority.

## Arrays and zone indices
`octoliner.analog_read_all()` returns a list of eight readings. Python list indices start at zero: `sensor_data[3]` selects the fourth reading. Viewed from above, sensors 5–7 are on the left, 3–4 in the center, and 0–2 on the right. For this exercise use one scout per zone: 6, 3, and 1 respectively.

## Boolean values and `elif`
A comparison such as `reading > threshold` produces `True` or `False`. `int(True)` is 1 and `int(False)` is 0, so adding the three converted results gives the number of active zones.

Use `if / elif / else` to distinguish zero, one, or multiple active zones. Exactly one of these cases applies to each scan.

## Assignment
1. Set sensitivity to **243** and `threshold = 800`. A reading detects the line only when it is **greater than** the threshold.
2. Repeat **5 times**: move forward **5 cm**, wait **0.5 seconds**, then call `octoliner.analog_read_all()` once and store the result in `sensor_data`.
3. Compare three readings with the threshold: **left = index 6**, **center = index 3**, **right = index 1**. Save each comparison as a Boolean.
4. Count the active zones. Use `if / elif / else` to print exactly one classification per scan:
   - zero: `No line`
   - one: `Line in one zone`
   - two or three: `Line in multiple zones`
5. Print the three Boolean states on the next line using `print("Left:", left, "Center:", center, "Right:", right)`. For example, if the left and center zones detect the line:
   ```text
   Line in multiple zones
   Left: True Center: True Right: False
   ```
6. After the loop, print `Survey complete.`.

The simulator compares each classification and each zone state with the actual readings. Reporting several active zones is correct; choosing only the center would discard information.

The physical robot starts at camera coordinates **(70, 50) cm**, facing right. The simulator uses its own aligned start on the virtual map.
