# **Lesson 2: Analog LED Fade with Loops**

## **Lesson Objective**

Use a list of brightness steps to drive PWM with a `for` loop, create a smooth LED fade, and share the steps through MQTT.

---

## **Introduction**

Pulse-width modulation (PWM) lets the robot output more than just on or off. By sending different duty cycles to the LED, you can make it brighten and dim. This lesson walks through building a list of target levels, playing them back with a loop, and printing the exact sequence so the checker can replay the fade.

---

## **Theory**

### **PWM Basics**

`analogWrite(pin, value)` accepts values from `0` (off) to `255` (fully on). Moving through that range slowly creates a visible ramp.

### **Lists Keep the Sequence Clear**

Storing the targets in a list shows the shape of the fade and makes it easy to tweak.

```python
steps = [0, 32, 64, 96, 128, 160, 192, 224, 255, 224, 192, 160, 128, 96, 64, 32, 0]
```

### **Looping Over Each Step**

A `for` loop sends every value to the LED. Add a short pause so the change is visible.

```python
for level in steps:
    analogWrite(robot.LED_LEFT, level)
    time.sleep(0.05)
```

### **MQTT Summary Line**

The verifier reads one line beginning with `LED_FADE:` followed by the list you used.

```
LED_FADE:steps=[0, 32, 64, 96, 128, 160, 192, 224, 255, 224, 192, 160, 128, 96, 64, 32, 0]
```

---

## **Assignment**

1. Build a list named `steps` that rises from `0` to at least `255` and returns to `0`.
2. Loop over the list and call `analogWrite` on one LED for each value.
3. Include `time.sleep` inside the loop so the fade is smooth.
4. After the loop, print the MQTT line above so the `analog_led_fade` verifier can match your program.

---

## **Conclusion**

Lists and loops give you precise control over PWM output. Recording the same list in your printout documents the effect and lets the verifier check every brightness level.
