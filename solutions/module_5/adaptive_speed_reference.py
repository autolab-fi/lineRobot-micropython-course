import machine
import time
from lineRobot import Robot
from octoliner import Octoliner

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

octoliner.set_sensitivity(245)

kp = 25
max_speed = 85
braking_force = 45

print("Starting Adaptive Speed Controller...")

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
        # Calculate Adaptive Speed
        dynamic_speed = max_speed - (braking_force * abs(position))

        # Calculate P-Controller Power
        P = kp * position

        # Apply Power to Dynamic Speed
        left_speed = int(dynamic_speed + P)
        right_speed = int(dynamic_speed - P)

        # Send to Motors
        robot.run_motors_speed(left_speed, right_speed)

    time.sleep(0.01)
