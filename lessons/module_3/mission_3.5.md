---
index: 18
module: module_3
task: led_feedback
previous: arrays_and_elif
next: simple_line_follower
---

# Mission 3.5 Visual Telemetry (LEDs)

**Completion:** Pass **Check in simulator** or **Verify on robot**.

Extend your scanner from **3.4** with a light that signals detection of the marked line in **any zone**.

## GPIO and functions
Configure the onboard LED with `machine.Pin(15, machine.Pin.OUT)`. Its `.on()` and `.off()` methods switch it on and off. Put one on/off cycle in a function so you can call it after a scan.

## Assignment
1. Keep the complete scanner from 3.4: sensitivity **243**, threshold **800**, **5 steps of 5 cm**, **0.5 seconds** settling time, zone classifications, Boolean state reports, and the final `Survey complete.` message.
2. Configure **pin 15** as an output.
3. Define a function `blinkLED()` that turns the LED on, waits **0.2 seconds**, turns it off, and waits **0.2 seconds**.
4. After each scan, call the function **once if at least one zone detects the line**. Use `left or center or right` to express this condition.
5. If no zone detects the line, do not blink. If two or three zones detect it, still blink only once.

The simulator checks that each detected scan has one complete LED pulse and each empty scan has none. Keep the LED off between scans and at the end.

The physical robot starts at camera coordinates **(70, 50) cm**, facing right. The simulator uses its own aligned start on the virtual map.
