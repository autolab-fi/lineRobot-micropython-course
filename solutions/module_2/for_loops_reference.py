from lineRobot import Robot
import machine
import time
from octoliner import Octoliner

robot = Robot()
side = 60
step = 5
w_time = 0.1


for i in range(0, 10):
    robot.move_forward_distance(side)
    robot.turn_right_angle(90)
    time.sleep(w_time)
    side -= step

robot.stop()
