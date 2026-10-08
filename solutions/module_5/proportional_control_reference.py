import machine
import time
from lineRobot import Robot
from octoliner import Octoliner

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

octoliner.set_sensitivity(245)

base_speed = 30
kp = 20

print("Starting P-controller...")

while True:
    sensor_array = octoliner.analog_read_all()
    time.sleep(0.01)
    position = octoliner.track_line()

    # Failsafe Check
    if max(sensor_array) < 700:
        print("CRITICAL: Line lost! Emergency Stop.")
        robot.stop()
        break
    else:
        # P-Controller Math
        P = kp * position
        left_speed = int(base_speed + P)
        right_speed = int(base_speed - P)
        
        # Send to motors
        robot.run_motors_speed(left_speed, right_speed)

    time.sleep(0.01)
