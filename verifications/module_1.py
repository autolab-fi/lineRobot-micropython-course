import cv2
import math
import time
import os
import numpy as np


target_points = {
    'short_distance_race': [(80, 50), (30, 0)],
    'maneuvering': [(35, 50), (30, 0)],
    'long_distance_race': [(35, 50), (30, 0)],

    # Parking reset / reference position
    'Parking': [(20, 30), (43, 0)],

    # REQUIRED final parking position and angle
    'Parking_final': [(115.3, 55.1), (177, 0)]
}


block_library_functions = {
    'short_distance_race': False,
    'maneuvering': False,
    'long_distance_race': False,
    'Parking':False
}

def get_block_library_functions(task):
    global block_library_functions
    return block_library_functions[task]


# function to get value from dictionary target_point
def get_target_points(task):
    global target_points
    return target_points[task]

def delta_points(point_0, point_1):
    return math.sqrt(((point_0[0] - point_1[0]) ** 2) +
                     ((point_0[1] - point_1[1]) ** 2))


def short_distance_race(robot, image, td: dict):
    """Test for lesson 3: Short distance race"""

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

def maneuvering(robot, image, td: dict):
    """Test for lesson 4: Maneuvering"""

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
                {"left": 90, "right": 0},
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


def long_distance_race(robot, image, td: dict):
    """Test for lesson 5: Long distance race."""

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

    if not td["data"] and robot:
        route = [
            {'forward': 30, 'backward': 0},
            [{'left': 90, 'right': 0}],
            {'forward': 20, 'backward': 0},
            [{'left': 0, 'right': 90}],
            {'forward': 28, 'backward': 0},
            [{'left': 0, 'right': 90}],
            {'forward': 20, 'backward': 0}
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


def Parking(robot, image, td: dict):
    """Lesson 15: Parking verification"""

    result = {
        "success": True,
        "description": "Parking completed successfully",
        "score": 100
    }

    text = "Not recognized"

    # Draw robot info
    image = robot.draw_info(image)

    # Init state
    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 30,
            "parked": False,
            "reset_checked": False
        }

    # ------------------------------
    # 1. Check reset position
    # ------------------------------
    if not td["reset_checked"] and robot:

        expected_pos, expected_ang_tuple = get_target_points("Parking")
        expected_ang = expected_ang_tuple[0]

        real_pos = robot.get_info().get("position")
        real_ang = robot.compute_angle_x()

        if real_pos is not None:
            d = delta_points(real_pos, expected_pos)
            a = abs((real_ang - expected_ang + 180) % 360 - 180)

            text = f"Reset check: dist {d:.1f} cm | angle error {a:.1f}°"

        td["reset_checked"] = True

    # ------------------------------
    # 2. Check final parking target
    # ------------------------------
    final_pos, final_ang_tuple = get_target_points("Parking_final")
    final_ang = final_ang_tuple[0]

    pos = robot.get_info().get("position")

    if pos is not None:
        dist = delta_points(pos, final_pos)
        ang_err = abs((robot.compute_angle_x() - final_ang + 180) % 360 - 180)

        text = f"Distance to parking: {dist:.1f} cm | angle error: {ang_err:.1f}°"

        if dist < 4 and ang_err < 10:
            td["parked"] = True
            td["end_time"] = time.time() + 2

    # ------------------------------
    # 3. Timeout fail
    # ------------------------------
    if time.time() > td["end_time"] and not td["parked"]:
        result["success"] = False
        result["score"] = 0
        result["description"] = (
            f"Robot failed to park. Target: {final_pos} @ {final_ang}°"
        )

    return image, td, text, result



# ---------------------------------------------------------
# TASK DISPATCHER
# ---------------------------------------------------------
# run_task dispatches the active lesson verification
# based on the selected task name

def run_task(task, robot, image, td):
    if task == "Parking":
        return Parking(robot, image, td)

    if task == "short_distance_race":
        return short_distance_race(robot, image, td)
    if task == "maneuvering":
        return maneuvering(robot, image, td)
    if task == "long_distance_race":
        return long_distance_race(robot, image, td)

    return image, td, "Unknown task", {
        "success": False,
        "description": "Task name not recognized",
        "score": 0
    }
