---
index: 19
module: module_3
task: simple_line_follower
previous: led_feedback
next: python_lists
---

# Mission 3.6 Simple Line Follower

## Objective
Guide the Artemis rover using `if/elif/else` and motor speeds to follow a short, nearly straight section of the line. This is your first relay controller: it chooses between driving straight, steering left and steering right.

Starting settings: `sensitivity = 243`, `threshold = 700`, `speed = 15`, `turn_speed = 3`.
Sensitivity configures the Octoliner (0–255); the threshold is compared with its readings.

## Three sensor zones
The starter code combines the eight readings into three zones. Facing forward, indices 5–7 are left, 3–4 are center and 0–2 are right. `max(a, b, c)` returns the largest reading: a zone detects the line when any of its sensors sees it. Keep these supplied expressions unchanged while implementing steering.

## Assignment
Complete the three marked steering branches in the starter code:

- Center sees the line: set both wheel speeds to `speed`.
- Left sees the line: slow the left wheel to `turn_speed`, keeping the right at `speed`.
- Right sees the line: keep the left wheel at `speed`, slowing the right to `turn_speed`.

Use the supplied `run_motors_speed()` call. Do not add angle turns: the loop should keep reading the sensor while steering. Pass the two checkpoints on the short section before the bend; the checker ends the run after both are reached.

The starter code also handles brief gaps in detection. It remembers the previous wheel speeds, then stops after 15 consecutive readings without a line. You do not need to implement this part. If it stops immediately, inspect the sensor readings and starting position rather than increasing the timeout.

## Starter code

```python
import machine
import time
from octoliner import Octoliner
from lineRobot import Robot

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(243)
robot = Robot()

threshold = 700
speed = 15
turn_speed = 3
left_speed = speed
right_speed = speed
lost_samples = 0
lost_limit = 15

while True:
    sensor_data = octoliner.analog_read_all()
    left_scout = max(sensor_data[5], sensor_data[6], sensor_data[7])
    center_scout = max(sensor_data[3], sensor_data[4])
    right_scout = max(sensor_data[0], sensor_data[1], sensor_data[2])

    if center_scout > threshold:
        left_speed, right_speed = 0, 0  # TODO: drive straight
        lost_samples = 0
    elif left_scout > threshold:
        left_speed, right_speed = 0, 0  # TODO: steer left
        lost_samples = 0
    elif right_scout > threshold:
        left_speed, right_speed = 0, 0  # TODO: steer right
        lost_samples = 0
    else:
        lost_samples += 1
        if lost_samples >= lost_limit:
            robot.stop()
            print("Line lost. Stop and check the starting position.")
            break

    robot.run_motors_speed(left_speed, right_speed)
    time.sleep(0.02)
```

## Next step
You have closed the control loop: the Artemis rover reads the ground and changes its steering without waiting for Mission Control. Later, `track_line()` will combine all eight sensor readings into a signed position estimate for more precise controllers.
