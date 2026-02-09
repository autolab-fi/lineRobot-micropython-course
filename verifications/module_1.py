import cv2
import math
import time
import os
import numpy as np
import re


target_points = {
    'welcome': [(35, 50), (30, 0)],
    'test_drive': [(35, 50), (30, 0)],
    'license_to_drive': [(35, 50), (30, 0)],
    'directional_movement': [(80, 50), (30, 0)],
    'python_variables_commands': [(80, 50), (30, 0)],
    'maneuvering': [(35, 50), (30, 0)],
    'sequential_navigation': [(35, 60), (30, 0)],
}

block_library_functions = {
    'welcome': False,
    'test_drive': False,
    'license_to_drive': False,
    'directional_movement': False,
    'python_variables_commands': False,
    'maneuvering': False,
    'sequential_navigation': False,
}

def get_block_library_functions(task):
    global block_library_functions
    return block_library_functions[task]


# function to get value from dictionary target_point
def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])

def delta_points(point_0, point_1):
    return math.sqrt(((point_0[0] - point_1[0]) ** 2) +
                     ((point_0[1] - point_1[1]) ** 2))

def welcome(robot, image, td: dict, user_code=None):
    """Test for Mission 1.1 Welcome"""
    result = {
        "success": True,
        "description": "Connection established! System check complete.",
        "score": 100
    }

    if not td:
        td = {"start_time": time.time(), "end_time": time.time() + 2}

    if time.time() > td["end_time"]:
        return image, td, "Link: Stable", result
    
    return image, td, "Checking connection...", result


def test_drive(robot, image, td: dict, user_code=None):
    """Test for Mission 1.2 Test drive"""

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

def license_to_drive(robot, image, td: dict, user_code=None):
    """Test for Mission 1.3 License to drive"""
    # init test data dictionary
    if not td:
        td = {
            "end_time": time.time() + 10,
            'time_for_task': 5,
            "prev_robot_center": None
        }

    return test_drive(robot, image, td)

def directional_movement(robot, image, td: dict, user_code=None):
    """Test for Mission 1.4 Directional Movement"""

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"
    image = robot.draw_info(image)
    # Initialize the dictionary with consistent structure
    if not td:
        td = {
            "end_time": time.time() + 20,
            "prev_robot_center": None,
            "goal": {
                "forward": 20,   
                "backward": 35   
            }
        }

    # Get the current robot position
    robot_position = robot.get_info()["position"]
    
    if td["prev_robot_center"] is not None and robot_position is not None:
        delta_pos = delta_points(robot_position, td["prev_robot_center"])
        text = f'Robot position: x: {robot_position[0]:0.1f} y: {robot_position[1]:0.1f}'

        # Calculate the angle for direction
        ang = robot.compute_angle_robot_point(td["prev_robot_center"])
        
        direction = 'unknown'
        if 170 < ang < 190: 
            direction = 'forward'
        elif 350 < ang or ang < 10:
            direction = 'backward'

        # Adjust goal distances based on the movement direction
        if direction != 'unknown':
            td["goal"][direction] -= delta_pos

        # Check for task completion and add extra time if needed
        if td['goal']['forward'] <= 3 and td['goal']['backward'] <= 3 and (td["end_time"] - time.time()) > 3:
            td["end_time"] = time.time() + 3

    # Check for task failure conditions
    if (
        (td['goal']['forward'] < 15 and td['goal']['backward'] > 5) or
        td['goal']['forward'] < -5 or td['goal']['backward'] < -5 or
        (td["end_time"] - time.time() <= 2 and (td['goal']['backward'] > 5 or td['goal']['forward'] > 5))
    ):
        result["success"] = False
        result["score"] = 0
        backward = 35 - td['goal']['backward']
        forward = 20 - td['goal']['forward']
        result["description"] = (
            f'Robot failed the task, moved {forward:.1f} cm forward, {backward:.1f} cm backward | Score: {result["score"]}'
        )

    # Store the previous robot position
    td['prev_robot_center'] = robot_position

    return image, td, text, result

