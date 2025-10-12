# Python 101: Programming for Line-Following Robotics

**Platform:** ondroid.org | **Duration:** 7 weeks | **Total Lessons:** 40

---

## Week 1: Introduction to Python Programming (6 lessons)

**Focus:** Python basics, syntax, variables, operators, environment setup

### Lesson 1.1: Introduction to Python
- **Topics:** What is Python, installation, IDEs, first program, print()
- **Assignment:** Install Python, write "Hello World", explore IDE features
- **Functions Used:** `print()`

### Lesson 1.2: Variables and Basic Data Types
- **Topics:** Variables, integers, floats, strings, naming conventions
- **Assignment:** Create variables for robot parameters (speed, distance, sensor values)
- **Functions Used:** Variable assignment, type()

### Lesson 1.3: Arithmetic Operators
- **Topics:** +, -, *, /, //, %, **, order of operations
- **Assignment:** Calculate robot wheel circumference, distance traveled, speed conversions
- **Functions Used:** Math operators

### Lesson 1.4: Comparison Operators
- **Topics:** ==, !=, >, <, >=, <=, boolean values
- **Assignment:** Compare sensor threshold values, determine line detection
- **Functions Used:** Comparison operators, bool()

### Lesson 1.5: String Operations
- **Topics:** Concatenation, f-strings, string methods, formatting
- **Assignment:** Create formatted robot status messages with multiple data types
- **Functions Used:** String methods, f-strings

### Lesson 1.6: Basic Input/Output
- **Topics:** print() formatting, input(), type conversion
- **Assignment:** Create interactive robot configuration program with user input
- **Functions Used:** `print()`, `input()`, `int()`, `float()`, `str()`

---

## Week 2: Data Types and Collections (6 lessons)

**Focus:** Lists, tuples, data storage, manipulation, formatted output

### Lesson 2.1: Introduction to Lists
- **Topics:** Creating lists, indexing, accessing elements, list basics
- **Assignment:** Store Octoliner 8-sensor readings in a list, access specific sensors
- **Functions Used:** Lists, indexing `[]`

### Lesson 2.2: List Methods
- **Topics:** append(), extend(), insert(), remove(), pop(), sort()
- **Assignment:** Build turn command queue, add/remove commands dynamically
- **Functions Used:** `.append()`, `.remove()`, `.pop()`, `.sort()`

### Lesson 2.3: Tuples
- **Topics:** Creating tuples, immutability, tuple packing/unpacking
- **Assignment:** Store encoder positions as (left, right) tuples, RGB colors as tuples
- **Functions Used:** Tuples `()`, unpacking

### Lesson 2.4: List Slicing
- **Topics:** Slicing syntax [start:end:step], negative indices, copying
- **Assignment:** Extract sensor subsets, reverse lists, create circular buffers
- **Functions Used:** Slicing `[:]`

### Lesson 2.5: Nested Lists
- **Topics:** Lists of lists, 2D arrays, accessing nested elements
- **Assignment:** Store multiple Octoliner readings over time, create 2D grid
- **Functions Used:** Nested indexing `[][]`

### Lesson 2.6: F-strings and Formatting
- **Topics:** F-string syntax, formatting specifiers, alignment, precision
- **Assignment:** Create professional telemetry display with aligned columns
- **Functions Used:** F-strings, format specifiers

---

## Week 3: Functions and Modules (6 lessons)

**Focus:** Function definition, parameters, return values, modules, libraries

### Lesson 3.1: Defining Functions
- **Topics:** def keyword, parameters, function body, calling functions
- **Assignment:** Create move_square(), move_triangle() functions using Robot library
- **Functions Used:** `def`, `move_forward_distance()`, `turn_left()`

### Lesson 3.2: Function Parameters
- **Topics:** Positional parameters, default values, keyword arguments
- **Assignment:** Create configurable movement functions with optional speed/distance
- **Functions Used:** Function parameters, default values

### Lesson 3.3: Return Values
- **Topics:** return keyword, returning single/multiple values, None
- **Assignment:** Create encoder calculation functions (degrees to distance, etc.)
- **Functions Used:** `return`, `encoder_degrees_left()`, `encoder_degrees_right()`

