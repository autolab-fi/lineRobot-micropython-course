import cv2
import math
import time
import os
import numpy as np
import re
import ast

target_points = {
    'electric_motors': [(30, 50), (30, 0)],
    'differential_drive': [(30, 50), (30, 0)],
    'defining_functions':[(50, 50), (30, 0)],
    'for_loops': [(50,30),(30,0)],
    'encoder_theory': [(30, 50), (30, 0)],
    'while_loops': [(30, 50), (30, 0)]
}

block_library_functions = {
    'electric_motors': False,
    'differential_drive': False,
    'defining_functions': False,
    'for_loops': False,
    'encoder_theory': False,
    'while_loops': False
}


# Core Functions

def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])

def delta_points(point_0, point_1):
    return math.sqrt(((point_0[0] - point_1[0]) ** 2) +
                     ((point_0[1] - point_1[1]) ** 2))

# Necessary Helper Functions

def closest_node(node, nodes):
    """Find the index of the closest node in a set of nodes"""
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.argmin(dist_2)

def rotate_image(image, angle):
    """Rotate an image by the given angle"""
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


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


# 2.1 electric motors

def electric_motors(robot, image, td: dict, user_code=None):
    """Test for lesson: Electric Motors — robot must reach the flag using run_motor commands"""
    #Values in relation to robot!
    FLAG_X_CM = 115.0
    FLAG_Y_CM = 46.0
    FLAG_THRESHOLD = 10.0

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"

    image = robot.draw_info(image)
    if td is not None and td["data"].get("final_result") is not None:
        return image, td, td["data"]["final_text"], td["data"]["final_result"].copy()

    if not td:
        banned = ["turn_left", "turn_right", "move_forward_distance",
                  "move_backward_distance", "move_forward_seconds", "move_backward_seconds"]
        try:
            tree = ast.parse(user_code or "")
            calls = {node.func.attr for node in ast.walk(tree)
                     if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
        except SyntaxError:
            calls = set()
        found_banned = sorted(calls.intersection(banned))
        required_present = {"run_motors_speed", "stop"}.issubset(calls)

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "data": {
                "reached": False,
                "code_valid": len(found_banned) == 0 and required_present,
                "banned_found": found_banned,
                "flag-coords": (int(FLAG_Y_CM / robot.pixels_to_cm(1)),
                                int(FLAG_X_CM / robot.pixels_to_cm(1))),
                "flag-coords-cm": (FLAG_X_CM, FLAG_Y_CM),
                "stable_position": None,
                "stable_since": time.time(),
                "last_seen": None,
                "at_target": False,
                "stopped": False,
            }
        }

        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "flag_finish.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "flag_finish.jpg")

            flag = cv2.imread(filepath)

            if flag is None:
                print("Warning: flag_finish.jpg not found, using placeholder")
                flag = np.zeros((90, 60, 3), dtype=np.uint8)
                cv2.rectangle(flag, (5, 10), (8, 85), (180, 120, 60), -1)
                cv2.rectangle(flag, (8, 10), (55, 40), (0, 0, 220), -1)
                for row in range(3):
                    for col in range(5):
                        if (row + col) % 2 == 0:
                            cv2.rectangle(flag,
                                        (8 + col*9, 10 + row*10),
                                        (17 + col*9, 20 + row*10),
                                        (255, 255, 255), -1)

            flag = cv2.resize(flag, (int(flag.shape[1]/3), int(flag.shape[0]/3)))
            lower_green = np.array([0, 240, 0])
            upper_green = np.array([50, 255, 50])
            td["data"]["flag-mask"] = cv2.bitwise_not(cv2.inRange(flag, lower_green, upper_green))
            td["data"]["flag"] = flag

        except Exception as e:
            print(f"Error loading or processing image: {e}")
            td["data"]["image_error"] = True

    # draw flag
    if not td["data"].get("image_error", False) and "flag" in td["data"]:
        flag = td["data"]["flag"]
        x_left = int(flag.shape[0]/2)
        x_right = flag.shape[0] - x_left
        y_bottom = int(flag.shape[1]/2)
        y_up = flag.shape[1] - y_bottom
        coords = td["data"]["flag-coords"]

        if (0 <= coords[0] - x_left < image.shape[0] and
            coords[0] + x_right < image.shape[0] and
            0 <= coords[1] - y_bottom < image.shape[1] and
            coords[1] + y_up < image.shape[1]):

            if td["data"]["reached"]:
                result_img = rotate_image(flag, 45)
                mask = cv2.inRange(result_img, (0, 0, 0), (205, 205, 205))
                result_img[mask > 0] = (0, 255, 0)
                cv2.copyTo(result_img, rotate_image(td["data"]["flag-mask"], 45),
                          image[coords[0] - x_left:x_right + coords[0],
                                coords[1] - y_bottom:y_up + coords[1]])
            else:
                cv2.copyTo(flag, td["data"]["flag-mask"],
                          image[coords[0] - x_left:x_right + coords[0],
                                coords[1] - y_bottom:y_up + coords[1]])

    # evaluation — only if code valid
    if td["data"]["code_valid"]:
        position = robot.get_info()["position"]
        if position:
            delta = robot.delta_points(position, td["data"]["flag-coords-cm"])
            now = time.time()
            td["data"]["last_seen"] = now
            anchor = td["data"]["stable_position"]
            if anchor is None or robot.delta_points(position, anchor) > 1.0:
                td["data"]["stable_position"] = tuple(position)
                td["data"]["stable_since"] = now
            td["data"]["at_target"] = delta < FLAG_THRESHOLD
            td["data"]["stopped"] = now - td["data"]["stable_since"] >= 0.75
            if delta < FLAG_THRESHOLD:
                td["data"]["reached"] = True
                text = "The robot has reached target point!"
            else:
                text = f'Distance to target point {delta:0.1f} cm'
    else:
        text = "Use run_motors_speed() and stop(), without high-level navigation."

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Use run_motors_speed() and stop(), without high-level navigation | Score: 0"
            text = "Banned functions detected."
        elif (not td["data"]["at_target"] or not td["data"]["stopped"]
              or td["data"]["last_seen"] is None or time.time() - td["data"]["last_seen"] > 1.5):
            result["success"] = False
            result["score"] = 0
            result["description"] = "Robot must stop within 10 cm of (115, 46) cm | Score: 0"
            text = "Failed to reach target point."
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = "You are amazing! The Robot has reached the target point | Score: 100"
            text = "The robot has reached target point!"

        td["data"]["final_result"] = result.copy()
        td["data"]["final_text"] = text

    return image, td, text, result


