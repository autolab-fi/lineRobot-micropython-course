from lineRobot import Robot
robot = Robot()

angle = 90
d1 = 35
d2 = 25

#Moving to point 1
robot.move_forward_distance(d1)
robot.turn_left_angle(angle)

#Moving to point 2
robot.move_forward_distance(d2)
robot.turn_right_angle(angle)

#Moving to point 3
robot.move_forward_distance(d1)
robot.turn_right_angle(angle)


#Moving to final point
robot.move_forward_distance(d2)
