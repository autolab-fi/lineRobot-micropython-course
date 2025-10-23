### 2. **Proportional (P) Controller**

The P controller improves on relay by making the output proportional to how far off the robot is from the center of the line.

**Formula:**

```
u(t) = Kp × error
```

Where:

- `u(t)` is the control output,
- `Kp` is the proportional gain (a tuning constant),
- `error` is the difference between the current position and the desired position (usually 3.5 for 8 sensors).

The farther the robot is from the line center, the stronger the correction. This makes the movement smoother and more precise.

![P](https://github.com/pranavk-2003/line-robot-curriculum/blob/assignments/images/module_8/p.png?raw=True)

**Limitations:**

- Can't completely eliminate steady-state error.
- High gain may cause overshoot or oscillation.

---

### 3. **Proportional-Integral (PI) Controller**

The PI controller fixes the steady-state error left behind by the P controller.

It adds an integral term, which keeps track of accumulated past errors. If the robot is slightly off for a long time, the integral slowly increases to push it back to the center.

**Formula:**

```
u(t) = Kp × error + Ki × sum_of_errors
```

Where:

- `Kp` is the proportional gain,
- `Ki` is the integral gain,
- `sum_of_errors` is the running total of all previous errors.

## ![Pi](https://github.com/pranavk-2003/line-robot-curriculum/blob/assignments/images/module_8/pi.png?raw=True)

## Assignment – Implement a PI Controller

### Step 1: Calculate Weighted Sum and Total Value

```python
weighted_sum = 0
total_value = 0

for i in range(8):
    if sensorvalues[i] > MY_BLACK_THRESHOLD:
        weighted_sum += i * sensorvalues[i]
        total_value += sensorvalues[i]
```

### Step 2: Calculate Position and Error

```python
error = 0
if total_value > 0:
    position = weighted_sum / total_value
    error = position - 3.5  # 3.5 is the center of an 8-sensor array
```

### Step 3: Compute Control Output (PI logic)

```python
integral += error
integral = max(min(integral, 30), -30)  # limit the integral to avoid windup

output = (Kp * error) + (Ki * integral)
```

### Step 4: Set Motor Speeds

```python
left_speed = fwdspeed - 1.5 * output
right_speed = fwdspeed + 1.5 * output

robot.run_motors_speed(left_speed, right_speed)
```

---

### Summary

| Controller | Formula                             | Strength                              | Weakness                       |
| ---------- | ----------------------------------- | ------------------------------------- | ------------------------------ |
| Relay      | full left/right based on error sign | Simple and fast                       | Rough, unstable, zigzag motion |
| P          | u = Kp × error                      | Smooth control                        | Small steady-state error       |
| PI         | u = Kp × error + Ki × ∑error        | Smooth and accurate, eliminates error | Slower response, needs tuning  |

---

### Conclusion

In this lesson, we explored three control strategies for keeping a line-following robot centered: Relay, P, and PI. The relay controller is simple but leads to unstable movement. The P controller improves this by making adjustments based on how far off the robot is, but still can't fully correct long-term drift. The PI controller solves this by remembering past errors and slowly pushing the robot back on track.

Each method builds on the last, making the robot smarter and more stable. As we go forward, we’ll explore the PID controller, which adds one final component — the derivative — to further improve control and reduce overshoot.
