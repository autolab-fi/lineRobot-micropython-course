---
index: 32
module: module_6
task: art_of_debugging
previous: adaptive_speed
next: hardware_safety_net
---

# Mission 6.1 The Art of Debugging

## Objective
Understand the difference between syntax and logic errors, and master the "Print Debugging" technique to find hidden problems in the robot's logic.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
Welcome to Module 6!

Up to this point, you have written increasingly complex algorithms, from simple turns to P-controllers and color normalization. But in real-world robotics, writing the code is only half the battle. The other half is making it work correctly.

Errors (or "bugs") are inevitable. Even NASA engineers write bugs. True professionalism is not about writing flawless code on the first try, but knowing how to quickly find and fix the issues. Today, we begin mastering the art of debugging.

## Theory

### 1. Two Types of Errors
In programming, you will face two main enemies:
* **Syntax Errors:** These are typos. You forgot a colon after an `if` statement, missed a parenthesis, or typed `prnt()` instead of `print()`. Python will immediately stop the program and point out the exact line where you made the mistake. These are the easiest to fix.
* **Logic Errors:** This is a roboticist's nightmare. The code is written perfectly, and there are no red error messages. However, instead of driving forward, the robot spins in place or crashes into a wall. The problem isn't in the grammar of the language, but in the *logic* of your instructions.

### 2. Reading the Robot MQTT Log
Look closely at your **Robot MQTT Log** in the terminal. You will see a `Traceback` telling you exactly which line caused the crash:
```text
11:18:53: Traceback (most recent call last):
11:18:53:   File "<string>", line 19
11:18:53: SyntaxError: invalid syntax
11:18:53: MPY: soft reboot
```

### 3. Print Debugging
How do you find a logic error if the computer is completely silent? You must force it to talk.

The golden rule of debugging is: **Never guess. Verify.**
If the robot turns the wrong way, do not just randomly change numbers in your code. Instead, output the variables to the terminal using the `print()` function to see what the robot is *actually* thinking at that exact moment.

**A Real-World Example:**
Imagine the robot is supposed to drive straight but keeps veering left.

```python
base_speed = 30
correction = 10

# It looks correct, but let's add a print statement!
left_motor = base_speed - correction
right_motor = base_speed + correction

print(f"DEBUG: Left={left_motor}, Right={right_motor}")
robot.run_motors_speed(left_motor, right_motor)
```

*Terminal Output:* `DEBUG: Left=20, Right=40`.

By looking at the output, you immediately see the problem: the right motor is spinning faster than the left, causing the robot to turn left. To make it go right, you need to swap the addition and subtraction signs.

## Assignment
Today, you are stepping into the shoes of a Senior QA (Quality Assurance) Engineer. A junior developer has submitted a Proportional Controller script, but it is a complete mess. 

The provided code contains a chain of **6 distinct bugs (3 Syntax/Runtime + 3 Logic)**. You must use your knowledge of the MQTT Log and Print Debugging to fix them one by one.

**Your Bug Hunt Checklist:**
1. **The Syntax Crash:** Look at the MQTT Log for a `SyntaxError` and inspect the main loop structure.
2. **The Typo Crash:** The Traceback indicates an unrecognized name. Locate and fix the typo.
3. **The Fake Emergency:** The failsafe triggers instantly. Review the threshold condition for logical accuracy.
4. **The Attribute Crash:** The Traceback points to a method that does not exist. Verify the spelling of the hardware commands.
5. **The Drunken Sailor:** The Proportional power (`P`) is miscalculated. Use `print()` to inspect the math.
6. **The Blocked Steering:** The robot accelerates instead of turning. Print `left_speed` and `right_speed` to find the flaw in the differential steering.

Find all 6 bugs, fix them, and watch the rover successfully navigate the track!

## Conclusion
Outstanding work, Senior Engineer! You have successfully hunted down a complex combination of grammar, spelling, and physics bugs.

You learned that debugging is a step-by-step process: first, you fix the crashes by reading the Traceback in the MQTT log, and then you fix the behavior by using `print()` to peek inside the robot's brain.