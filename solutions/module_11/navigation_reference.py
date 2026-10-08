from lineRobot import Robot

robot = Robot()
first_distance = 20
long_distance = 40
small_angle = 45
large_angle = 90
# Moving to waypoint 1
robot.move_forward_distance(first_distance)
robot.turn_left_angle(small_angle)
# Moving to waypoint 2
robot.move_forward_distance(long_distance)
robot.turn_right_angle(small_angle)
# Moving to waypoint 3
robot.move_forward_distance(first_distance)
robot.turn_right_angle(large_angle)
# Moving to waypoint 4
robot.move_forward_distance(long_distance)
