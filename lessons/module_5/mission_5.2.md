---
index: 28
module: module_5
task: upgraded_relay_controller
previous: concept_of_error
next: proportional_control
---

# Mission 5.2 Upgraded Relay Controller

## Objective
Learn how to use the sensor's auto-calibration feature and build an upgraded Relay (Bang-Bang) controller using the continuous Error variable and a `NaN` failsafe.

## Introduction
In Module 3, you built a Relay Controller by checking multiple individual sensors (Index 1, 3, 6) to decide whether to turn left or right. It worked, but the code was long and complex.

Now that we have the `track_line()` function, which gives us a single continuous Error value from `-1.0` to `1.0`, writing that same controller becomes incredibly simple. 

Before we jump into the advanced math of Proportional Control, we will use this Error value to rewrite our Bang-Bang logic. We will also let the robot automatically calibrate its own "eyes"!

## Theory

### 1. Auto-Calibration
In the past, we manually set the sensor's threshold using `octoliner.set_sensitivity(245)`. But lighting conditions change. The Octoliner library has a smart function called `optimize_sensitivity_on_black()`. 

If you place the robot over a black line and call this function once at the start of your program, it will automatically test different light levels and find the perfect sensitivity for the current room! It returns `True` if successful.

### 2. Thresholding the Error
Instead of asking "Does Sensor 1 see the line?", we now ask "Is the Error large enough?". 
We can create "zones" using simple math thresholds:
* If `position < -0.15`: The line is too far left. We need to steer left.
* If `position > 0.15`: The line is too far right. We need to steer right.
* `else`: The line is somewhere near the center (`0.0`). Drive straight!

### 3. The `NaN` Failsafe
If the robot is lifted into the air or completely loses the track on a blank surface, `track_line()` will return a special value called `NaN` (Not a Number). 

To detect this, we use the `math.isnan(position)` function. It asks the computer a simple question: *"Is this variable Not a Number?"* and returns a Boolean (`True` or `False`). If it returns `True`, it means our sensor is completely blind.

**But wait, do we need this on our lunar map?**
You might notice that even when the rover drives off the black line, it rarely triggers a `NaN` error. Why? Because the lunar surface map is filled with dark craters and shadows. The infrared sensors see a dark crater and get confused, interpreting it as the edge of the line (returning a valid number like `1.0` instead of `NaN`).

**So why do we still check for it?** Because of **Robust Engineering**. 
What if the rover is moved to a clean, white test track tomorrow? What if an I2C wire momentarily disconnects and the sensor sends blank data? 

If a `NaN` value ever accidentally slips into your motor speed calculations (e.g., `speed + NaN`), the entire Python program will instantly crash, and the robot will require a hard reboot. Catching `NaN` is a mandatory "safety net" in professional robotics. Even if you don't expect to fall, you always wear a parachute!

**Requirements:**
1. **Auto-Calibration:** Use `octoliner.optimize_sensitivity_on_black()` in an `if` statement. If it succeeds, print a success message. If it fails, print a warning.
2. **The Tracking Loop:** Create a `while True:` loop. Inside the loop:
   * Read the `track_line()` position.
   * **Failsafe Check:** First, check `if math.isnan(position):`. If True, stop the motors, print an error, and `break` the loop.
   * **Steering Logic:** If the position is valid (`else:`), use an `if / elif / else` block to check the `position` variable. 
     * If `< -0.3`: Turn Left (e.g., Left: `5`, Right: `25`)
     * If `> 0.3`: Turn Right (e.g., Left: `25`, Right: `5`)
     * Otherwise: Drive Straight 
Watch how much cleaner your steering logic has become.

## Conclusion
Mission accomplished! You have successfully modernized your autonomous control system.

By using auto-calibration, your rover is now adaptable to new environments. By using the Error value for steering, you reduced a massive block of sensor checks into just three clean lines of logic. And with the `NaN` failsafe, your software is protected from crashes.

However, the rover still wobbles because it uses hard turns. In the next mission, we will finally use the Error value to calculate exactly *how hard* the robot needs to turn. Get ready for the Proportional Controller!