---
index: 7
module: module_1
task: sequential_navigation
previous: maneuvering
next: electric_motors
---

# Mission 2.7 Sequential navigation

## Objective

Create a complex route visiting multiple waypoints and learn how to document your code using comments.

## Introduction

You have mastered the controls: moving, turning, and using variables. Now, you are ready for your first real navigation.

A real mission is never just "drive forward." It involves a sequence of actions: "Go to the crater, turn left, approach the solar panel, turn right..." As your programs get longer, they can become hard to read. In this mission, we will learn how to organize long code and navigate a complex route.

## Theory

### 1. Sequential Execution
Throughout the preceding lessons, you've been creating programs. Let's define what a program is: a program is an ordered sequence of commands. These commands are executed by a designated executor, which, in our case, is the robot.
The robot reads your code from **top to bottom**, line by line. It will not start the next command until the previous one is finished.

This means the **order** of your commands is critical. If you swap a "Turn" and a "Move," the robot will end up in a completely different place!

### 2. Comments (The "Mission Logs")
When writing long programs, it is easy to forget what a specific block of code does. To help yourself (and other engineers), you can use **Comments**.

A comment is a line of text that the computer **ignores**. It is meant only for humans. In Python, we create a comment using the hash symbol (`#`).

```python
# This is a comment. The robot ignores it.
robot.move_forward_distance(20) # You can also write comments here
```

**Why use comments?**
* **Organization:** Separate your code into logical blocks (e.g., `# Section 1: Leaving Base`).
* **Debugging:** Quickly disable a line of code without deleting it.

## Assignment

You need to navigate the robot through a specific route to collect geological samples (minerals) at **4 waypoints**. You must use **comments** to label each section of the journey.
    * Example: `# Moving to Point 1`, `# Collecting Sample 2`, `# Returning to base`.

![trajectory](https://github.com/autolab-fi/lineRobot-micropython-course/blob/main/images/module-1/trajectory.png?raw=true)

You can refresh your memory of the library functions by revisiting the previous lessons.

**Hint:** Break the path down into small steps. Write code for the first leg, run it, test it, and then add the next leg.

## Conclusion

Mission accomplished! You have successfully programmed a multi-step autonomous route and learned to keep your code clean with comments.

You have completed the Basic Training! Next up is the **Weekly Challenge**, where you will put everything you've learned to the ultimate test.
