from lineRobot import Robot
import time

robot = Robot()
robot.run_motors_speed(30, 30)
time.sleep(6.4)
robot.stop()
