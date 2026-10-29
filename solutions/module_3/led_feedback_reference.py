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

indicator_led = machine.Pin(15, machine.Pin.OUT)

def blinkLED():
    indicator_led.on()
    time.sleep(0.2)
    indicator_led.off()
    time.sleep(0.2)

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
    if left or center or right:
        blinkLED()

print("Survey complete.")
