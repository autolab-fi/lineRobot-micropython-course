from lineRobot import Robot
import machine
from time import sleep
from octoliner import Octoliner

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

robot = Robot()

octoliner.set_sensitivity(243)
threshold = 800

robot.run_motors_speed(20, 20)

while True:
    sensor_3 = octoliner.analog_read(3)
    print(sensor_3)
    if sensor_3 > threshold:
        robot.stop()
        break
    sleep(0.05)

print("Target found. Rover stopped.")
