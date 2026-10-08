from lineRobot import Robot

robot = Robot()
robot.turn_left_angle(45)
robot.move_forward_distance(20)
for i in range(3):
    robot.turn_right()
    robot.move_forward_distance(20)
