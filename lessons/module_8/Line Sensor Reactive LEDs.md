# **Lesson 1: Line Sensor Reactive LEDs**

## **Lesson Objective**

Collect Octoliner readings in a list, decide whether the robot sees the line, drive the LEDs, and report the result with a single MQTT message.

---

## **Introduction**

Earlier modules showed how the line sensor reports eight light values and how LEDs can display quick feedback. In this lesson you will store the readings in order, use a small bit of logic to decide if the line is under the robot, mirror that decision to the LED hardware, and print one status line that matches the checker format.

---

## **Theory**

### **Lists Store the Eight Sensor Values**

`robot.read_line_sensors()` returns an iterable of eight numbers. Wrapping it in `list()` keeps the values together so you can check specific positions later.

```python
readings = list(robot.read_line_sensors())
```

### **Checking the Centre Sensors**

A typical threshold for detecting black tape is `120`. Looking at indexes `3` and `4` tells you whether the centre of the robot is still above the path.

```python
line_seen = readings[3] < 120 or readings[4] < 120
```

### **Dictionaries Describe LED States**

A dictionary keeps the LED decision clear and makes it easy to print the same information you show on the robot.

```python
leds = {"left": "on" if line_seen else "off", "right": "on" if line_seen else "off"}
```

### **Single-Line MQTT Output**

The verifier expects one line with the prefix `LINE_LED:`.

```
LINE_LED:state=on;readings=[212, 205, 48, 36, 210, 220, 225, 218]
```

Make sure the state you print comes from the actual sensor check.

---

## **Assignment**

1. Read the eight sensor values into a list named `readings`.
2. Decide if the line is seen by checking indexes `3` and `4` against the `120` threshold.
3. Build a dictionary named `leds` with keys `"left"` and `"right"` that match the decision.
4. Call `digitalWrite` for each LED so the hardware matches the dictionary.
5. Print a single line exactly like the example so the `line_sensor_leds` verifier can compare the LED state with the readings.

---

## **Conclusion**

Lists and dictionaries help you keep the sensor result, LED feedback, and debug message in sync. The same structure will support longer behaviours later in the module.
