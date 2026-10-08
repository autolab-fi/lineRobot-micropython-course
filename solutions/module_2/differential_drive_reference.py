from lineRobot import Robot
import time

robot = Robot()

speed = 400
sp_offset = 40

# TODO: Start the left motor with a raw PWM value

robot.run_motor_left(speed)
robot.run_motor_right(speed + sp_offset)

# TODO: Start the right motor with a slightly different PWM value to fix the drift

# Wait for 3 seconds
time.sleep(3)

# TODO: Stop the motors

robot.stop()
