# Lesson 1 : Planetary Surface Mapping

## Lesson Objective
Program the robot to systematically explore and reveal a fog-covered terrain map by executing a repeatable movement pattern that uncovers at least 60% of the hidden surface.

## Introduction
Mission Control provides a partially obscured map—only areas the robot physically visits will be revealed. Your task is to write a sequence of movements that can be repeated to efficiently survey the landing zone, uncovering more than half the terrain without manually controlling each step.

## Theory

### Fog of War Exploration
In planetary exploration, robots often face limited sensor range or data transmission constraints. The "fog of war" concept means areas remain hidden until directly surveyed. Your robot must follow a systematic pattern to maximize map coverage with minimal backtracking.

### Movement Sequences
Rather than writing individual commands for each move, you'll create a reusable movement pattern. Think of it like a lawnmower pattern—moving forward in straight lines, then shifting over and repeating. The key is:
- **Consistency**: Each pass should cover equal distance
- **Overlap**: Slight overlap ensures no gaps in coverage

### Calculating Coverage
The verification system tracks what percentage of the map your robot reveals. Your goal is **60% minimum coverage** within the time limit. More efficient patterns mean higher coverage scores.

### Map Overview

Robot directions
![Starting Point](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_9/fog.png?raw=true)

## Assignment
Write a program that:

1. Moves the robot forward a fixed distance (one "pass" across the survey area)
2. Shifts position slightly to start the next parallel pass
3. Repeats this pattern multiple times using a loop
4. The movement sequence should be simple enough to repeat


**Example approach:**
```python
# Pseudocode - adapt to your strategy
for pass_number in range(number_of_passes):
    move_forward_distance(survey_distance)
    # Add turning logic here
    # Add positioning logic here
```

## Conclusion
You've programmed an autonomous exploration pattern that systematically reveals unknown terrain. This principle applies to real planetary rovers that must efficiently survey large areas with limited human intervention. By using loops and fixed movement sequences, you created a scalable solution that could map even larger territories.
