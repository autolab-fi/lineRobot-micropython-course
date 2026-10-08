from lineRobot import Robot
import machine
import time
from octoliner import Octoliner

def diagnostic_sweep(speed_left, speed_right):
    print("Starting sweep...")
    for i in range(5):
        robot.run_motors_speed(speed_left, speed_right)
        time.sleep(0.1)
        robot.stop()

        # Completed TODOs
        position = octoliner.track_line()
        print("Error:", position)

        time.sleep(0.4)

    print("Returning to center...")
    robot.run_motors_speed(-speed_left, -speed_right)
    time.sleep(0.4)
    robot.stop()
    print("Sweep complete.")

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(245)

# Mission Sequence
diagnostic_sweep(-15, 15)
robot.move_forward_distance(30)
diagnostic_sweep(15, -15)
