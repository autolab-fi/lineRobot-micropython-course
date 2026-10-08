from lineRobot import Robot

robot = Robot()
side_length = 30
for i in range(4):
    robot.move_forward_distance(side_length)
    robot.turn_right()
