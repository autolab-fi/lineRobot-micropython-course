# Lesson 4: Auto-Docking

## Lesson objective
Make the rover dock with the charging station and report the charging status.

## Introduction
After a long exploration mission, your rover needs to recharge. In this lesson, you will implement an auto-docking sequence that guides the robot backward to find its charging station. The robot will continuously monitor its charging status and stop when it successfully makes contact with the charging pads.

## Theory

### Understanding the charging detection system
Your robot is equipped with sensors that can measure battery voltage and charging current. When the robot makes contact with the charging pads, the charging current increases significantly, allowing the robot to detect successful docking.

### Measuring voltage and charging status
The `measure_adc` module provides functions to read the robot's battery voltage and charging level:

```python
from measure_adc import measure, measure_print

def report_status(source="USER"):
    voltage, charging = measure()
    print(f'{source}{{"voltage": {voltage:.2f}, "charging": {charging:.2f}}}')

report_status()
measure_print()
```

The **measure()** function returns two values:
- **voltage**: The current battery voltage in volts (V)
- **charging**: The charging current level (a value that increases significantly when charging)

When the robot is not connected to the charging station, the charging value is typically low (close to 0). When the robot successfully docks, the charging value increases to 10 or higher, indicating that power is flowing into the battery.

### The auto-docking algorithm
The auto-docking sequence follows these steps:

1. **Start moving backward** at a slow, controlled speed to approach the charging station gently
2. **Continuously monitor** the charging status while moving
3. **Detect charging contact** by checking if the charging value reaches the threshold (≥10)
4. **Stop immediately** when charging is detected
5. **Report final status** to confirm successful docking

The slow speed is important because it gives the sensors time to detect the charging pads and prevents the robot from crashing into the station.

### Checking conditions in a loop
You can use a **while** loop to continuously check the charging status:

```python
while True:
    voltage, charging = measure()
    
    if charging >= 10:
        # Charging detected!
        break
    
    time.sleep(0.3)  # Check every 0.3 seconds
```

This loop runs indefinitely until the charging condition is met. The **time.sleep(0.3)** adds a small delay between checks to avoid overwhelming the system with readings.

## Assignment
Write a program that implements an auto-docking sequence:

- Start the robot moving backward at a slow speed (around 20-30% speed)
- Continuously measure and print the voltage and charging values
- Stop the robot when the charging value reaches 10 or higher
- Print a confirmation message showing the final voltage and charging values

**Hints:**
- Use **robot.run_motors_speed()** with negative values to move backward
- You may need to adjust the motor speeds slightly if the robot doesn't move straight

## Conclusion
Congratulations! You've implemented an autonomous docking system that allows your robot to find and connect to its charging station. This capability is essential for long-term autonomous operations, as the robot can now return to recharge without human intervention. The combination of sensor monitoring and motor control demonstrates how robots make decisions based on real-time feedback from their environment.
