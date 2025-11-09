# Lesson 2: Analog LED Fade with Loops

## Lesson objective
Strengthen list and loop skills by designing a PWM brightness profile, iterating through it with `for` loops, and coordinating LED output with logged telemetry.

## Introduction
Smooth LED effects rely on repeating patterns. This lesson demonstrates how lists can hold a planned series of brightness levels, how loops step through each value, and how PWM commands translate the numbers into gradual light changes that you can record for verification.

## Theory

### Understanding PWM brightness
PWM rapidly switches the LED on and off. Higher duty cycles keep the LED on for a larger fraction of each cycle, making it appear brighter. The dashboard exposes `robot.set_led_pwm(channel, duty_cycle)` with values from `0` (off) to `255` (fully on).

```python
robot.set_led_pwm("left", 128)  # Half brightness on the left LED
```

### Building a fade profile with lists
Lists let you design the fade curve numerically. Starting at `0`, stepping up to `255`, and gliding back down creates a symmetric glow.

```python
steps = [0, 32, 64, 96, 128, 160, 192, 224, 255, 224, 192, 160, 128, 96, 64, 32, 0]
```

### Looping through each brightness step
A `for` loop visits every entry in the list. Apply each level to the LED and pause briefly so the fade is visible on the physical robot.

```python
import time

for level in steps:
    robot.set_led_pwm("left", level)
    robot.set_led_pwm("right", level)
    time.sleep(0.05)
```

### Publishing the fade summary
After the loop completes, publish the exact list so the backend can verify the profile. The verifier listens for a single `LED_FADE:` line with a `steps` field.

```python
robot.publish(f"LED_FADE:steps={steps}")
```

## Assignment
Create a program that defines a symmetric list of LED brightness values, runs a loop that applies each level to both LEDs with a short delay, and prints `LED_FADE:steps=[...]` so the playback sequence is recorded.

Platform API:
- `robot.set_led_pwm(channel: str, duty_cycle: int)` – set `"left"` or `"right"` LED brightness (0–255).
- `time.sleep(seconds: float)` – pause between PWM updates so the fade is perceptible.
- `robot.publish(message: str)` – send a heartbeat message to the MQTT log.

The work is complete when the `analog_led_fade` verification_function observes your `LED_FADE:` message, confirms the values stay in range, and replays the list to match the LED output.

## Conclusion
Well done! You combined lists, loops, and PWM to choreograph a smooth LED fade and documented the behaviour for automated checking. Up next you will reuse these collection skills to generate richer telemetry messages.
