from lineRobot import Robot
import time

robot = Robot()

route = [55, 60, 70]  # can be different, depends on object placement

total_waypoints = len(route)
print("Mission Control, I have received", total_waypoints, "waypoints.")

for distance in route:
    robot.move_forward_distance(distance)
    robot.turn_right()
    time.sleep(1)
