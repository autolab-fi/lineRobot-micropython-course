# Lesson 2: Analog LED Fade with Loops

## Lesson objective
Build confidence with Python lists and loops while coordinating gradual LED brightness changes.

## Introduction
Many robotics effects depend on repeating values in a specific order. Lists give you a convenient place to store that sequence, and loops let you step through each entry without rewriting the same command. Pairing those structures with pulse-width modulation (PWM) opens the door to smooth LED fades and other time-based behaviours.

## Theory

### Understanding PWM brightness
PWM rapidly toggles an LED on and off. A higher duty cycle means the LED spends more time on during each cycle, which the eye perceives as a brighter light.

```python
robot.set_led_pwm("left", 128)  # Half brightness on the left LED
```

### Designing sequences with lists
Lists can outline the entire fade pattern. A symmetric list climbs from dark to bright and then returns to dark.

```python
fade_steps = [0, 32, 64, 96, 128, 160, 192, 224, 255, 224, 192, 160, 128, 96, 64, 32, 0]
```

### Looping through each step
A `for` loop applies every list value in turn. Adding a short pause makes each stage visible on the physical robot.

```python
import time

for level in fade_steps:
    robot.set_led_pwm("left", level)
    robot.set_led_pwm("right", level)
    time.sleep(0.05)
```

### Recording the plan for verification
Telemetry messages can capture the exact list you executed, giving the verifier a record to check against the LED output.

```python
robot.publish(f"LED_FADE:steps={fade_steps}")
```

## Assignment
Create a program that defines a list of PWM levels, cycles both LEDs through each value with a short delay, and publishes a single line formatted `LED_FADE:steps=[...]` once the fade completes. The task is finished when the `analog_led_fade` verification_function reads your `LED_FADE:` message, confirms the levels stay within range, and replays the list to match the observed LED behaviour.

## Conclusion
Great job! You used lists to script a brightness pattern, loops to play it back, and telemetry to document the result. The final lesson shifts from lists to dictionaries so you can assemble richer telemetry reports.
