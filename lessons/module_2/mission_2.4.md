---
index: 4
module: module_2
task: for_loops
previous: defining_functions
next: encoder_theory
---
# Mission 2.4 For Loops & Patterns

## Objective
Learn how to use **for** loops to create complex movement patterns by using the loop counter variable.

## Introduction
In the last mission, you created a function. You could call that function 4 times to drive in a square. But what if you need to repeat an action 100 times? Or what if you want each movement to be slightly faster or longer than the previous one?

This is where **For Loops** shine. They don't just repeat code; they provide a **counter**—a variable that updates itself automatically on every "lap" of the loop.

## Theory

### 1. Why Loops are Better than Repeated Calls
If you want to repeat a command, you could just copy-paste it. But:
* **Scalability:** If you need to repeat something 100 times, a loop takes 2 lines, while copy-pasting takes 100.
* **Flexibility:** Loops give you a "counter" variable (usually called `i`) that changes its value in every iteration.

### 2. How the "For" Loop Works
A `for` loop follows a specific structure in Python: `for variable in sequence:`. 

* **The Variable (`i`):** Think of `i` as a temporary "container." In every "lap" (iteration), Python takes the next number from your sequence and puts it into this container.
* **The `range()` function:** This is what creates the list of numbers. By default, `range(5)` creates the sequence: `0, 1, 2, 3, 4`. 
* **The Body (Indentation):** Python uses indentation to know which commands belong to the loop. When the code reaches the last indented line, it jumps back to the top, updates `i` with the next number, and starts again.

**Example of the counter in action:**
```python
# This loop will run 3 times
for i in range(3):
    print("Starting lap number:", i)
    # Lap 1: i = 0
    # Lap 2: i = 1
    # Lap 3: i = 2
```
### 3. Advanced Range Control
You can give `range()` more instructions to control exactly how the counter `i` behaves:

* **`range(stop)`**: Starts at 0, ends before the stop value.
* **`range(start, stop)`**: Starts at a specific number. Example: `range(10, 13)` gives 10, 11, and 12.
* **`range(start, stop, step)`**: Changes how much `i` increases each time. Example: `range(0, 10, 2)` gives 0, 2, 4, 6, and 8.

### 4. Dynamic Behavior (Acceleration Example)
Imagine we want the robot to slowly speed up. We can use `i` to increase the power on every step:

```python
import time

for i in range(10):
    # Speed will grow: 10, 20, 30... 100
    current_speed = (i + 1) * 10
    robot.run_motors_speed(current_speed, current_speed)
    time.sleep(0.5)

robot.stop()
```

Here, we wrote the command once, but because of `i`, the robot behaves differently every time the loop runs.

## Assignment
Your rover has been assigned to scan a landing site by driving in a **Square Spiral**. You must start from a large square and slowly "wind" inward toward the center.

## Assignment: The Spiral Scan
Your rover must scan the landing zone by driving in a **Square Spiral**. You will start with a wide perimeter and "wind" inward toward the center.

**Requirements:**
* **Initial Distance:** Start with a side length of **60 cm**.
* **Step:** Decrease the distance by **5 cm** on every turn.
* **Repetition:** Use a `for` loop to perform exactly **10 turns**.
* **The Pattern:** Your distances should follow this sequence: 60, 55, 50, 45...
* **Navigation:** Use `move_forward_distance()` and `turn_right_angle(90)`.

**Hint:** Think about how the variable `i` grows (0, 1, 2...). You can use a mathematical formula involving `i` or overwrite your distance variable inside the loop. Both ways work!


## Conclusion
Excellent! You have moved from basic sequences to **algorithmic movement**. By using the loop counter, you can create any geometric pattern with just a few lines of code. Next, we will learn how to make the robot even smarter by using sensors called **Encoders** to measure distance based on actual wheel rotations!