def python_variables_commands(robot, image, td: dict, user_code):
    """Test for Mission 1.5 Python Variables & Commands"""
    
    if not td:
        td = {
            "end_time": time.time() + 25,
            "prev_robot_center": None,
            "goal": {"forward": 15, "backward": 20.5}
        }

    # Physical movement check
    image, td, text, move_result = directional_movement(robot, image, td)

    # Code style check
    has_float = re.search(r"=\s*\d+\.\d+", user_code)
    has_int = re.search(r"=\s*\d+", user_code)
    has_plus = "+" in user_code
    has_print = "print" in user_code
    code_is_correct = has_float and has_int and has_plus and has_print

    # Final judgment logic
    time_up = time.time() > td["end_time"]
    movement_done = (td['goal']['forward'] <= 3 and td['goal']['backward'] <= 3)

    # If physical task is finished or time is out, check the code style
    if movement_done or time_up:
        if not code_is_correct:
            move_result.update({
                "success": False,
                "score": 0,
                "description": "Task failed. Use variables (int, float), '+' and print()."
            })
            # Return current position (text) along with the error
            return image, td, text, move_result
        
    return image, td, text, move_result

def maneuvering(robot, image, td: dict, user_code): 
    """Test for Mission 1.6 Maneuvering"""

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100  
    }
    text = "Not recognized"
    image = robot.draw_info(image)
    # Initialize the task dictionary
    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 20,
            "target_angle": [
                {"left": 145, "right": 0},
                {"left": 90, "right": 0},
                {"left": 0, "right": 90}
            ]
        }

    min_for_error = 15
    min_for_change_point = 10

    if robot is not None:
        # ✅ FIX: Removed the extra argument
        ang = robot.compute_angle_x()

        if 'ang_0' in td:
            if td['ang_0'] < 90 and ang > 300:
                td['ang_0'] = 360 + td['ang_0']
            elif td['ang_0'] > 300 and ang < 90:
                td['ang_0'] -= 360

            delta_ang = ang - td['ang_0']

            if delta_ang < 0:
                td['target_angle'][-1]['right'] += delta_ang
            else:
                td['target_angle'][-1]['left'] -= delta_ang

        if (
            td['target_angle'][-1]['left'] < min_for_change_point and
            td['target_angle'][-1]['right'] < min_for_change_point
        ):
            if len(td['target_angle']) > 1:
                td['target_angle'].pop()
            elif td["end_time"] - td["start_time"] == 12:
                td["end_time"] = time.time() + 1

        text = f"Current angle with x-axis: {ang:0.0f}"
        td['ang_0'] = ang

    # Code style check
    style_ok = True
    param_match = re.search(r"turn_left_angle\s*\(\s*([^)]+)\s*\)", user_code)
    if param_match:
        param = param_match.group(1).strip()
        if re.match(r"^\d+\.?\d*$", param): # If only digits
            style_ok = False
    else:
        style_ok = False

    if (
        td['target_angle'][-1]['left'] < -min_for_error or
        td['target_angle'][-1]['right'] < -min_for_error or
        (
            td['end_time'] - time.time() < 2 and
            (
                td['target_angle'][0]['right'] > min_for_error or
                td['target_angle'][0]['left'] > min_for_error
            )
        )
    ):
        result["success"] = False
        result["score"] = 0 
        result["description"] = (
            f"It is disappointing, but robot failed the task. "
            f"The robot had to turn more: "
        )

        for i in range(len(td['target_angle']) - 1, -1, -1):
            if abs(td['target_angle'][i]['right']) > min_for_change_point:
                result["description"] += (
                    f"{int(td['target_angle'][i]['right'])} degrees right; "
                )
            if abs(td['target_angle'][i]['left']) > min_for_change_point:
                result["description"] += (
                    f"{int(td['target_angle'][i]['left'])} degrees left; "
                )

    if result["success"] and not style_ok:
        result["success"] = False
        result["score"] = 0
        result["description"] = "Task failed. Use a variable for the 145 degree turn."

    result["description"] += f' | Score: {result["score"]}'  
    return image, td, text, result

def calculate_target_point(rb, targets):
    """Calculate the target points based on the robot's current position and movement directions."""
    
    # Get the robot's position properly
    pos = rb.get_info().get("position")
    
    if pos is None:
        print("Error: Robot position is None")
        return []

    point = [pos[0], pos[1]]
    direction = rb.compute_angle_x()

    res = []
    for target in targets:
        if isinstance(target, dict):
            point[0] += target['forward'] * math.cos(math.radians(direction))
            point[0] -= target['backward'] * math.cos(math.radians(direction))
            point[1] -= target['forward'] * math.sin(math.radians(direction))
            point[1] += target['backward'] * math.sin(math.radians(direction))
            res.append((point[0], point[1]))
        else:
            # Handle reversed y-axis
            direction += target[0]['left']
            direction -= target[0]['right']

    res.reverse()
    return res


