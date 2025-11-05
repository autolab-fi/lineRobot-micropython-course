# **Lesson 3: Telemetry Heartbeat with Status Levels**

## **Lesson Objective**

Reuse the STATUS line from Module 6, add a computed health field, and organise the data with a dictionary before printing.

---

## **Introduction**

Module 6 collected the robot name, speed, battery voltage, and readiness flag into one STATUS message. Operators also want a quick answer to the question “is everything okay?”. This lesson shows how to calculate a health label from the same numbers, keep the values together in a dictionary, and publish the expanded heartbeat.

---

## **Theory**

### **Start from Known Variables**

Create the four variables again: `robot_name`, `speed_cm_s`, `battery_v`, and `is_ready`. These values continue to feed the STATUS message.

### **Classifying Health**

Use simple thresholds so the health field lines up with what the robot is doing:

- Report `low` if the battery is below `7.0` volts or the speed is `0`.
- Otherwise report `warn` if the battery is below `9.0` volts, the speed is below `10` cm/s, or `is_ready` is `False`.
- In all other cases report `ok`.

Store the text in a variable named `health_level`.

### **Store Everything in a Dictionary**

Placing the values in a dictionary keeps the code tidy and makes it easy to add the extra field.

```python
telemetry = {
    "name": robot_name,
    "speed": speed_cm_s,
    "battery": battery_v,
    "ready": is_ready,
    "health": health_level,
}
```

### **Publish One STATUS Line**

Stick with the format from earlier lessons and add the new field at the end.

```
STATUS:name=Robo;speed=42;battery=9.6;ready=True;health=ok
```

---

## **Assignment**

1. Define the four telemetry variables with sensible values.
2. Decide the `health_level` string using the thresholds above.
3. Build the `telemetry` dictionary containing the original fields plus the `"health"` entry.
4. Print a single STATUS line that includes all five fields so the `telemetry_heartbeat_health` verifier can check both the numbers and the decision.

---

## **Conclusion**

Adding a derived field to the STATUS heartbeat delivers both raw data and an easy-to-read summary. Keeping everything in a dictionary prepares you for longer reports in later modules.
