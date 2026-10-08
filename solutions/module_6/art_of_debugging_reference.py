import time
from lineRobot import Robot
from octoliner import Octoliner
import machine

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(240)
base_speed = 30
kp = 20
print("Beginning Bug Hunt")
while True:
    sensor_array = octoliner.analog_read_all()
    position = octoliner.track_line()
    print(sensor_array)
    if max(sensor_array) < 500:
        print("CRITICAL: Failsafe triggered! Stopping motors.")
        robot.stop()
        break
    else:
        P = kp * position
        left_speed = int(base_speed + P)
        right_speed = int(base_speed - P)
        robot.run_motors_speed(left_speed, right_speed)
        time.sleep(0.05)
