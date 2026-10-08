from lineRobot import Robot
import time
import math

robot = Robot()
R = 3.21
robot.reset_left_encoder()
robot.reset_right_encoder()
robot.run_motor_left(550)
robot.run_motor_right(550)
time.sleep(0.6)
robot.stop_motor_left()
robot.stop_motor_right()
# Let the wheels finish coasting before reading both counters.
time.sleep(0.3)
left_deg = robot.encoder_degrees_left()
print("Encoder degrees left:", left_deg)
distance = (left_deg / 360) * (2 * math.pi * R)
print("Distance in cm:", distance)
print("Encoder degrees right:", robot.encoder_degrees_right())