### Lesson 3.4: Docstrings and Documentation
- **Topics:** Triple-quoted strings, documenting functions, help()
- **Assignment:** Document all previous functions with proper docstrings
- **Functions Used:** Docstrings `"""..."""`, `help()`

### Lesson 3.5: Importing Modules
- **Topics:** import, from...import, aliasing with as, standard library
- **Assignment:** Use math module for sensor calculations, time module for delays
- **Functions Used:** `import math`, `import time`, `math.sqrt()`, `time.sleep()`

### Lesson 3.6: Creating Your Own Module
- **Topics:** Module structure, __name__, organizing code into files
- **Assignment:** Create robot_utils.py module with all utility functions
- **Functions Used:** Module creation, imports

---

## Week 4: Arrays, Lists, and Data Structures (6 lessons)

**Focus:** Advanced list operations, comprehensions, nested structures

### Lesson 4.1: List Comprehensions
- **Topics:** [expression for item in list], conditional comprehensions
- **Assignment:** Process Octoliner data - normalize, filter, threshold in one line
- **Functions Used:** List comprehensions

### Lesson 4.2: Iterating Over Lists
- **Topics:** for loops, enumerate(), zip(), range()
- **Assignment:** Iterate through sensor arrays, pair left/right encoder readings
- **Functions Used:** `for`, `enumerate()`, `zip()`, `range()`

### Lesson 4.3: List Operations
- **Topics:** Concatenation, repetition, membership (in), min/max/sum
- **Assignment:** Combine sensor lists, check for values, calculate statistics
- **Functions Used:** `+`, `*`, `in`, `min()`, `max()`, `sum()`, `len()`

### Lesson 4.4: Dictionaries
- **Topics:** Key-value pairs, accessing, adding, removing items
- **Assignment:** Store robot configuration as dictionary, color sensor readings
- **Functions Used:** `{}`, `.keys()`, `.values()`, `.items()`

### Lesson 4.5: Nested Data Structures
- **Topics:** Lists of dicts, dicts of lists, complex structures
- **Assignment:** Create color log with {position, rgb, timestamp} dictionaries
- **Functions Used:** Nested structures

### Lesson 4.6: Sorting and Searching
- **Topics:** sorted(), .sort(), custom sort keys, searching lists
- **Assignment:** Sort color samples by position/brightness, search for specific colors
- **Functions Used:** `sorted()`, `.sort()`, `key=lambda`

---

## Week 5: Control Flow and Error Handling (6 lessons)

**Focus:** Conditionals, loops, exceptions, debugging, validation

### Lesson 5.1: If Statements
- **Topics:** if, elif, else, boolean logic, nested conditionals
- **Assignment:** Implement relay controller logic for line following decisions
- **Functions Used:** `if`, `elif`, `else`, `count_of_black()`

### Lesson 5.2: While Loops
- **Topics:** while condition, break, continue, loop control
- **Assignment:** Continuous sensor polling loop with exit conditions
- **Functions Used:** `while`, `break`, `continue`, `analog_read_all()`

### Lesson 5.3: For Loops Deep Dive
- **Topics:** Iterating sequences, nested loops, loop else clause
- **Assignment:** Process 2D sensor history, analyze patterns over time
- **Functions Used:** Nested `for` loops

### Lesson 5.4: Exception Handling Basics
- **Topics:** try, except, finally, common exception types
- **Assignment:** Handle I2C sensor read errors gracefully
- **Functions Used:** `try`, `except OSError`, `except IndexError`

### Lesson 5.5: Raising Exceptions
- **Topics:** raise keyword, custom error messages, validation
- **Assignment:** Create parameter validation functions (distance, angle, PWM ranges)
- **Functions Used:** `raise ValueError`, `raise TypeError`

### Lesson 5.6: Debugging Techniques
- **Topics:** Print debugging, understanding tracebacks, logical reasoning
- **Assignment:** Debug intentionally broken line follower code
- **Functions Used:** `print()`, error analysis

---

## Week 6: MicroPython and Embedded Systems (6 lessons)

**Focus:** MicroPython basics, hardware interfacing, GPIO, motors, encoders

