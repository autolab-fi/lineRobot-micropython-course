---
index: 2
module: module_1
task: test_drive
previous: welcome
next: license_to_drive
---

# Mission 1.2. Test drive

## Objective

Understand the concept of a "Robot Object" and execute your first movement code.

## Introduction

In this lesson, you will initiate the robot's movement. But before we push the button, we need to understand *who* receives our commands.

Behold the mighty rover who will assist you in learning:

![Picture of the robot](../../images/module-1/robot.jpg)


## Theory: The Digital Twin

Computers don't know what a "rover" is until we tell them. In Python, we create a specific software representation of our hardware.

Look at this line of code:
```python
robot = Robot()
```

Here is what happens:
1. **`Robot()`** refers to the **Class** (the blueprint or instructions on how to build a robot).
2. **`robot`** is the **Object** (the specific robot we just created).

Think of it this way: `Robot()` is the factory, and `robot` is the specific machine that rolled off the assembly line. We will send all our commands to this `robot`.

## Instructions

Now, let's bring this object to life.

1. Copy the code provided below and paste it into the code editor.

```python
from lineRobot import Robot

robot = Robot()

robot.move_forward_seconds(3)
```

2. Upload the program to the robot.
3. Observe the program execution results in the output and on the video feed.

## Conclusion

Wasn't hard, was it? A tiny code though a giant leap towards building your robotics skillset. You have successfully acquired the skill to make the robot move. Now, you can proceed to the next lesson!
