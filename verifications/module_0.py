import cv2
import math
import time


# start points for the tasks
target_points = {
    'sandbox': [(50, 50), (30, 0)]
}

# The dictionary specifies the disabled movement functions of the library. This is necessary to prevent cheating.  
# For example, if the task is to write a function for robot movement, the user might attempt 
# to call a library function directly.
# However, these functions will be disabled if the corresponding value in the dictionary is set to `True`.
block_library_functions = {
    'sandbox': False,
}

# function to get value from dictionary block_library_functions
def get_block_library_functions(task):
    global block_library_functions
    return block_library_functions[task]


# function to get value from dictionary target_point
def get_target_points(task):
    global target_points
    return target_points[task]


def restore_trajectory(image, prev_point, point, color, width):
    """Function for restoring trajectory if robot was not recognized"""
    cv2.line(image, prev_point, point, color, width)


def draw_trajectory(image, points, color, width, restore):
    """Function for drawing point trajectory"""
    prev_point = None
    for point in points:
        cv2.circle(image, point, width, color, -1)
        if restore and prev_point is not None and math.sqrt(
                (prev_point[0] - point[0]) ** 2 + (prev_point[1] - point[1]) ** 2) > 1:
            restore_trajectory(image, prev_point, point, color, int(width * 2))
        prev_point = point


def sandbox(robot, image, td: dict, user_code=None):
    """Drawing trajectory at lesson Drawing"""

    # init result dictionary
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }

    text = "Not recognized"
    # init testData
    if not td:
        td = {
            "end_time": time.time() + 60,
            'trajectory': []
        }
    image = robot.draw_info(image)
    # get robot position in pixels
    info = robot.get_info()
    robot_position_px = info['position_px']
    robot_position = info['position']
    # if robot found on the image then add point to trajectory
    if robot_position is not None:
        td['trajectory'].append(robot_position_px)
        text = f'Robot position: x: {robot_position[0]:0.1f} y: {robot_position[1]:0.1f}'
    # draw trajectory
    if len(td['trajectory'])>0:
        draw_trajectory(image, td['trajectory'], (255, 0, 0), 3, True)
    
    # get message from the robot
    msg = robot.get_msg()
    if msg is not None:
        text = f"Message received: {msg}"

    return image, td, text, result
