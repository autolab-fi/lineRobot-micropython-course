# **Lesson 6: Sensor Log – List and Aggregates**

## **Lesson Objective**

Collect multiple sensor readings in a list, compute summary values, and broadcast them through MQTT log messages.

---

## **Introduction**

Robots rarely rely on a single measurement. By storing successive readings in a list we can determine how many samples we have, display them together, and report statistics such as the average. The verification tool listens for three separate `LOG:` messages that must agree with each other, so careful formatting is important.

---

## **Theory**

### **Lists of Integers**

A Python list can hold multiple values under one name. Indexing starts at `0` and continues to `len(list) - 1`.

```python
sensor_values = [132, 128, 140]
```

### **Aggregate Functions**

- `len(sensor_values)` returns how many readings are stored.
- `sum(sensor_values)` adds the readings together.
- `average = sum(sensor_values) / len(sensor_values)` computes the mean value. Convert to a float to show decimals when needed.

### **Printing Multiple Messages**

Each `print()` call sends one message. The assignment expects three lines in this order:

1. `LOG:COUNT=<count>`
2. `LOG:VALUES=<v1,v2,...>`
3. `LOG:AVERAGE=<average>`

---

## **Example Implementation**

```python
sensor_values = [132, 128, 140, 137]
count = len(sensor_values)
average = sum(sensor_values) / count

print(f"LOG:COUNT={count}")
print("LOG:VALUES=" + ",".join(str(value) for value in sensor_values))
print(f"LOG:AVERAGE={average:.2f}")
```

The second line uses `join()` to combine the integer readings into a comma-separated string. `{average:.2f}` keeps the average readable while preserving accuracy.

---

## **Assignment**

1. Create a list with at least three integer sensor readings.
2. Calculate the total count and the average value of the list.
3. Print the three required `LOG:` messages exactly in the specified order and format.
4. Run the script. The `sensor_log_summary` verification confirms that the reported count matches the number of values and that the average is within ±0.05 of the calculated result.

---

## **Conclusion**

You have practised storing data in a list, computing aggregates, and sharing the results through MQTT messages. These techniques help summarize sensor behaviour for monitoring dashboards and automated analysis tools.
