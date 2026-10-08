import machine
import time
from lineRobot import Robot
from octoliner import Octoliner

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

octoliner.set_sensitivity(245)

print("Starting tracking...")

while True:
    sensor_array = octoliner.analog_read_all()
    time.sleep(0.01)  # Let sensors stabilize
    position = octoliner.track_line()

    # Failsafe Check - if no sensor detects line
    if max(sensor_array) < 700:
        print("CRITICAL: Line lost! Emergency Stop.")
        robot.stop()
        break
    else:
        # Simple Control Logic
        if position < -0.3:
            robot.run_motors_speed(5, 25)   # Turn left
        elif position > 0.3:
            robot.run_motors_speed(25, 5)   # Turn right
        else:
            robot.run_motors_speed(20, 20)  # Go straight

    time.sleep(0.01)
