import cv2
import math
import time


def delta_points(point_0, point_1):
    return math.sqrt(((point_0[0] - point_1[0]) ** 2) +
                     ((point_0[1] - point_1[1]) ** 2))

# start points for the tasks
target_points = {
    'test_drive': [(35, 50), (30, 0)],
    'license_to_drive': [(35, 50), (30, 0)],
    'sandbox': [(50, 50), (30, 0)]
}

# The dictionary specifies the disabled movement functions of the library. This is necessary to prevent cheating.  
# For example, if the task is to write a function for robot movement, the user might attempt 
# to call a library function directly.
# However, these functions will be disabled if the corresponding value in the dictionary is set to `True`.
block_library_functions = {
    'test_drive': False,
    'license_to_drive': False,
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


def test_drive(robot, image, td: dict):
    """Test for lesson 1: Test drive"""

    # init result dictionary
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    # init test data dictionary
    if not td:
        td = {
            "end_time": time.time() + 10,
            'time_for_task': 3,
            "prev_robot_center": None
        }

    robot_position = robot.get_info()["position"]

    text = "Not recognized"
    image = robot.draw_info(image)

    # check if robot position is not none and previous robot is not none
    if  td["prev_robot_center"] is not None and robot_position is not None:
        # calculate delta position
        delta_pos = delta_points(robot_position, td["prev_robot_center"])
        
        text = f'Robot position: x: {robot_position[0]:0.1f} y: {robot_position[1]:0.1f}'
        # init time when robot started motion
        if 'robot_start_move_time' not in td and delta_pos>0.7:
            td['robot_start_move_time'] = time.time()
            td["end_time"] = time.time() + td['time_for_task'] + 3
        # init time when robot finished motion
        if 'robot_start_move_time' in td and 'robot_end_move_time' not in td and delta_pos<0.7:
            td['robot_end_move_time'] = time.time()

    # check if task failed
    if ('robot_end_move_time' not in td and td["end_time"]-1<time.time()
            ) or ('robot_start_move_time'in td and 'robot_end_move_time' in td and 
            (td['time_for_task']+0.8<td['robot_end_move_time']-td['robot_start_move_time'] 
            or td['robot_end_move_time']-td['robot_start_move_time']<td['time_for_task']-0.8)):

        result["success"] = False
        result["score"] = 0
        # check reason that task failed
        if 'robot_start_move_time' in td and ('robot_end_move_time' not in td or 'robot_end_move_time' in td 
            and td['robot_start_move_time']+td['time_for_task']+0.7<td['robot_end_move_time']):
            result["description"] = 'It is disappointing, but robot failed the task. The robot moved more than it should have.'
        else:
            result["description"] = 'It is disappointing, but robot failed the task. The robot moved less then it should have'
    
    # update previous robot position
    if robot_position:
        td["prev_robot_center"] = robot_position

    return image, td, text, result


def license_to_drive(robot, image, td: dict):
    """Test for lesson 2: License to drive"""
    # init test data dictionary
    if not td:
        td = {
            "end_time": time.time() + 10,
            'time_for_task': 5,
            "prev_robot_center": None
        }

    return test_drive(robot, image, td)


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


def sandbox(robot, image, td: dict):
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
