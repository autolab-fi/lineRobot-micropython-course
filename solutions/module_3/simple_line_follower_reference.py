import machine
import time
from octoliner import Octoliner
from lineRobot import Robot

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(245)
robot = Robot()

threshold = 700
speed = 15
turn_speed = 5

while True:
    sensor_data  = octoliner.analog_read_all()
    left_scout   = sensor_data[6]
    center_scout = sensor_data[3]
    right_scout  = sensor_data[1]

    if center_scout > threshold:
        robot.run_motors_speed(speed, speed)
        print("straight")
    elif left_scout > threshold:
        robot.turn_left_angle(5)
        print("left")
    elif right_scout > threshold:
        robot.turn_right_angle(5)
        print("right")
    else:
        robot.run_motors_speed(15, 15)
        print("looking for a line")

    time.sleep(0.05)