# 2.2 differential drive

def differential_drive(robot, image, td, user_code=None):
    """Verification function for driving straight assignment"""

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Drive the robot in a straight line for 3 seconds"

    image = robot.draw_info(image)
    if td is not None and td["data"].get("final_result") is not None:
        return image, td, td["data"]["final_text"], td["data"]["final_result"].copy()

    if not td:
        banned = ["move_forward_distance", "move_forward_speed_distance", "move_forward_seconds",
                  "move_backward_distance", "move_backward_seconds", "turn_left", "turn_right"]
        try:
            tree = ast.parse(user_code or "")
            calls = {n.func.attr for n in ast.walk(tree)
                     if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        except SyntaxError:
            calls = set()
        found_banned = sorted(calls.intersection(banned))
        required_present = {"run_motor_left", "run_motor_right"}.issubset(calls) and (
            "stop" in calls or {"stop_motor_left", "stop_motor_right"}.issubset(calls))

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "data": {
                "code_valid": len(found_banned) == 0 and required_present,
                "banned_found": found_banned,
                "task-failed": "",
                "failed-cone": {},
                "direction_0": None,
                "prev_robot_position": None,
                "prev_sample_time": None,
                "first_still_time": None,
                "last_seen": None,
                "settled": False,
                "robot_start_move_time": None,
                "robot_end_move_time": None,
                "max_angle_deviation": 0,
                "straight_driving_start": None,
                "straight_driving_duration": 0,
                "cones-coords": [],
            }
        }

        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "traffic-sign.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "traffic-sign.jpg")

            if not os.path.exists(filepath):
                print("Warning: traffic-sign.jpg not found, using placeholder")
                cone = np.ones((100, 100, 3), dtype=np.uint8) * 255
                pts = np.array([[50, 5], [95, 95], [5, 95]], np.int32)
                cv2.fillPoly(cone, [pts], (0, 100, 255))
                cv2.polylines(cone, [pts], True, (0, 0, 0), 2)
                cv2.line(cone, (27, 65), (73, 65), (255, 255, 255), 6)
            else:
                cone = cv2.imread(filepath)
                cone = cv2.resize(cone, (int(cone.shape[1]), int(cone.shape[0])))

            lower_green = np.array([0, 240, 0])
            upper_green = np.array([35, 255, 35])
            td["data"]["cone-mask"] = cv2.bitwise_not(cv2.inRange(cone, lower_green, upper_green))
            td["data"]["cone"] = cone

        except Exception as e:
            print(f"Error initializing drive straight test: {e}")
            td["data"]["image_error"] = True

    if not td["data"]["code_valid"]:
        text = f"Banned functions detected: {', '.join(td['data']['banned_found'])}"

    # set up cone corridor
    if robot and robot.position_px and len(td["data"].get("cones-coords", [])) == 0:
        y_u = robot.position_px[1] - 150
        y_d = robot.position_px[1] + 150
        for i in range(10):
            x = robot.position_px[0] + (i % 5) * 200
            if i < 5:
                td["data"]["cones-coords"].append((y_u, x))
            else:
                td["data"]["cones-coords"].append((y_d, x))

        if td["data"]["direction_0"] is None:
            td["data"]["direction_0"] = robot.compute_angle_x()
            if td["data"]["direction_0"] > 180:
                td["data"]["direction_0"] -= 360

    # draw cones
    if "cones-coords" in td["data"] and "cone" in td["data"] and len(td["data"]["cones-coords"]) > 0:
        try:
            cone = td["data"]["cone"]
            x_left = int(cone.shape[0] / 2)
            x_right = cone.shape[0] - x_left
            y_bottom = int(cone.shape[1] / 2)
            y_up = cone.shape[1] - y_bottom

            for i in range(min(10, len(td["data"]["cones-coords"]))):
                coords = td["data"]["cones-coords"][i]
                if (0 <= coords[0] - x_left < image.shape[0] and
                    coords[0] + x_right < image.shape[0] and
                    0 <= coords[1] - y_bottom < image.shape[1] and
                    coords[1] + y_up < image.shape[1]):

                    if i in td["data"]["failed-cone"]:
                        result_img = rotate_image(cone, td["data"]["failed-cone"][i])
                        cv2.copyTo(
                            result_img,
                            rotate_image(td["data"]["cone-mask"], td["data"]["failed-cone"][i]),
                            image[coords[0] - x_left:x_right + coords[0],
                                 coords[1] - y_bottom:y_up + coords[1]]
                        )
                        if td["data"]["failed-cone"][i] > -89:
                            td["data"]["failed-cone"][i] -= 45
                    else:
                        cv2.copyTo(
                            cone,
                            td["data"]["cone-mask"],
                            image[coords[0] - x_left:x_right + coords[0],
                                 coords[1] - y_bottom:y_up + coords[1]]
                        )
        except Exception as e:
            print(f"Error drawing cones: {e}")

    # Bound movement by the adjacent stationary samples. Measuring only between
    # moving samples loses up to two camera frame intervals from a 3 s pulse.
    now = time.time()
    if td["data"]["code_valid"] and robot and robot.position is not None:
        data = td["data"]
        data["last_seen"] = now
        angle_x = robot.compute_angle_x()
        if data["direction_0"] is not None:
            angle_diff = abs((angle_x - data["direction_0"] + 180) % 360 - 180)
            data["max_angle_deviation"] = max(data["max_angle_deviation"], angle_diff)
            previous = data["prev_robot_position"]
            if previous is not None:
                moved = robot.delta_points(robot.position, previous) > 0.5
                if moved and not data["settled"]:
                    if data["robot_start_move_time"] is None:
                        data["robot_start_move_time"] = data["prev_sample_time"]
                    data["first_still_time"] = None
                    data["straight_driving_duration"] = now - data["robot_start_move_time"]
                elif data["robot_start_move_time"] is not None and not data["settled"]:
                    if data["first_still_time"] is None:
                        data["first_still_time"] = now
                    if now - data["first_still_time"] >= 0.6:
                        data["settled"] = True
                        data["straight_driving_duration"] = data["first_still_time"] - data["robot_start_move_time"]
                if data["robot_start_move_time"] is not None and angle_diff > 10:
                    data["task-failed"] = f"Robot deviated {angle_diff:.1f}° (max allowed: 10°)"
            data["prev_robot_position"] = tuple(robot.position)
            data["prev_sample_time"] = now
            text = f"Straight: {data['straight_driving_duration']:.1f}/3.0s, Deviation: {angle_diff:.1f}°"

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Use both raw motor functions and stop the motors, without high-level navigation. | Score: 0"
            text = "Banned functions detected."
        elif td["data"]["task-failed"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = td["data"]["task-failed"] + " | Score: 0"
            text = "Failed: " + td["data"]["task-failed"]
        elif td["data"].get("robot_start_move_time") is None:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Robot didn't start moving | Score: 0"
            text = "Robot didn't start moving."
        elif not td["data"]["settled"] or td["data"]["last_seen"] is None or now - td["data"]["last_seen"] > 1.5:
            result = {"success": False, "score": 0, "description": "Stop the robot in camera view after driving straight. | Score: 0"}
            text = "Final stop not confirmed."
        elif td["data"]["straight_driving_duration"] >= 3.0:
            result["success"] = True
            result["score"] = 100
            result["description"] = (
                f"Success! Robot drove straight for {td['data']['straight_driving_duration']:.1f}s "
                f"with max deviation of {td['data']['max_angle_deviation']:.1f}° | Score: 100"
            )
            text = f"Success! Drove straight for {td['data']['straight_driving_duration']:.1f}s"
        else:
            result["success"] = False
            result["score"] = 0
            result["description"] = (
                f"Robot only drove straight for {td['data']['straight_driving_duration']:.1f}s "
                f"(need 3.0s) | Score: 0"
            )
            text = f"Only {td['data']['straight_driving_duration']:.1f}s straight, need 3.0s."

        td["data"]["final_result"] = result.copy()
        td["data"]["final_text"] = text

    return image, td, text, result


# 2.3 defining functions

def defining_functions(robot, image, td: dict, user_code=None):
    """Test: Robot must turn 180 degrees using a defined function."""

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100,
    }
    text = "Waiting..."

    image = robot.draw_info(image)
    if td is not None and td["data"].get("final_result") is not None:
        return image, td, td["data"]["final_text"], td["data"]["final_result"].copy()

    if not td:
        banned = ["turn_left", "turn_right", "move_forward_distance",
                  "move_backward_distance", "move_forward_seconds", "move_backward_seconds"]
        try:
            tree = ast.parse(user_code or "")
            methods = {node.func.attr for node in ast.walk(tree)
                       if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
            definitions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
            calls = {node.func.id for statement in tree.body if not isinstance(statement, ast.FunctionDef)
                     for node in ast.walk(statement)
                     if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
            valid_function = bool(definitions & calls)
            valid_motors = ('run_motors_speed' in methods or {'run_motor_left', 'run_motor_right'}.issubset(methods)) and 'stop' in methods
        except SyntaxError:
            methods = set()
            valid_function = valid_motors = False
        found_banned = sorted(method for method in methods if any(method.startswith(name) for name in banned))

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "target_ang": None,  # set lazily once robot is detected
            "data": {
                "code_valid": len(found_banned) == 0 and valid_function and valid_motors,
                "banned_found": found_banned,
            }
        }

    # set target_ang lazily on first robot detection
    ang = robot.compute_angle_x()
    if ang is not None and td["target_ang"] is None:
        td["target_ang"] = ang + 180 if ang < 180 else ang - 180

    delta_ang = abs((ang - td["target_ang"] + 180) % 360 - 180) if ang is not None and td["target_ang"] is not None else None

    if not td["data"]["code_valid"]:
        text = f"Banned functions detected: {', '.join(td['data']['banned_found'])}"
    elif delta_ang is None:
        text = "Waiting for robot detection..."
    else:
        text = f"Robot must turn to: {delta_ang:0.0f}°"

        if delta_ang < 10:
            if "confirm_start" not in td["data"]:
                td["data"]["confirm_start"] = time.time()
            elif time.time() - td["data"]["confirm_start"] > 1.0:
                result["success"] = True
                result["score"] = 100
                result["description"] = "You are amazing! The Robot has completed the assignment | Score: 100"
                text = "Target angle reached!"
        else:
            if "confirm_start" in td["data"]:
                del td["data"]["confirm_start"]

    # timeout / final verdict
    if (td["end_time"] - time.time()) < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Define and call a function using manual motor control and stop(); high-level navigation is not allowed | Score: 0"
            text = "Banned functions detected."
        elif delta_ang is None:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Robot not detected in camera frame | Score: 0"
            text = "Robot not detected."
        elif delta_ang < 10 and time.time() - td["data"].get("confirm_start", time.time()) >= 1.0:
            result["success"] = True
            result["score"] = 100
            result["description"] = "You are amazing! The Robot has completed the assignment | Score: 100"
            text = "Target angle reached!"
        else:
            result["success"] = False
            result["score"] = 0
            result["description"] = f"Robot did not turn 180 degrees. Final error: {delta_ang:0.0f}° | Score: 0"
            text = "Failed to reach target angle."

        td["data"]["final_result"] = result.copy()
        td["data"]["final_text"] = text

    return image, td, text, result


# 2.4 for loops

def for_loops(robot, image, td: dict, user_code=None):
    """Verification for lesson: For Loops / Drawing trajectory"""

    TASK_DURATION = 60
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
            "end_time": time.time() + 60,
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


# 2.5 encoder theory

def encoder_theory(robot, frame, td, user_code=None):
    """Verification function for encoder theory task.
    Checks: math import, encoder resets, math.pi, printed encoder value 310-360°,
    printed distance in expected range, AND physical displacement matches.

    Use the wheel radius specified in the HAMK lesson: 3.21 cm.
    """

    # ===== CONFIGURATION =====
    WHEEL_RADIUS = 3.21      # HAMK lesson formula; do not copy another robot's radius
    ENCODER_MIN = 310       # minimum acceptable encoder degrees
    ENCODER_MAX = 360       # maximum acceptable encoder degrees

    # Allow rounding around the configured radius and encoder interval.
    DISTANCE_MIN = ENCODER_MIN / 360 * 2 * math.pi * WHEEL_RADIUS - 0.4
    DISTANCE_MAX = ENCODER_MAX / 360 * 2 * math.pi * WHEEL_RADIUS + 0.4

    # Physical displacement bounds (slightly wider tolerance for measurement error)
    DISPLACEMENT_MIN = 16.5 # NEW: OpenCV physical measurement lower bound
    DISPLACEMENT_MAX = 22.0 # NEW: OpenCV physical measurement upper bound

    TASK_DURATION = 20      # seconds
    # =========================

    # ===== 0. INITIAL RESULT TEMPLATE =====
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Reading encoder data..."

    # ===== 1. FIRST-RUN INITIALIZATION =====
    if not td:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        missing = []
        if 'import math' not in active_code and 'from math' not in active_code:
            missing.append('math library')
        if 'reset_left_encoder' not in active_code:
            missing.append('reset_left_encoder()')
        if 'reset_right_encoder' not in active_code:
            missing.append('reset_right_encoder()')
        if 'math.pi' not in active_code:
            missing.append('math.pi')

        td = {
            "start_time": time.time(),
            "end_time": time.time() + TASK_DURATION,
            "data": {
                "completed": False,
                "code_valid": len(missing) == 0,
                "missing": missing,
                "encoder_left": None,
                "encoder_right": None,
                "telemetry_tail": "",
                "distance": None,
                "start_position": None,
                "end_position": None,
            }
        }

    # ===== 2. STATE LOCK =====
    if td["data"].get("completed", False):
        frame = robot.draw_info(frame)
        return frame, td, td["data"].get("final_text", text), td["data"].get("final_result", result)

    # ===== 3. DRAW OVERLAY =====
    frame = robot.draw_info(frame)

    # ===== 4. CODE VALIDATION CHECK =====
    if not td["data"]["code_valid"]:
        text = f"Missing: {', '.join(td['data']['missing'])}"

    # ===== 5. TRACK PHYSICAL DISPLACEMENT =====
    # Always track regardless of code validity
    pos = robot.position
    if pos is not None:
        if td["data"]["start_position"] is None:
            td["data"]["start_position"] = pos
        td["data"]["end_position"] = pos

    # ===== 6. PARSE MQTT MESSAGES =====
    # Matches student template print format:
    # print("Encoder degrees left:", left_deg)
    # print("Distance in cm:", distance)
    for _ in range(64):
        msg = robot.get_msg()
        if msg is None:
            break
        combined = td["data"]["telemetry_tail"] + str(msg)
        for match in re.finditer(r"Encoder degrees (left|right):\s*(-?\d+(?:\.\d+)?)|Distance in cm:\s*(-?\d+(?:\.\d+)?)", combined):
            if match.group(1):
                td["data"]["encoder_" + match.group(1)] = float(match.group(2))
            else:
                td["data"]["distance"] = float(match.group(3))
        td["data"]["telemetry_tail"] = combined[-512:]

    # Show live readings on overlay
    if td["data"]["encoder_left"] is not None:
        text = (f"Left: {td['data']['encoder_left']:.0f}° "
                f"Dist: {td['data']['distance'] or 0:.2f}cm")

    # ===== 7. TIMEOUT / FINAL EVALUATION =====
    # All failure cases handled here — completed=True always set before success=False
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed", False):
        td["data"]["completed"] = True

        if not td["data"]["code_valid"]:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = f"Missing required elements: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."

        else:
            left = td["data"]["encoder_left"]
            right = td["data"]["encoder_right"]
            distance = td["data"]["distance"]
            start = td["data"]["start_position"]
            end = td["data"]["end_position"]

            # Cross-check: expected distance from encoder using correct formula
            expected = (left / 360) * (2 * math.pi * WHEEL_RADIUS) if left else None

            if left is None:
                result["success"] = False
                result["score"] = 0
                result["description"] = "No encoder data received | Score: 0"
                text = "No encoder data received."

            elif not (ENCODER_MIN <= left <= ENCODER_MAX):
                result["success"] = False
                result["score"] = 0
                result["description"] = (
                    f"Encoder value out of range. "
                    f"Left: {left:.0f}° "
                    f"(need {ENCODER_MIN}-{ENCODER_MAX}°) | Score: 0"
                )
                text = "Encoder value out of range."

            elif right is None or not (ENCODER_MIN <= right <= ENCODER_MAX):
                result = {"success": False, "score": 0,
                          "description": f"Print the right encoder after stopping; both encoders must be {ENCODER_MIN}-{ENCODER_MAX} degrees. Right: {right} | Score: 0"}
                text = "Right encoder missing or out of range."
            elif distance is None:
                result["success"] = False
                result["score"] = 0
                result["description"] = "No distance calculation received | Score: 0"
                text = "Distance not printed."

            elif distance < DISTANCE_MIN or distance > DISTANCE_MAX or abs(distance - expected) > 0.3:
                result["success"] = False
                result["score"] = 0
                result["description"] = (
                    f"Distance out of range: {distance:.2f}cm "
                    f"(expected {DISTANCE_MIN:.1f}-{DISTANCE_MAX:.1f}cm based on R={WHEEL_RADIUS}cm) | Score: 0"
                )
                text = "Distance calculation incorrect."

            elif start is None or end is None:
                result["success"] = False
                result["score"] = 0
                result["description"] = "Robot not detected in camera frame | Score: 0"
                text = "Robot not detected."

            else:
                displacement = robot.delta_points(start, end)
                if displacement < DISPLACEMENT_MIN or displacement > DISPLACEMENT_MAX:
                    result["success"] = False
                    result["score"] = 0
                    result["description"] = (
                        f"Physical movement mismatch: robot moved {displacement:.1f}cm "
                        f"but printed distance was {distance:.2f}cm "
                        f"(expected from encoder: {expected:.2f}cm) | Score: 0"
                    )
                    text = "Movement does not match printed values."
                else:
                    result["success"] = True
                    result["score"] = 100
                    result["description"] = (
                        f"Left encoder: {left:.0f}° "
                        f"Printed distance: {distance:.2f}cm "
                        f"Expected: {expected:.2f}cm "
                        f"Physical displacement: {displacement:.1f}cm | Score: 100"
                    )
                    text = "Encoder task complete!"

        td["data"]["final_result"] = result
        td["data"]["final_text"] = text

    return frame, td, text, result


# 2.6 while loops

def while_loops(robot, frame, td, user_code=None):
    """
    Verification: Don't Hit the Wall
    - Wall hit determined by physical displacement (OpenCV)
    - Score determined by encoder-derived distance

    UPDATED: New wheel radius = 3.21cm (changed from 3.4cm)
    """

    TASK_DURATION      = 15
    TARGET_DISTANCE_CM = 20.0
    SUCCESS_MIN_CM     = 18.0
    R                  = 3.21  # NEW: Updated wheel radius (was 3.4)
    ENCODER_SANITY_CAP = 2000
    WALL_VISUAL_OFFSET = 150
    BANNED_FUNCTIONS   = ["move_forward", "move_backward", "move_forward_distance",
                          "move_backward_distance", "move_forward_seconds", "move_backward_seconds"]

    result = {
        "success": True,
        "description": "You are amazing! Robot stopped before the wall.",
        "score": 100
    }
    text = "Waiting..."

    frame = robot.draw_info(frame)

    if td is None:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        found_banned = [f for f in BANNED_FUNCTIONS if f in active_code]

        td = {
            "start_time": time.time(),
            "end_time": time.time() + TASK_DURATION,
            "start_position": None,
            "wall_px": None,
            "data": {
                "wall_hit": False,
                "code_valid": len(found_banned) == 0,
                "banned_found": found_banned,
                "encoder_left": None,
                "peak_displacement": 0.0,
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Banned functions detected: {', '.join(td['data']['banned_found'])}"

    # capture start position and derive wall pixel x
    pos    = robot.position
    pos_px = robot.position_px

    if td["start_position"] is None and pos is not None and pos_px is not None:
        td["start_position"] = pos
        if pos[0] != 0:
            px_per_cm = pos_px[0] / pos[0]
            td["wall_px"] = int(pos_px[0] + TARGET_DISTANCE_CM * px_per_cm + WALL_VISUAL_OFFSET)

    # parse MQTT messages
    msg = robot.get_msg()
    if msg is not None:
        try:
            val = float(msg.strip().split(":")[-1].strip())
            if val < ENCODER_SANITY_CAP:
                td["data"]["encoder_left"] = val
        except (ValueError, IndexError):
            pass

    # track displacement and wall hit
    if td["start_position"] is not None and pos is not None:
        dx = pos[0] - td["start_position"][0]
        dy = pos[1] - td["start_position"][1]
        displacement = math.sqrt(dx**2 + dy**2)

        if displacement > td["data"]["peak_displacement"]:
            td["data"]["peak_displacement"] = displacement

        enc = td["data"]["encoder_left"] or 0
        text = f"Displacement: {displacement:.1f}cm | Encoder: {enc:.0f}°"

        if td["data"]["peak_displacement"] >= TARGET_DISTANCE_CM:
            td["data"]["wall_hit"] = True
            text = f"WALL HIT! Displacement: {displacement:.1f}cm | Encoder: {enc:.0f}°"

    # draw wall line
    if td["wall_px"] is not None:
        wall_color = (0, 0, 255) if td["data"]["wall_hit"] else (0, 0, 0)
        cv2.line(frame, (td["wall_px"], 0), (td["wall_px"], frame.shape[0]), wall_color, 3)

    # timeout / final verdict
    if time.time() > td["end_time"]:
        enc      = td["data"]["encoder_left"]
        peak_disp = td["data"]["peak_displacement"]
        enc_dist = (enc / 360) * (2 * math.pi * R) if enc is not None else None

        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = (f"Banned functions used: "
                                     f"{', '.join(td['data']['banned_found'])} | Score: 0")
            text = "Banned functions detected."
        elif enc is None:
            result["success"] = False
            result["score"] = 0
            result["description"] = "No encoder data received. Did you print inside the loop? | Score: 0"
            text = "No encoder data received."
        elif td["data"]["wall_hit"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = (f"Robot hit the wall! "
                                     f"Encoder distance: {enc_dist:.1f}cm | "
                                     f"Final displacement (with drift): {peak_disp:.1f}cm | Score: 0")
            text = "WALL HIT!"
        elif enc_dist < SUCCESS_MIN_CM:
            result["success"] = False
            result["score"] = 50
            result["description"] = (f"Stopped too early — "
                                     f"Encoder distance: {enc_dist:.1f}cm | "
                                     f"Final displacement: {peak_disp:.1f}cm | Score: 50")
            text = "Stopped too short."
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = (f"Stopped in the zone! "
                                     f"Encoder distance: {enc_dist:.1f}cm | "
                                     f"Final displacement: {peak_disp:.1f}cm | Score: 100")
            text = "Stopped in the zone!"

    return frame, td, text, result