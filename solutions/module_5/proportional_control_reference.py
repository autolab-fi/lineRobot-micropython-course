import machine
import time
from lineRobot import Robot
from octoliner import Octoliner

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

octoliner.set_sensitivity(245)

base_speed = 20
kp = 30

print("Starting P-controller...")

lost_readings = 0
while True:
    sensor_array = octoliner.analog_read_all()
    time.sleep(0.01)
    position = octoliner.track_line()

    # Failsafe Check
    if max(sensor_array) < 700:
        lost_readings += 1
        if lost_readings < 5:
            time.sleep(0.01)
            continue
        print("Line lost samples:", sensor_array, "position:", position)
        print("CRITICAL: Line lost! Emergency Stop.")
        robot.stop()
        break
    else:
        lost_readings = 0
        # P-Controller Math
        P = kp * position
        left_speed = int(base_speed + P)
        right_speed = int(base_speed - P)

        # Send to motors
        robot.run_motors_speed(left_speed, right_speed)

    time.sleep(0.01)
