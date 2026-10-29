import machine
import time
from octoliner import Octoliner
from lineRobot import Robot

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(243)
robot = Robot()
threshold = 800

for i in range(5):
    robot.move_forward_distance(5)
    time.sleep(0.5)
    sensor_data = octoliner.analog_read_all()
    left = sensor_data[6] > threshold
    center = sensor_data[3] > threshold
    right = sensor_data[1] > threshold
    count = int(left) + int(center) + int(right)

    if count == 0:
        print("No line")
    elif count == 1:
        print("Line in one zone")
    else:
        print("Line in multiple zones")
    print("Left:", left, "Center:", center, "Right:", right)

print("Survey complete.")