def sequential_navigation(robot, image, td: dict, user_code): 
    """Test for Mission 1.7 Sequential navigation"""

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"
    image = robot.draw_info(image)

    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 30,
            "data": {},
            "delta": 4,
            "reached_point": False
        }

    # Code style check
    comments_count = user_code.count('#')
    style_ok = comments_count >= 3

    if not td["data"] and robot:
        route = [
            {'forward': 35, 'backward': 0},
            [{'left': 90, 'right': 0}],
            {'forward': 25, 'backward': 0},
            [{'left': 0, 'right': 90}],
            {'forward': 35, 'backward': 0},
            [{'left': 0, 'right': 90}],
            {'forward': 25, 'backward': 0}
        ]

        td["data"]['targets'] = calculate_target_point(robot, route)
        td["data"]['delta'] = 4
        td["data"]['reached_point'] = False

        # Load single mineral image
        basepath = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(basepath, 'images', 'mineral.png')
        
        mineral_img = cv2.imread(filepath)
        
        if mineral_img is None:
            print("Error: Could not load mineral.png")
            td["data"]["mineral"] = None
            td["data"]["mask"] = None
        else:
            # Resize mineral to match original fruit size
            original_height = mineral_img.shape[0]
            original_width = mineral_img.shape[1]
            new_height = int(original_height * 0.2)
            new_width = int(original_width * 0.2)
            mineral_img = cv2.resize(mineral_img, (new_width, new_height))
            
            # Create mask: non-black pixels are visible
            gray = cv2.cvtColor(mineral_img, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
            
            td["data"]["mineral"] = mineral_img
            td["data"]["mask"] = mask
        
        # Track which checkpoints are still visible
        td["data"]["checkpoint_visible"] = [True] * 4
        
        td["data"]['coordinates'] = [
            (robot.cm_to_pixel(x), robot.cm_to_pixel(y)) for x, y in td["data"]['targets']
        ]

    d = None

    if robot:
        robot_position = robot.get_info().get("position")
        if robot_position is not None:
            d = delta_points(robot_position, td["data"]['targets'][-1])
            text = (
                f'The distance to the next ({td["data"]["targets"][-1][0]:0.0f}, '
                f'{td["data"]["targets"][-1][1]:0.0f}) point is {d:0.0f}'
            )

            if d < td["data"]['delta']:
                if len(td["data"]['targets']) > 1:
                    # Mark this checkpoint as collected
                    checkpoint_index = len(td["data"]['targets']) - 1
                    td["data"]["checkpoint_visible"][checkpoint_index] = False
                    
                    td["data"]['delta'] += 1.3
                    td["data"]['targets'].pop()
                elif not td["data"]['reached_point']:
                    # Final checkpoint collected
                    td["data"]["checkpoint_visible"][0] = False
                    td["data"]['reached_point'] = True
                    td["end_time"] = time.time() + 4

    if d is not None and td["end_time"] - time.time() < 2 and (
            len(td["data"]['targets']) != 1 or d > td["data"]['delta']):
        if len(td["data"]['targets']) > 1:
            text = "Robot missed several checkpoints"
        else:
            text = (
                f'It is disappointing, but robot failed the task, '
                f'because it is {d:0.0f} centimeters away from the target point'
            )
        result["description"] = text
        result["success"] = False
        result["score"] = 0

    # Final check
    time_up = time.time() > td["end_time"]
    if td["data"].get('reached_point') or time_up:
        if not style_ok and result["success"]:
            result.update({"success": False, "score": 0, 
                           "description": "Task failed. Use at least 3 comments (#) in your code."})

    # Draw minerals at checkpoint locations with masking
    if td["data"] and td["data"]["mineral"] is not None and td["data"]["mask"] is not None:
        mineral = td["data"]["mineral"]
        mask = td["data"]["mask"]
        
        # Use same positioning as original code
        ymin = mineral.shape[0] // 2
        ymax = mineral.shape[0] - ymin
        xmin = mineral.shape[1] // 2
        xmax = mineral.shape[1] - xmin
        
        for i, (x, y) in enumerate(td["data"]['coordinates']):
            # Only draw if checkpoint is still visible
            if i < len(td["data"]["checkpoint_visible"]) and td["data"]["checkpoint_visible"][i]:
                # Check bounds before drawing
                if (y - ymin >= 0 and y + ymax <= image.shape[0] and 
                    x - xmin >= 0 and x + xmax <= image.shape[1]):
                    # Use cv2.copyTo to apply mask (only non-black pixels)
                    cv2.copyTo(mineral, mask, image[y - ymin:y + ymax, x - xmin:x + xmax])

    return image, td, text, result