### Lesson 6.1: Introduction to MicroPython
- **Topics:** MicroPython vs Python, ESP32 platform, constraints, deployment
- **Assignment:** Flash MicroPython firmware, run first embedded program
- **Functions Used:** MicroPython REPL

### Lesson 6.2: GPIO Control
- **Topics:** machine.Pin, digital output, LED control
- **Assignment:** Blink LEDs on pins 2 and 15, create patterns
- **Functions Used:** `machine.Pin()`, `.on()`, `.off()`

### Lesson 6.3: Timing in MicroPython
- **Topics:** time.sleep(), time.sleep_ms(), non-blocking delays
- **Assignment:** Create LED alarm pattern with precise timing
- **Functions Used:** `time.sleep()`, `time.sleep_ms()`

### Lesson 6.4: Motor PWM Control
- **Topics:** PWM basics, run_motor_left/right(), speed control
- **Assignment:** Implement motor acceleration/deceleration ramps
- **Functions Used:** `run_motor_left()`, `run_motor_right()`, `stop()`

### Lesson 6.5: Reading Encoders
- **Topics:** encoder_degrees_left/right(), position tracking, odometry
- **Assignment:** Track distance traveled using encoder feedback
- **Functions Used:** `encoder_degrees_left()`, `encoder_degrees_right()`, `reset_encoders()`

### Lesson 6.6: Differential Drive
- **Topics:** Differential drive kinematics, motor synchronization
- **Assignment:** Drive straight using manual PWM control, no high-level functions
- **Functions Used:** `run_motor_left()`, `run_motor_right()`, encoders

---

## Week 7: Advanced Topics and Integration (10 lessons)

**Focus:** I2C sensors, validation, nested structures, line following, PID control

### Lesson 7.1: I2C Communication
- **Topics:** machine.I2C, bus scanning, multi-device communication
- **Assignment:** Initialize I2C bus, scan for Octoliner and color sensor
- **Functions Used:** `machine.I2C()`, `.scan()`

### Lesson 7.2: Octoliner Setup
- **Topics:** Octoliner.begin(), set_sensitivity(), analog_read()
- **Assignment:** Initialize Octoliner, read individual sensors
- **Functions Used:** `Octoliner()`, `begin()`, `set_sensitivity()`, `analog_read()`

### Lesson 7.3: Octoliner Array Reading
- **Topics:** analog_read_all(), sensor array processing
- **Assignment:** Read all 8 sensors, display formatted output
- **Functions Used:** `analog_read_all()`

### Lesson 7.4: Octoliner Calibration
- **Topics:** optimize_sensitivity_on_black(), auto-calibration
- **Assignment:** Implement automatic sensor calibration routine
- **Functions Used:** `optimize_sensitivity_on_black()`, `get_sensitivity()`

### Lesson 7.5: Color Sensor Integration
- **Topics:** tcs3472(), rgb(), light(), color classification
- **Assignment:** Read RGB values, classify colors (red/green/blue/yellow)
- **Functions Used:** `tcs3472()`, `rgb()`, `light()`, `brightness()`

### Lesson 7.6: Data Validation Techniques
- **Topics:** Type checking, range validation, format verification
- **Assignment:** Validate all robot parameters before execution
- **Functions Used:** `isinstance()`, `type()`, conditional logic

### Lesson 7.7: Line Position Tracking
- **Topics:** track_line(), position range -1.0 to 1.0, count_of_black()
- **Assignment:** Read line position continuously, detect line states
- **Functions Used:** `track_line()`, `count_of_black()`, `digital_read_all()`

### Lesson 7.8: Proportional Controller
- **Topics:** P controller, error calculation, Kp tuning
- **Assignment:** Implement P controller for line following
- **Functions Used:** `track_line()`, `run_motors_speed()`

### Lesson 7.9: PI Controller
- **Topics:** Integral accumulation, windup protection, Ki tuning
- **Assignment:** Add integral term to P controller
- **Functions Used:** All line-following functions, integral calculation

### Lesson 7.10: Complete PID Line Follower
- **Topics:** Full PID, derivative smoothing, intersection detection
- **Assignment:** Build complete autonomous line follower with PID control
- **Functions Used:** All robot, Octoliner, TCS34725 functions

---

*Version: 2.0 | Last Updated: October 13, 2025 | Platform: ondroid.org*
