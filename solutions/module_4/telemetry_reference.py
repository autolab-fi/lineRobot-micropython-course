from lineRobot import Robot
import time

robot = Robot()

robot_name = "Artemis-1"
is_ready   = True
distance   = 40

start_time = time.time()
robot.move_forward_distance(distance)
end_time   = time.time()

duration   = end_time - start_time
speed_cm_s = distance / duration

print(f"STATUS:name={robot_name};dist={distance};time={duration};speed={speed_cm_s};ready={is_ready}")
