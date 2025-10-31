# **Lesson 4: MQTT Greeting of Variables**

## **Lesson Objective**

Declare variables of multiple types and publish them in a single MQTT-style status message.

---

## **Introduction**

Robots often send compact updates about their status to a control dashboard. MicroPython variables let us store the information we want to broadcast—such as the robot name, speed, battery voltage, and readiness flag. In this lesson we will gather those values and format them into one line that begins with `STATUS:` so it can be parsed by the checker.

---

## **Theory**

### **Core Variable Types**

- `str` – stores text such as the robot model name.
- `int` – stores whole numbers like speed in centimetres per second.
- `float` – stores decimal values, for example battery voltage.
- `bool` – stores `True` or `False` for status indicators.

### **Building MQTT Strings**

Formatted string literals (f-strings) combine text with variable values. Curly braces `{} ` are replaced with the values of the variables inside them when the string is evaluated.

```python
Name = "Alex"
Age = 18

print(f"Name={Name};Age={Age}")
```

## **Assignment**

1. Create variables named `robot_name`, `speed_cm_s`, `battery_v`, and `is_ready` with appropriate values.
2. Ensure the data types make sense:
   - `robot_name` → non-empty string
   - `speed_cm_s` → integer speed (1–200 cm/s recommended)
   - `battery_v` → float voltage (0–20 V range)
   - `is_ready` → boolean flag (`True` or `False`)
3. Use a single `print()` call to output:

   ```text
   STATUS:name=<robot_name>;speed=<speed_cm_s>;battery=<battery_v>;ready=<is_ready>
   ```

4. Run the program. The `hello_mqtt_variables` verification listens for the message and validates both the formatting and the values.

---

## **Conclusion**

You now know how to store robot data in variables and combine them into a formatted MQTT message. This approach keeps status updates structured and prepares you for more advanced telemetry in the following lessons.
