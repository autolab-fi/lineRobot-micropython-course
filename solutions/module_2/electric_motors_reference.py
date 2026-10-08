from lineRobot import Robot
import machine
from time import sleep
from octoliner import Octoliner

robot = Robot()

speed = 30
s_time = 2.5
sp_offset = 20

def moves(sp, st, off):
    robot.run_motors_speed(sp, sp + off)
    sleep(st)
    robot.stop()

moves(speed, s_time, sp_offset)
