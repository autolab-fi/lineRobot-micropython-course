# Robot Course Development Plan

## Module 0: Introduction to the Robot
**Description:** Getting familiar with the platform and learning how to control the robot.

### Lessons

#### 1. Sandbox
**What you'll learn:** Introduction to the platform, listing all peripherals, describing what we will be working with, and outlining any restrictions on libraries and tag words.

#### 2. Test drive
**What you'll learn:** Some introductory words on moving the robot forward using a library.

#### 3. License to drive
**What you'll learn:** Writing a simple program independently, similar to the previous lesson.

---

## Module 1: Controlling Robot Movement
**Description:** Demonstrating the robot's capabilities.

### Lessons

#### 4. Short distance race
**What you'll learn:** Using library functions to move a specific distance, both forward and backward.

#### 5. Maneuvering
**What you'll learn:** Turning right and left in place. Task: Read data from a file and write it to another.

#### 6. Fruit Ninja
**What you'll learn:** Writing a program with a sequence of commands to move along a trajectory depicted in the diagram.

---

## Module 2: Controlling LEDs
**Description:** Basic arduino functions of working with GPIO using LEDs as examples.

### Lessons

#### 7. Headlights
**What you'll learn:** Understanding how LEDs work. Task: Turning on LEDs.

#### 8. Robot's alarm
**What you'll learn:** More about the digitalWrite() and pinMode() functions. Task: Blinking LEDs.

---

## Module 3: Controlling Motors
**Description:** Studying robot kinematics. Writing functions. What are DC motors.

### Lessons

#### 9. Differential drive
**What you'll learn:** An introduction to the robot's kinematics. Task: Experiment with functions for moving the robot forward.

#### 10. Movement Function
**What you'll learn:** Writing functions in Arduino. Task: Write a function to rotate the robot.

#### 11. Electric Motor
**What you'll learn:** Basic principles of DC motors. Task: Move to a specific point on the map using only functions for controlling motors.

---

## Module 5: Line Sensor Introduction
**Description:** Understanding how IR line sensors work and detecting black lines using the Octoliner sensor array.

### Lessons

#### 12. Line Sensor and Black Line Detection
**What you'll learn:** This lesson focuses on understanding how an Octoliner sensor detects black lines using IR sensors and implementing black line detection.

---

## Module 6: Programming Fundamentals
**Description:** Essential programming concepts including variables, conditional statements, loops, and arrays for robot control.

### Lessons

#### 13. Introduction to Variables and Conditional Statements
**What you'll learn:** Learn how to declare and use variables in programming, and apply conditional logic using if, else if, and else statements.

#### 14. Loops and Conditional Logic
**What you'll learn:** Learn how to repeat actions using for and while loops combined with conditional statements.

#### 15. Arrays and Processing Data with Loops
**What you'll learn:** Understand how to use arrays to store and analyze sensor data with systematic data collection.

#### 16. MQTT Greeting of Variables
**What you'll learn:** Declare variables of different types and broadcast them in a single MQTT status line.

#### 17. Telemetry: Calculating Time
**What you'll learn:** Compute mission travel time from distance and speed and format it as telemetry.

#### 18. Sensor Log: List and Aggregates
**What you'll learn:** Summarise a list of sensor readings by reporting the count, values, and average.

#### 19. Working with Lists: Adding, Removing, and Measuring
**What you'll learn:** Manipulate a mixed-type list and report its contents and length via MQTT.

---

## Module 7: Advanced Line Following
**Description:** Advanced line following techniques including relay, P, PI, and PID controllers for smooth and accurate robot movement.

### Lessons

#### 20. Relay, P, and PI Controllers
**What you'll learn:** Understand how different types of controllers work — Relay, Proportional (P), and Proportional-Integral (PI) for line following.

#### 21. P and PI Controllers
**What you'll learn:** Learn about Proportional and Proportional-Integral controllers for improved line following performance.

#### 22. PID Controller
**What you'll learn:** Implement a complete PID controller combining proportional, integral, and derivative terms for optimal line following.

---

## Module 8: Lists, Dictionaries and More
**Description:** Hands-on assignments that connect sensors, LEDs, PWM, and telemetry using MicroPython data structures.

### Lessons

#### 23. Telemetry Heartbeat with Status Levels
**What you'll learn:** Derive a health flag from readiness, speed, and battery data and include it in the STATUS heartbeat.

#### 24. Line Sensor Reactive LEDs
**What you'll learn:** Mirror Octoliner readings to the LEDs using lists and dictionaries, then report the snapshot over MQTT.
