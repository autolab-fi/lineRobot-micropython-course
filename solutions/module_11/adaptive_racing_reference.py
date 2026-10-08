import time
from lineRobot import Robot
from octoliner import Octoliner
import machine

max_vel = 70
brake_f = 45
k_prop = 35
robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(240)
print("Starting Adaptive Racing Controller...")
while True:
    position = octoliner.track_line()
    dynamic_speed = max_vel - (brake_f * abs(position))
    P = k_prop * position
    left_wheel = int(dynamic_speed + P)
    right_wheel = int(dynamic_speed - P)
    robot.run_motors_speed(left_wheel, right_wheel)
    time.sleep(0.05)
