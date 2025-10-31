# **Lesson 5: Telemetry – Calculating Time**

## **Lesson Objective**

Calculate mission travel time using distance and speed, then publish it in an MQTT-formatted mission report.

---

## **Introduction**

Mission control dashboards need to know how long the robot will take to travel to a checkpoint. By dividing a known distance by the current speed, we can estimate the travel time and broadcast it as a `MISSION:` message. This lesson shows how to perform the calculation, round it to a readable value, and send the result for verification.

---

## **Theory**

### **Speed, Distance, and Time**

The basic relationship is:

```text
travel_time = distance / speed
```

If the distance is in centimetres and the speed is in centimetres per second, the result is measured in seconds.

---

## **Assignment**

1. Define variables for `distance_cm` (use `120`) and `speed_cm_s` (use `18.0`).
2. Compute `travel_time = distance_cm / speed_cm_s` using floating-point division.
3. Print the mission report exactly in the format:

   ```text
   MISSION:distance=120cm;speed=18.0cm/s;time=<value>s
   ```

4. The `<value>` portion must be the numeric time you calculated. Include the trailing `s`.
5. Run the script. The `mission_time_report` verification accepts answers within ±0.05 seconds of the mathematically correct value.

---

## **Conclusion**

You now know how to compute travel duration from distance and speed and how to present the result as structured telemetry. Accurate time estimates are a foundation for scheduling robot missions and coordinating multi-robot fleets.
