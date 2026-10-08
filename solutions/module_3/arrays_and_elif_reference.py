from lineRobot import Robot
import machine
from time import sleep
from octoliner import Octoliner

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(243)

robot = Robot()
threshold = 800

for i in range(5):
    robot.move_forward_distance(5)
    sleep(0.3)

    sensor_data = octoliner.analog_read_all()
    left_scout   = sensor_data[1]
    center_scout = sensor_data[3]
    right_scout  = sensor_data[6]

    if center_scout > threshold:
        print("Vein: Center")
    elif left_scout > threshold:
        print("Vein: Left")
    elif right_scout > threshold:
        print("Vein: Right")
    else:
        print("No minerals")

print("Survey complete.")
