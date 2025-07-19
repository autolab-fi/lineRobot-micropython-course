### 3.**PID Controller**

### Objective

Understand how the derivative term adds predictive power to a control system. Learn how the PID controller combines all three terms (Proportional, Integral, Derivative) to give the best performance for a line-following robot.

### Theory

So far, we’ve seen how the proportional term reacts to present error and how the integral term accumulates past errors. But both of these only respond after an error happens. The derivative term predicts future behavior by measuring how fast the error is changing.

If the robot is correcting too aggressively, the derivative slows things down before it overshoots. This makes the system more stable and less wobbly.

## ![Pid](https://github.com/pranavk-2003/line-robot-curriculum/blob/assignments/images/module_8/pid_f.png?raw=True)

### The Full PID Formula

```
u(t) = Kp × error + Ki × sum_of_errors + Kd × rate_of_error_change
```

Where:

- `Kp` is the proportional gain
- `Ki` is the integral gain
- `Kd` is the derivative gain
- `error` is the difference between current and ideal position
- `sum_of_errors` is the cumulative total of all past errors
- `rate_of_error_change` is the difference between the current error and the previous error

Each term contributes:

| Term         | What it does                               |
| ------------ | ------------------------------------------ |
| Proportional | Fixes the current error                    |
| Integral     | Fixes small errors that build up over time |
| Derivative   | Predicts and dampens future errors         |

---

### Assignment – Implement the PID Controller

#### Step 1: Calculate Error and Derivative

```python
derivative = error - prev_error
prev_error = error
```

Here, `derivative` tells you how fast the error is changing. If it's changing quickly, the robot might be about to overshoot.

---

#### Step 2: Compute PID Output

```python
output = (Kp * error) + (Ki * integral) + (Kd * derivative)
```

You now combine the present error, the accumulated error, and the error trend into a single control output.

---

#### Step 3: Motor Speed Control

```python
left_speed = fwdspeed - 1.5 * output
right_speed = fwdspeed + 1.5 * output

robot.run_motors_speed(left_speed, right_speed)
```

This sets the robot's left and right motor speeds based on the total output of the PID controller.

---

### Conclusion

You now have a full understanding of PID control. This is the most powerful and widely used controller in robotics. By tuning the three constants — Kp, Ki, and Kd — you can get a balance of speed, accuracy, and stability.

The proportional term keeps the robot centered, the integral term eliminates slow drift, and the derivative term makes everything smoother by preventing overshoot. Together, they make your robot move confidently and cleanly along the line.
