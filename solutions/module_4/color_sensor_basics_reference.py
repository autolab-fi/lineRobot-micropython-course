from lineRobot import Robot
import machine
from tcs3472 import tcs3472
import time

robot = Robot()

bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
color_sensor = tcs3472(bus)

for step in range(6):
    r, g, b = color_sensor.rgb()
    print(f"Scan - R:{r} G:{g} B:{b}")
    robot.move_forward_distance(10)
    time.sleep(0.5)

print("Linear scan complete.")
