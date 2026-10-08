import machine
import time
from octoliner import Octoliner
from lineRobot import Robot

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(243)
robot = Robot()

threshold = 700
speed = 15
turn_speed = 3
left_speed = speed
right_speed = speed
lost_samples = 0
lost_limit = 15

while True:
    sensor_data = octoliner.analog_read_all()
    left_scout = max(sensor_data[5], sensor_data[6], sensor_data[7])
    center_scout = max(sensor_data[3], sensor_data[4])
    right_scout = max(sensor_data[0], sensor_data[1], sensor_data[2])

    if center_scout > threshold:
        left_speed, right_speed = speed, speed
        lost_samples = 0
    elif left_scout > threshold:
        left_speed, right_speed = turn_speed, speed
        lost_samples = 0
    elif right_scout > threshold:
        left_speed, right_speed = speed, turn_speed
        lost_samples = 0
    else:
        lost_samples += 1
        if lost_samples >= lost_limit:
            robot.stop()
            print("Line lost. Stop and check the starting position.")
            break

    robot.run_motors_speed(left_speed, right_speed)
    time.sleep(0.02)
