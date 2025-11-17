# Lesson 2: Mineral Scanner Sweep

## Lesson objective
Reach a target waypoint, activate a spinning mineral scanner visualised with LEDs and an OpenCV cone, and log any mineral signatures detected during the sweep.

## Introduction
The rover has landed near a promising rock cluster. Before digging in, it must travel to a waypoint, deploy a scanner, and rotate on the spot to detect mineral signatures. LEDs mirror the scanner state while an OpenCV wedge shows the detection cone. Any mineral hit must be recorded for later reporting.

## Theory

### Coordinating movement and scanner state
Break the mission into clear phases: drive to the waypoint, stop, switch the LEDs to a scanning colour, then rotate in place. Keeping phases separate makes the timing and logging predictable.

### Visualising the detection cone
Represent the scanner as a wedge drawn in OpenCV and aligned to the robot heading. Update the cone angle as the robot rotates so you can see where the scanner is “looking.”

### Detecting and storing mineral hits
Define bearing ranges that map to mineral types (iron, ice, crystal, etc.). When the cone crosses a range, record the mineral name in a list or variable so Lesson 3 can reuse it.

### Loading the overlay asset
An optional overlay is available to illustrate the scanner cone:

```python
OVERLAY_PATH = "images/module_9/scanner_overlay.png"
# Load or display this overlay in your dashboard while the scanner spins.
```

## Assignment
Write a program that:

- Drives the robot to the assigned waypoint and halts before starting the scan.
- Sets the LEDs to a “scanner active” colour/brightness that stays on during the sweep.
- Rotates the robot 360° while updating an OpenCV cone overlay aligned with the current heading.
- Logs any mineral types detected when the cone passes their bearing ranges and prints a summary at the end of the spin.
- Saves the detected mineral type for use in Lesson 3.

## Conclusion
You combined waypoint navigation with a rotating scan, linked LED states to visual feedback, and captured mineral data for later missions. These skills are the basis for autonomous surveys that blend motion control with sensor logging.
