---
index: 6
module: module_2
task: headlights
previous: long_distance_race
next: alarm
---

# Lesson 6: Headlights

## Lesson objective

Learn about GPIO.

## Introduction

In this lesson, you will learn about a basic concept for microcontrollers - GPIO, and explore how it works using LEDs installed on the robot!

## Theory

### What is GPIO?

GPIO stands for "General Purpose Input/Output." It's an interface for the microcontroller to interact with external devices. GPIO pins allow us to read signals from a pin or write signals to a device. The signal for GPIO is voltage.

![image](https://github.com/autolab-fi/line-robot-curriculum/blob/main/images/module_2/headlights_2.png?raw=True)

Today, we'll only discuss signals of the logical high and logical low types: a low signal is 0 volts, while a high signal can have different values depending on the platform. For example, on Arduino Uno, Mega, Nano, this value will be 5 volts, but our robot uses an ESP32 board, where the logical high level is 3.3 volts. With GPIO pins, we can connect various devices, including:

- Buttons/switches
- Sensors
- LEDs
- Motors
- Displays
- etc.

### Controlling LED

So in this lesson, we're looking at an LED, which is a semiconductor device that emits light when an electric current passes through it. An LED is quite an interesting thing, and we can try to use GPIO on our board using it as an example. We can set the logical signal level using the **on()** function. But before sending any signal to a GPIO pin, we need to specify in which mode our GPIO pin should work - to read or to write a signal. To specify the operating mode of a GPIO pin, we can use the **machine.Pin()** function.

### Setting Pin Mode

To set the operating mode of a pin in MicroPython, create a **machine.Pin** object with the desired mode, such as **machine.Pin.OUT** for output or **machine.Pin.IN** for input.

### Writing to a Pin

To set a high or low logical voltage level, use the **on()** or **off()** methods of the Pin object. For example, **led.on()** sets the pin to a high voltage level, and **led.off()** sets it to a low voltage level.

**Example:**

```python
led_left = machine.Pin(15, machine.Pin.OUT); led_left.on()
```

### Example: Declaring and Using a Pin in MicroPython

```python
led_left = machine.Pin(15, machine.Pin.OUT); led_left.on()
```

## Assignment

Write a program that turns on two LEDs on the robot. The LEDs are connected to pins 15 and 2 and you should define in the code as **led_left** and **led_right**.

## Hint

You need to set the correct operating mode for the pin and send a signal to it. Create a **machine.Pin** object with the required mode for each pin, and use the **on()** or **off()** methods to send a signal to each pin.

## Conclusion

Congratulations! Now you know what GPIO is and how to send a logical signal to a pin!
