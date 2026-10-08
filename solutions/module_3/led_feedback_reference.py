from lineRobot import Robot
import machine
from time import sleep
from octoliner import Octoliner

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(243)

robot = Robot()
led = machine.Pin(15, machine.Pin.OUT)

threshold = 800

def blink_led():
    for i in range(0, 5):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)

for i in range(15):
    robot.move_forward_distance(2)
    sleep(0.3)

    sensor_data = octoliner.analog_read_all()
    left_scout   = sensor_data[1]
    center_scout = sensor_data[3]
    right_scout  = sensor_data[6]

    if center_scout > threshold:
        print("Vein: Center")
        blink_led()
    elif left_scout > threshold:
        print("Vein: Left")
        blink_led()
    elif right_scout > threshold:
        print("Vein: Right")
        blink_led()
    else:
        print("No minerals")

print("Survey complete.")
