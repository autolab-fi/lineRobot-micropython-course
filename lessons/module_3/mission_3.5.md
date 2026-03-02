---
index: 18
module: module_3
task: led_feedback
previous: arrays_and_elif
next: simple_line_follower
---

# Mission 3.5 Visual Telemetry (LEDs)

## Objective
Learn the basics of GPIO (General Purpose Input/Output) and control the rover's onboard LED to provide physical visual feedback during a geological scan.

## Introduction
In the previous mission, your rover successfully scanned the lunar surface and reported the location of basaltic mineral veins to the terminal. However, in the harsh environment of the Moon, Mission Control cannot always stare at a computer screen. 

We need real-time, visual telemetry. Today, you will step away from the sensors for a moment to learn how to send electrical signals to external hardware, turning the rover's onboard LED into a "Target Locked" indicator!

## Theory

### 1. What is GPIO?
GPIO stands for "General Purpose Input/Output." It is the standard interface that allows the rover's "brain" (microcontroller) to interact with external physical devices. 
* **Input:** Reading signals (like we did with the Octoliner).
* **Output:** Sending signals (like sending voltage to a motor or a light).

![image](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_2/headlights_2.png?raw=True)

Now, we will focus on sending a logical high (voltage ON) and logical low (voltage OFF) signal to an LED (Light Emitting Diode). 

### 2. Setting the Pin Mode
Before sending any signal, we must tell the rover's computer *how* a specific hardware pin should behave. We do this using the `machine.Pin` function. 

To turn on a light, the pin must be configured as an Output (`machine.Pin.OUT`). The rover's primary LED is wired to **Pin 15**.

```python
import machine

# Configure Pin 15 as an Output and name it 'indicator_led'
indicator_led = machine.Pin(15, machine.Pin.OUT)
```

### 3. Writing to a Pin
Once the pin is configured as an output, you can control the electrical voltage going to it using the `.on()` and `.off()` commands.

```python
indicator_led.on()  # Sends voltage, turning the LED ON
indicator_led.off() # Stops voltage, turning the LED OFF
```

## Assignment
Upgrade your step-by-step geological scanner. Create a custom function that blinks the LED, and call it whenever the rover detects a mineral vein in any of its zones.

## Conclusion
Outstanding engineering! You now understand how GPIO works and how to manipulate external hardware.

By combining sensor inputs, custom functions, and LED outputs, you have created a smart, reactive system. You have mastered all the core pieces of robotics: reading sensors, making decisions, and controlling hardware. 