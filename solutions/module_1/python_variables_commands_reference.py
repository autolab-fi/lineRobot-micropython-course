from lineRobot import Robot

robot = Robot()

# 1. Create variables
back_dist = 20.5
fwd_dist = 15

# 2. Move using variables
robot.move_backward_distance(back_dist)

robot.move_forward_distance(fwd_dist)

# 3. Calculate and print total distance
total_dist = back_dist + fwd_dist
print("Total distance:", total_dist, "cm")
