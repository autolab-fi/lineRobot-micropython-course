import cv2
import math
import time
import os
import numpy as np
import re


target_points = {
    'navigation': [(30, 70), (30, 0)],
    'perimeter': [(50, 50), (30, 0)]
}

block_library_functions = {
    'navigation': False,
    'perimeter': False,
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

def draw_trajectory(image, points, color, width, restore):
    """Function for drawing point trajectory"""
    prev_point = None
    for point in points:
        cv2.circle(image, point, width, color, -1)
        if restore and prev_point is not None and math.sqrt(
                (prev_point[0] - point[0]) ** 2 + (prev_point[1] - point[1]) ** 2) > 1:
            restore_trajectory(image, prev_point, point, color, int(width * 2))
        prev_point = point

def restore_trajectory(image, prev_point, point, color, width):
    """Function for restoring trajectory if robot was not recognized"""
    cv2.line(image, prev_point, point, color, width)

# Task 1: Navigation

def navigation(robot, image, td: dict, user_code): 
    """Test for task 1 navigation"""

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
    has_variables = bool(re.search(r'\w+\s*=\s*\d+', user_code))

    style_ok = (comments_count >= 2) and has_variables

    if not td["data"] and robot:
        route = [
            {'forward': 20, 'backward': 0},
            [{'left': 45, 'right': 0}],
            {'forward': 40, 'backward': 0},
            [{'left': 0, 'right': 45}],
            {'forward': 20, 'backward': 0},
            [{'left': 0, 'right': 90}],
            {'forward': 40, 'backward': 0},
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
                           "description": "Task failed. Use variables (e.g., dist = 20) and at least 2 comments (#) in your code."})

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

# Task 2: Perimeter

def perimeter(robot, image, td: dict, user_code=None):
    """Test for task 2 perimeter"""

    TASK_DURATION = 45
    TRAJECTORY_COLOR = (255, 0, 0)
    TRAJECTORY_WIDTH = 3

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"

    image = robot.draw_info(image)

    if not td:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        code_valid = 'for' in active_code

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 45,
            "data": {
                "code_valid": code_valid,
            },
            "trajectory": []
        }

    if not td["data"]["code_valid"]:
        text = "No for loop detected in code"

    # trajectory tracking
    info = robot.get_info()
    robot_position_px = info["position_px"]
    robot_position = info["position"]

    MIN_DIST_PX = 5   # only record a new point if robot moved at least this many pixels

    if robot_position is not None:
        if len(td["trajectory"]) == 0:
            td["trajectory"].append(robot_position_px)
        else:
            last = td["trajectory"][-1]
            dx = robot_position_px[0] - last[0]
            dy = robot_position_px[1] - last[1]
            if (dx**2 + dy**2) ** 0.5 >= MIN_DIST_PX:
                td["trajectory"].append(robot_position_px)
        text = f'Robot position: x: {robot_position[0]:0.1f} y: {robot_position[1]:0.1f}'

    if len(td["trajectory"]) > 0:
        draw_trajectory(image, td["trajectory"], TRAJECTORY_COLOR, TRAJECTORY_WIDTH, True)

    msg = robot.get_msg()
    if msg is not None:
        text = f"Message received: {msg}"

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "No for loop found in code | Score: 0"
            text = "No for loop detected."
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = "You are amazing! The Robot has completed the assignment | Score: 100"
            text = "Trajectory complete!"

    return image, td, text, result