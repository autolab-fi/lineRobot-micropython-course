from lineRobot import Robot
import machine
import time
from octoliner import Octoliner

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

robot = Robot()

sensi = 243
threshold = 900
dist = 1

def detect_line(sensitivity, distance, threshold):
    octoliner.set_sensitivity(sensitivity)
    for i in range(15):
        robot.move_forward_distance(distance)
        sensor_3 = octoliner.analog_read(3)
        sensor_4 = octoliner.analog_read(4)
        if sensor_3 > threshold:
            print(f"Sensor 3 : {sensor_3} Found geological layers!")
        if sensor_4 > threshold:
            print(f"Sensor 4: {sensor_4} Found geological layers!")
        time.sleep(0.1)

detect_line(sensi, dist, threshold)
