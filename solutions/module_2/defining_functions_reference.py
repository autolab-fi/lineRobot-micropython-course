from lineRobot import Robot
import time

robot = Robot()

def turn_around():
    robot.run_motors_speed(50, -50)
    time.sleep(0.63)
    robot.stop()

turn_around()
