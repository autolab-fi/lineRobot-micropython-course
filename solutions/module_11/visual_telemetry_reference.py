import machine
import time
from lineRobot import Robot
from octoliner import Octoliner

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(245)
led = machine.Pin(15, machine.Pin.OUT)
while True:
    robot.run_motors_speed(20, 20)
    sensors = octoliner.analog_read_all()
    if sensors[3] > 500 or sensors[4] > 500:
        robot.stop()
        break
    time.sleep(0.05)
for i in range(3):
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
