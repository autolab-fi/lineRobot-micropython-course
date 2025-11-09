# Lesson 2: Analog LED Fade with Loops

## Lesson objective
Create a list of PWM brightness targets, iterate through them with a `for` loop, and publish the exact sequence used to fade the robot's LEDs.

## Introduction
Now that you can toggle LEDs on and off, it is time to explore pulse-width modulation (PWM) for smoother feedback in the remote lab. In this lesson you will build a list of brightness values, sweep through them with MicroPython, command the robot's LED driver, and document the sequence so the verifier can replay the effect.

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
Task: Program a PWM fade that raises the LEDs from off to full brightness and back down, driving both LEDs in sync and broadcasting the sequence you used.

Platform API:
- `robot.set_led_pwm(channel: str, duty_cycle: int)` – set `"left"` or `"right"` LED brightness (0–255).
- `time.sleep(seconds: float)` – pause between PWM updates so the fade is perceptible.
- `robot.publish(message: str)` – send a heartbeat message to the MQTT log.

Verification: The `analog_led_fade` verification_function waits for `LED_FADE:steps=[...]`, replays your list, and checks that every value stays within the allowed range and forms a smooth fade. Your submission passes once the printed sequence matches the LED output.

## Conclusion
Well done! You combined lists, loops, and PWM to choreograph a smooth LED fade and documented the behaviour for automated checking. Up next you will reuse these collection skills to generate richer telemetry messages.

## Links
- [MicroPython PWM Tutorial](https://docs.micropython.org/en/latest/tutorial/pwm.html)
