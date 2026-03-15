---
index: 22
module: module_4
task: telemetry
previous: python_lists
next: color_sensor_basics
---

# Mission 4.2 Telemetry 

## Objective
Learn how to track real-world execution time, perform mathematical operations to calculate the robot's actual speed, and construct structured telemetry reports using Python f-strings.

## Introduction
Welcome back to Mission Control! While your rover executes its routes, it must constantly report its status and sensor data back to the base—a process known as **telemetry**.

In previous modules, you printed basic messages by separating text and variables with commas, like `print("Total distance:", total)`. While this is fine for simple reading, it automatically inserts unwanted spaces and quickly becomes a confusing mess of quotation marks when you try to format multiple variables like `print("name=", name, ";dist=", dist)`. 

Automated dashboards require data to be sent in an exact, strict format to parse it correctly. Today, you will learn a much cleaner Python tool to construct these complex messages. Furthermore, instead of just broadcasting static numbers, you will generate real physical telemetry by using a digital stopwatch to calculate the rover's actual speed!

## Theory

### 1. Reviewing and Expanding Data Types
In Module 1, you learned how to store integers (`int`) and decimals (`float`) in variables. To build a complete telemetry report, we need to introduce two more types:
* **`str` (String):** Stores text. Used for names and string identifiers (e.g., `robot_name = "LunarRover-1"`).
* **`bool` (Boolean):** You used Booleans (`True`/`False`) when working with sensor logic. Now, we will store them directly in variables to act as status flags (e.g., `is_ready = True`).

### 2. Measuring Time and Calculating Speed
You already know how to perform basic math in Python. Today, we will use division (`/`) to calculate the rover's actual speed based on real physical time.
To calculate speed, we need a digital stopwatch. The `time` library has a function called `time.time()` that returns the current time in seconds.

```python
import time

start_time = time.time()       # Start the stopwatch
# ... robot moves here ...
end_time = time.time()         # Stop the stopwatch

duration = end_time - start_time
```

Python uses `/` for true division. Note that this operation always results in a `float` (a decimal number), which is perfect for precise physics calculations.

### 3. Building Telemetry Strings (f-strings)
To send all this data to the dashboard, we need to combine text and variables into one single string. The modern and cleanest way to do this in Python is using **formatted string literals**, or **f-strings**.

By placing the letter `f` directly before the opening quotation mark, you tell Python to evaluate any variables placed inside curly braces `{}` and inject their values directly into the text.

```python
name = "Alex"
age = 18

# Without f-strings, this is messy. With f-strings, it's clean:
print(f"Name={name};Age={age}")
```

## Assignment
Your task is to conduct a speed test. You will command the rover to drive a specific distance, measure how long the physical movement takes, calculate its speed, and broadcast the results.

**Requirements:**
1. Command the rover to drive forward by **40 cm**.
2. Use the `time.time()` function to measure the exact `duration` of the movement.
3. Calculate the rover's real-world speed (`speed_cm_s`). *Hint*: Remember from physics that Distance = Speed * Time.
4. Declare two additional variables for the report: a string `robot_name` (e.g., "Artemis-1") and a boolean `is_ready` (set to `True`).
5. Output the results using a single `print()` call with an **f-string**. The output must strictly match this format:
  `STATUS:name=<your_robot_name>;dist=<your_distance>;time=<your_duration>;speed=<your_speed>;ready=<is_ready_status>`


## Conclusion
Excellent work! You have successfully utilized a data structure to store and execute a complex navigation plan.
Using lists makes your code significantly cleaner and highly scalable!