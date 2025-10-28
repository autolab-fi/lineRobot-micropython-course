# **Lesson 7: Working with Lists – Adding, Removing, and Measuring**

## **Lesson Objective**

Practise modifying mixed-type lists using `append()`, `pop()`, and `del`, then publish the contents and length via MQTT.

---

## **Introduction**

Lists can store any combination of values: strings for names, integers for speeds, floats for voltages, and booleans for readiness flags. Changing the list while the program runs is a powerful way to keep track of robot state. In this lesson we will adjust a list and report both its contents and its length to confirm the operations.

---

## **Theory**

### **Creating Mixed Lists**

```python
robot_info = ["LineRacer", 15, 7.4, True]
```

A single list can hold different types. This allows you to combine descriptive text with numeric data.

### **Adding and Removing Elements**

- `append(value)` adds an item to the end of the list.
- `pop(index)` removes and returns the element at `index`. If no index is given, the last element is removed.
- `del list[index]` deletes the element at `index` without returning it.

### **Measuring Lists**

- `len(list_name)` counts the number of items.
- `sum()` only works on numeric values, so mixed lists require selecting the numeric elements before summing them.

---

## **Example Implementation**

```python
robot_info = ["LineRacer", 15, 7.4, True]
robot_info.append("Ready")     # add a status string
removed_speed = robot_info.pop(1)  # remove the old speed value
del robot_info[1]              # delete the voltage to demonstrate del

print(f"LIST:items={robot_info}")
print(f"LIST:length={len(robot_info)}")
```

The output confirms both the modified list and the number of remaining entries.

---

## **Assignment**

1. Start with a list containing at least three items of at least two different data types.
2. Use `append()` to add a new element and `pop()` (or `del`) to remove one.
3. After the modifications, print two MQTT messages:

   ```text
   LIST:items=<your_list>
   LIST:length=<len_value>
   ```

4. Ensure the printed length matches the actual number of elements in the list.
5. Run the program. The `list_operations_check` verification watches for the `LIST:` messages and confirms that the list length updates correctly after the modifications.

---

## **Conclusion**

You have experimented with adding and removing elements from a mixed-type list and reported the results in MQTT format. These skills help maintain dynamic state information for more complex robot behaviours.
