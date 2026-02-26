import cv2
import math
import time
import os
import numpy as np
import re

target_points = {
    # new
    'electric_motors': [(30, 50), (30, 0)],
    'differential_drive': [(30, 50), (30, 0)],
    'defining_functions':[(50, 50), (30, 0)],
    'for_loops': [(50,30),(30,0)],
    'encoder_theory': [(30, 50), (30, 0)],
    'while_loops': [(30, 50), (30, 0)]


    # old
    #'headlights': [(30, 50), (30, 0)],
    #'alarm': [(30, 50), (30, 0)],

}

block_library_functions = {
    # new
    'electric_motors': False,
    'differential_drive': False,
    'defining_functions': False,
    'for_loops': False,
    'encoder_theory': False,
    'while_loops': False

    # old
    #'headlights': False,
    #'alarm': False,
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


#New functions

#2.1 electric motor

def electric_motors(robot, image, td: dict, user_code=None):
    """Test for lesson 8: Electric motor"""

    # ===== CONFIGURATION =====
    FLAG_X = 300        # pixel x coordinate of flag on screen
    FLAG_Y = 400        # pixel y coordinate of flag on screen
    FLAG_THRESHOLD = 7.0  # detection radius in cm
    # =========================

    # ===== 0. INITIAL RESULT TEMPLATE =====
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"

    # ===== 1. FIRST-RUN INITIALIZATION =====
    if not td:
        banned = ["turn_left", "turn_right", "move_forward_distance",
                  "move_backward_distance", "move_forward_seconds", "move_backward_seconds"]
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        found_banned = [f for f in banned if f in active_code]

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "data": {
                "completed": False,
                "reached": False,
                "code_valid": len(found_banned) == 0,
                "banned_found": found_banned,
                "flag-coords": (FLAG_X, FLAG_Y),
                "flag-coords-cm": (robot.pixels_to_cm(FLAG_X), robot.pixels_to_cm(FLAG_Y)),
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
            #return image, td, f"Error processing image: {str(e)}", result

    # ===== 2. STATE LOCK =====
    if td["data"].get("completed", False):
        image = robot.draw_info(image)
        return image, td, td["data"].get("final_text", text), td["data"].get("final_result", result)

    # ===== 3. DRAW OVERLAY =====
    image = robot.draw_info(image)

    # ===== 4. CODE VALIDATION CHECK =====
    # Don't return early — just block evaluation and wait for timeout
    if not td["data"]["code_valid"]:
        text = f"Banned functions detected: {', '.join(td['data']['banned_found'])}"

    # ===== 5. FLAG IMAGE DRAWING =====
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

    # ===== 6. EVALUATION LOOP =====
    # Only runs if code is valid
    if td["data"]["code_valid"]:
        position = robot.get_info()["position"]
        if position and "flag-coords-cm" in td["data"]:
            delta = robot.delta_points((position[1], position[0]), td["data"]["flag-coords-cm"])

            if delta < FLAG_THRESHOLD:
                td["data"]["reached"] = True
                if "confirm_start" not in td["data"]:
                    td["data"]["confirm_start"] = time.time()
                elif time.time() - td["data"]["confirm_start"] > 1.0:
                    td["data"]["completed"] = True
                    result["success"] = True
                    result["score"] = 100
                    result["description"] = "You are amazing! The Robot has reached the target point | Score: 100"
                    text = "The robot has reached target point!"
                    td["data"]["final_result"] = result
                    td["data"]["final_text"] = text
                else:
                    text = "The robot has reached target point!"
            else:
                if "confirm_start" in td["data"]:
                    del td["data"]["confirm_start"]
                text = f'Distance to target point {delta:0.1f} cm'

    # ===== 7. TIMEOUT / FINAL EVALUATION =====
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed", False):
        td["data"]["completed"] = True

        if not td["data"]["code_valid"]:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = f"Banned functions used: {', '.join(td['data']['banned_found'])} | Score: 0"
            text = "Banned functions detected."
        else:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = "Robot did not reach the target point | Score: 0"
            text = "Failed to reach target point."

        td["data"]["final_result"] = result
        td["data"]["final_text"] = text

    return image, td, text, result

# 2.2 differential drive

def differential_drive(robot, image, td, user_code=None):
    """Verification function for driving straight assignment"""

    # ===== 0. INITIAL RESULT TEMPLATE =====
    # CRITICAL: Always start with success=True (platform requirement)
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Drive the robot in a straight line for 3 seconds"

    # ===== 1. FIRST-RUN INITIALIZATION =====
    if not td:
        # Check for banned functions in user code
        banned = ["move_forward_distance", "move_forward_speed_distance", "move_forward_seconds",
                  "move_backward_distance", "move_backward_seconds", "turn_left", "turn_right"]
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        found_banned = [f for f in banned if f in active_code]

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "data": {
                "completed": False,
                "code_valid": len(found_banned) == 0,
                "banned_found": found_banned,
                "task-failed": "",
                "failed-cone": {},
                "direction_0": None,
                "prev_robot_position": None,
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
                # Placeholder cone - orange triangle with white stripe
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

    # ===== 2. STATE LOCK - early return if already completed =====
    if td["data"].get("completed", False):
        image = robot.draw_info(image)
        return image, td, td["data"].get("final_text", text), td["data"].get("final_result", result)

    # ===== 3. DRAW OVERLAY =====
    image = robot.draw_info(image)

    # ===== 4. CODE VALIDATION CHECK =====
    # Don't return failure here — just block evaluation and wait for timeout
    # This way success=False is only set at timeout where completed=True is safe
    if not td["data"]["code_valid"]:
        text = f"Banned functions detected: {', '.join(td['data']['banned_found'])}"

    # ===== 5. SET UP CONE CORRIDOR =====
    # Cones always drawn regardless of code validity
    # Keep retrying until robot position is detected
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

    # ===== 6. DRAW CONES =====
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

    # ===== 7. EVALUATION LOOP =====
    # Only runs if code is valid
    if td["data"]["code_valid"] and robot and robot.position is not None:
        angle_x = robot.compute_angle_x()
        angle_x_disp = angle_x

        if angle_x > 180:
            angle_x -= 360

        if td["data"]["direction_0"] is not None:
            angle_diff = abs(td["data"]["direction_0"] - angle_x)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            td["data"]["max_angle_deviation"] = max(td["data"]["max_angle_deviation"], angle_diff)
            text = f'Robot angle with x: {angle_x_disp:0.0f}°, Deviation: {angle_diff:.1f}°'

            if td["data"]["prev_robot_position"] is not None:
                delta_pos = robot.delta_points(robot.position, td["data"]["prev_robot_position"])

                if td["data"]["robot_start_move_time"] is None and delta_pos > 1:
                    td["data"]["robot_start_move_time"] = time.time()
                    td["data"]["straight_driving_start"] = time.time()
                    text = f"Robot started moving at angle {angle_x_disp:0.0f}°"

                if td["data"]["robot_start_move_time"] is not None and delta_pos > 0.5:
                    if angle_diff <= 10 and td["data"]["straight_driving_start"] is not None:
                        current_time = time.time()
                        td["data"]["straight_driving_duration"] = current_time - td["data"]["straight_driving_start"]

                        if td["data"]["straight_driving_duration"] >= 3.0:
                            # SUCCESS — lock in immediately, no need to wait for timeout
                            td["data"]["completed"] = True
                            result["success"] = True
                            result["score"] = 100
                            result["description"] = (
                                f"Success! Robot drove straight for {td['data']['straight_driving_duration']:.1f}s "
                                f"with max deviation of {td['data']['max_angle_deviation']:.1f}° | Score: 100"
                            )
                            text = f"Success! Robot drove straight for {td['data']['straight_driving_duration']:.1f}s"
                            td["data"]["final_result"] = result
                            td["data"]["final_text"] = text
                        else:
                            text = f"Straight: {td['data']['straight_driving_duration']:.1f}/3.0s, Deviation: {angle_diff:.1f}°"

                    elif angle_diff > 10:
                        td["data"]["straight_driving_start"] = None
                        td["data"]["straight_driving_duration"] = 0

                        if not td["data"]["task-failed"]:
                            td["data"]["task-failed"] = f"Robot deviated {angle_diff:.1f}° (max allowed: 10°)"

                            if robot.position_px is not None and len(td["data"]["cones-coords"]) > 0:
                                min_index = closest_node((robot.position_px[1], robot.position_px[0]),
                                                        td["data"]["cones-coords"])
                                if min_index not in td["data"]["failed-cone"]:
                                    td["data"]["failed-cone"][min_index] = -20

                if td["data"]["robot_start_move_time"] is not None and delta_pos < 0.5:
                    if td["data"]["robot_end_move_time"] is None:
                        td["data"]["robot_end_move_time"] = time.time()
                        if td["data"]["straight_driving_duration"] < 3.0 and not td["data"]["task-failed"]:
                            td["data"]["task-failed"] = (
                                f"Robot only drove straight for {td['data']['straight_driving_duration']:.1f}s (need 3.0s)"
                            )

        td["data"]["prev_robot_position"] = robot.position

    # ===== 8. TIMEOUT / FINAL EVALUATION =====
    # All failure cases handled here — completed=True is always set before success=False
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed", False):
        td["data"]["completed"] = True

        if not td["data"]["code_valid"]:
            # Safe now — completed=True set above
            result["success"] = False
            result["score"] = 0
            result["description"] = f"Banned functions used: {', '.join(td['data']['banned_found'])} | Score: 0"
            text = "Banned functions detected."

        elif td["data"]["task-failed"]:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = td["data"]["task-failed"] + " | Score: 0"
            text = "Failed: " + td["data"]["task-failed"]

        elif td["data"].get("robot_start_move_time") is None:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = "Robot didn't start moving | Score: 0"
            text = "Robot didn't start moving."

        else:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = (
                f"Robot only drove straight for {td['data']['straight_driving_duration']:.1f}s "
                f"(need 3.0s) | Score: 0"
            )
            text = f"Only {td['data']['straight_driving_duration']:.1f}s straight, need 3.0s."

        td["data"]["final_result"] = result
        td["data"]["final_text"] = text

    return image, td, text, result

# 2.3 CHANGED FROM "movement" in module_3

def defining_functions(robot, image, td: dict, user_code=None):
    """Test: Robot must turn 180 degrees."""

    # ===== 0. INITIAL RESULT TEMPLATE =====
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100,
    }
    text = "Waiting..."

    # ===== 1. FIRST-RUN INITIALIZATION =====
    if not td:
        banned = ["turn_left", "turn_right", "move_forward_distance",
                  "move_backward_distance", "move_forward_seconds", "move_backward_seconds"]
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        found_banned = [f for f in banned if f in active_code]

        current_ang = robot.compute_angle_x()
        target_ang = current_ang + 180 if current_ang < 180 else current_ang - 180

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "target_ang": target_ang,
            "data": {
                "completed": False,
                "code_valid": len(found_banned) == 0,
                "banned_found": found_banned,
            }
        }

    # ===== 2. STATE LOCK =====
    if td["data"].get("completed", False):
        image = robot.draw_info(image)
        return image, td, td["data"].get("final_text", text), td["data"].get("final_result", result)

    # ===== 3. DRAW OVERLAY =====
    image = robot.draw_info(image)
    ang = robot.compute_angle_x()
    delta_ang = abs(ang - td["target_ang"])

    # ===== 4. CODE VALIDATION CHECK =====
    # Don't return early — just block evaluation and wait for timeout
    if not td["data"]["code_valid"]:
        text = f"Banned functions detected: {', '.join(td['data']['banned_found'])}"

    # ===== 5. EVALUATION LOOP =====
    # Only runs if code is valid
    if td["data"]["code_valid"]:
        text = f"Robot must turn to: {delta_ang:0.0f}°"

        if delta_ang < 10 and not td["data"]["completed"]:
            if "confirm_start" not in td["data"]:
                td["data"]["confirm_start"] = time.time()
            elif time.time() - td["data"]["confirm_start"] > 1.0:
                td["data"]["completed"] = True
                result["success"] = True
                result["score"] = 100
                result["description"] = "You are amazing! The Robot has completed the assignment | Score: 100"
                text = "Target angle reached!"
                td["data"]["final_result"] = result
                td["data"]["final_text"] = text
        else:
            if "confirm_start" in td["data"]:
                del td["data"]["confirm_start"]

    # ===== 6. TIMEOUT / FINAL EVALUATION =====
    if (td["end_time"] - time.time()) < 1 and not td["data"].get("completed", False):
        td["data"]["completed"] = True

        if not td["data"]["code_valid"]:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = f"Banned functions used: {', '.join(td['data']['banned_found'])} | Score: 0"
            text = "Banned functions detected."
        else:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = f"Robot did not turn 180 degrees. Final error: {delta_ang:0.0f}° | Score: 0"
            text = "Failed to reach target angle."

        td["data"]["final_result"] = result
        td["data"]["final_text"] = text

    return image, td, text, result

# 2.4 "for loops"
# make a drawing board (like in the sandbox, but change the starting point) + checking the code for a loop

def for_loops(robot, image, td: dict, user_code=None):
    """Verification for lesson: For Loops / Drawing trajectory"""

    # ===== CONFIGURATION =====
    TASK_DURATION = 60      # seconds to record trajectory
    TRAJECTORY_COLOR = (255, 0, 0)  # BGR - blue
    TRAJECTORY_WIDTH = 3
    # =========================

    # ===== 0. INITIAL RESULT TEMPLATE =====
    # CRITICAL: Always start with success=True (platform requirement)
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"

    # ===== 1. FIRST-RUN INITIALIZATION =====
    if not td:
        # Check for for loop in user code
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        code_valid = 'for' in active_code

        td = {
            "start_time": time.time(),
            "end_time": time.time() + TASK_DURATION,
            "data": {
                "completed": False,
                "code_valid": code_valid,
            },
            "trajectory": []
        }

    # ===== 2. STATE LOCK - early return if already completed =====
    if td["data"].get("completed", False):
        image = robot.draw_info(image)
        draw_trajectory(image, td["trajectory"], TRAJECTORY_COLOR, TRAJECTORY_WIDTH, True)
        return image, td, td["data"].get("final_text", text), td["data"].get("final_result", result)

    # ===== 3. DRAW OVERLAY =====
    image = robot.draw_info(image)

    # ===== 4. CODE VALIDATION CHECK =====
    # Don't return early — just flag and wait for timeout
    if not td["data"]["code_valid"]:
        text = "No for loop detected in code"

    # ===== 5. TRAJECTORY TRACKING =====
    # Always track regardless of code validity — visual feedback for student
    info = robot.get_info()
    robot_position_px = info["position_px"]
    robot_position = info["position"]

    if robot_position is not None:
        td["trajectory"].append(robot_position_px)
        text = f'Robot position: x: {robot_position[0]:0.1f} y: {robot_position[1]:0.1f}'

    if len(td["trajectory"]) > 0:
        draw_trajectory(image, td["trajectory"], TRAJECTORY_COLOR, TRAJECTORY_WIDTH, True)

    # ===== 6. MQTT MESSAGE =====
    msg = robot.get_msg()
    if msg is not None:
        text = f"Message received: {msg}"

    # ===== 7. TIMEOUT / FINAL EVALUATION =====
    # All failure cases handled here — completed=True always set before success=False
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed", False):
        td["data"]["completed"] = True

        if not td["data"]["code_valid"]:
            result["success"] = False  # safe — completed=True set above
            result["score"] = 0
            result["description"] = "No for loop found in code | Score: 0"
            text = "No for loop detected."
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = f"You are amazing! The Robot has completed the assignment | Score: 100"
            text = "Trajectory complete!"

        td["data"]["final_result"] = result
        td["data"]["final_text"] = text

    return image, td, text, result


# 2.5 Encoder theory
#checking the value of the encoders (falling within the range of 310-350) and checking the distance output

def encoder_theory(robot, image, td: dict, user_code=None):
    """Verification function for encoder theory task.
    Checks: math import, encoder resets, math.pi, printed encoder value 310-360°,
    printed distance in expected range, AND physical displacement matches.
    """

    # ===== CONFIGURATION =====
    WHEEL_RADIUS = 3.4      # actual measured wheel radius in cm
    ENCODER_MIN = 310       # minimum acceptable encoder degrees
    ENCODER_MAX = 360       # maximum acceptable encoder degrees
    DISTANCE_MIN = 18.0     # (310/360) * 2 * π * 3.4 = ~18.38 cm
    DISTANCE_MAX = 21.4     # (360/360) * 2 * π * 3.4 = ~21.36 cm
    DISPLACEMENT_MIN = 19.0 # OpenCV physical measurement lower bound
    DISPLACEMENT_MAX = 26.0 # OpenCV physical measurement upper bound
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
                "distance": None,
                "start_position": None,
                "end_position": None,
            }
        }

    # ===== 2. STATE LOCK =====
    if td["data"].get("completed", False):
        image = robot.draw_info(image)
        return image, td, td["data"].get("final_text", text), td["data"].get("final_result", result)

    # ===== 3. DRAW OVERLAY =====
    image = robot.draw_info(image)

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
    msg = robot.get_msg()
    if msg is not None:
        text = f"Received: {msg}"
        try:
            if msg.startswith("Encoder degrees left:"):
                td["data"]["encoder_left"] = float(msg.split(":")[1].strip())
            elif msg.startswith("Distance in cm:"):
                td["data"]["distance"] = float(msg.split(":")[1].strip())
        except (ValueError, IndexError):
            pass

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

            elif distance is None:
                result["success"] = False
                result["score"] = 0
                result["description"] = "No distance calculation received | Score: 0"
                text = "Distance not printed."

            elif distance < DISTANCE_MIN or distance > DISTANCE_MAX:
                result["success"] = False
                result["score"] = 0
                result["description"] = (
                    f"Distance out of range: {distance:.2f}cm "
                    f"(expected {DISTANCE_MIN}-{DISTANCE_MAX}cm based on R={WHEEL_RADIUS}cm) | Score: 0"
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

    return image, td, text, result

#2.6 While loops

def while_loops(robot, image, td: dict, user_code=None):
    """
    Verification: Don't Hit the Wall
    - Wall hit determined by physical displacement (OpenCV)
    - Score determined by encoder-derived distance
    - Both reported in final description
    - Final encoder read after stop is the authoritative value
    """

    # ===== CONFIGURATION =====
    TASK_DURATION       = 15
    TARGET_DISTANCE_CM  = 40.0          # wall position — robot must not exceed this physically
    SUCCESS_MIN_CM      = 38.0          # must reach at least this (encoder)
    R                   = 3.4           # wheel radius cm
    ENCODER_SANITY_CAP  = 2000          # filter concatenated MQTT values
    WALL_VISUAL_OFFSET  = 150           # extra pixels past target for wall line (tweak freely)
    BANNED_FUNCTIONS    = ["move_forward", "move_backward", "move_forward_distance",
                           "move_backward_distance", "move_forward_seconds", "move_backward_seconds"]
    # =========================

    # ===== 0. INITIAL RESULT TEMPLATE =====
    result = {
        "success": True,
        "description": "You are amazing! Robot stopped before the wall.",
        "score": 100
    }
    text = "Waiting..."

    # ===== 1. FIRST-RUN INITIALIZATION =====
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
                "completed": False,
                "wall_hit": False,
                "code_valid": len(found_banned) == 0,
                "banned_found": found_banned,
                "encoder_left": None,       # last value received — final print after stop is authoritative
                "final_displacement": None,
                "peak_displacement": 0.0,   # track max displacement to avoid jitter inflation
                "final_result": None,
                "final_text": None,
            }
        }

    # ===== 2. STATE LOCK =====
    if td["data"].get("completed", False):
        image = robot.draw_info(image)
        if td["wall_px"] is not None:
            wall_color = (0, 0, 255) if td["data"]["wall_hit"] else (0, 0, 0)
            cv2.line(image, (td["wall_px"], 0), (td["wall_px"], image.shape[0]), wall_color, 3)
        return image, td, td["data"].get("final_text", text), td["data"].get("final_result", result)

    # ===== 3. BANNED FUNCTION CHECK =====
    if not td["data"]["code_valid"]:
        td["data"]["completed"] = True
        result["success"] = False
        result["score"] = 0
        result["description"] = (f"Banned functions used: "
                                  f"{', '.join(td['data']['banned_found'])} | Score: 0")
        text = "Banned functions detected."
        td["data"]["final_result"] = result
        td["data"]["final_text"] = text
        return image, td, text, result

    # ===== 4. CAPTURE START POSITION & DERIVE WALL PIXEL X =====
    pos    = robot.position
    pos_px = robot.position_px

    if td["start_position"] is None and pos is not None and pos_px is not None:
        td["start_position"] = pos
        if pos[0] != 0:
            px_per_cm = pos_px[0] / pos[0]
            td["wall_px"] = int(pos_px[0] + TARGET_DISTANCE_CM * px_per_cm + WALL_VISUAL_OFFSET)

    # ===== 5. PARSE MQTT MESSAGES =====
    # The last message received is the authoritative encoder value —
    # student is instructed to do a final print after stop, capturing true position with drift
    msg = robot.get_msg()
    if msg is not None:
        try:
            val = float(msg.strip().split(":")[-1].strip())
            if val < ENCODER_SANITY_CAP:
                td["data"]["encoder_left"] = val
        except (ValueError, IndexError):
            pass

    # ===== 6. DRAW OVERLAY =====
    image = robot.draw_info(image)

    # ===== 7. TRACK DISPLACEMENT & WALL HIT FLAG =====
    if td["start_position"] is not None and pos is not None:
        dx = pos[0] - td["start_position"][0]
        dy = pos[1] - td["start_position"][1]
        displacement = math.sqrt(dx**2 + dy**2)

        # Track peak displacement to avoid post-stop jitter inflating the value
        if displacement > td["data"]["peak_displacement"]:
            td["data"]["peak_displacement"] = displacement

        td["data"]["final_displacement"] = displacement

        enc = td["data"]["encoder_left"] or 0
        text = f"Displacement: {displacement:.1f}cm | Encoder: {enc:.0f}°"

        # Wall hit is a physical event — triggered by peak displacement
        if td["data"]["peak_displacement"] >= TARGET_DISTANCE_CM:
            td["data"]["wall_hit"] = True
            text = f"WALL HIT! Displacement: {displacement:.1f}cm | Encoder: {enc:.0f}°"

    # ===== 8. DRAW WALL LINE =====
    # Color reflects wall_hit state set in section 7 — drawn after check so correct this frame
    if td["wall_px"] is not None:
        wall_color = (0, 0, 255) if td["data"]["wall_hit"] else (0, 0, 0)
        cv2.line(image, (td["wall_px"], 0), (td["wall_px"], image.shape[0]), wall_color, 3)

    # ===== 9. TIMEOUT EVALUATION =====
    if time.time() > td["end_time"] and not td["data"]["completed"]:
        td["data"]["completed"] = True
        enc       = td["data"]["encoder_left"]
        peak_disp = td["data"]["peak_displacement"]
        enc_dist  = (enc / 360) * (2 * math.pi * R) if enc is not None else None

        if enc is None:
            result["success"] = False
            result["score"] = 0
            result["description"] = "No encoder data received. Did you print inside the loop? | Score: 0"
            text = "No encoder data received."

        elif td["data"]["wall_hit"]:
            # Wall hit takes priority — but still report encoder distance so student sees the gap
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

        td["data"]["final_result"] = result
        td["data"]["final_text"] = text

    return image, td, text, result

##Old module_2 functions

def headlights(robot, image, td: dict, user_code=None):
    """Test for lesson 6: Headlights."""

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"

    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 15,
            "data": {
                "headlight_frames": 0,
                "count_frames": 0
            }
        }

        basepath = os.path.abspath(os.path.dirname(__file__))

        temp_on = cv2.imread(os.path.join(basepath, "images", "headlight-on.jpg"))
        temp_off = cv2.imread(os.path.join(basepath, "images", "headlight-off.jpg"))
        temp_on = cv2.resize(temp_on, (int(temp_on.shape[1]/3), int(temp_on.shape[0]/3)))
        temp_off = cv2.resize(temp_off, (int(temp_off.shape[1]/3), int(temp_off.shape[0]/3)))


        td["data"]["turn-on"] = temp_on
        td["data"]["turn-off"] = temp_off

        td["data"]["turn-on-mask"] = cv2.inRange(temp_on, np.array([0, 240, 0]), np.array([15, 255, 15]))
        td["data"]["turn-off-mask"] = cv2.inRange(temp_off, np.array([0, 0, 0]), np.array([15, 15, 15]))

    percentage_white = 0
    td["data"]["count_frames"] += 1
    image = robot.draw_info(image)

    if robot:
        lower_white = np.array([225, 225, 225])
        upper_white = np.array([255, 255, 255])

        # ✅ Use safe position retrieval
        robot_position = robot.get_info().get("position_px")
        if robot_position is not None:
            crop_x, crop_y = robot_position[0] + 80, robot_position[1] - 90
            crop_width, crop_height = 80, 180

            croped_image = image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]

            # Create mask for detecting white pixels
            mask = cv2.inRange(croped_image, lower_white, upper_white)

            # Calculate white pixel percentage
            total_pixels = croped_image.shape[0] * croped_image.shape[1]
            white_pixels = cv2.countNonZero(mask)
            percentage_white = (white_pixels / total_pixels) * 100

            # Draw contours around the white regions
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contour_image = croped_image.copy()
            cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

            # Overlay the contour image back to the main image
            image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width] = contour_image

    # ✅ Headlight detection logic
    if percentage_white > 2:
        td["data"]["headlight_frames"] += 1
        text = "Headlights ON"
        cv2.copyTo(td["data"]["turn-on"], td["data"]["turn-on-mask"],
                   image[30:30 + td["data"]["turn-on"].shape[0], 1080:1080 + td["data"]["turn-on"].shape[1]])
    else:
        text = "Headlights OFF"
        cv2.copyTo(td["data"]["turn-off"], td["data"]["turn-off-mask"],
                   image[30:30 + td["data"]["turn-off"].shape[0], 1080:1080 + td["data"]["turn-off"].shape[1]])

    # ✅ Check for task completion status
    if td["end_time"] - time.time() < 1:
        headlight_ratio = td["data"]["headlight_frames"] / td["data"]["count_frames"]

        if headlight_ratio < 0.6:
            result["success"] = False
            result["description"] = "It is disappointing, but the robot failed the task."
            result["score"] = 0

    return image, td, text, result


def alarm(robot, image, td: dict, user_code=None):
    """lesson 7: Alarm - Detects LED blinking with 1-second intervals."""

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"

    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 15,
            "data": {
                "headlight_frames": 0,
                "count_frames": 0,
                "changed": 0,
                "last_state": None,
                "state_start_time": None,
                "durations": [],
                "state_buffer": [],  # Buffer to smooth state changes
                "turn-on": None,
                "turn-off": None,
                "turn-on-mask": None,
                "turn-off-mask": None
            },
            "finished": False,
            "finish_time": None
        }

        basepath = os.path.abspath(os.path.dirname(__file__))

        temp_on_path = os.path.join(basepath, "images", "headlight-on.jpg")
        temp_off_path = os.path.join(basepath,"images", "headlight-off.jpg")

        # Check if files exist before loading
        if os.path.exists(temp_on_path) and os.path.exists(temp_off_path):
            temp_on = cv2.imread(temp_on_path)
            temp_off = cv2.imread(temp_off_path)

            if temp_on is not None and temp_off is not None:
                temp_on = cv2.resize(temp_on, (temp_on.shape[1] // 3, temp_on.shape[0] // 3))
                temp_off = cv2.resize(temp_off, (temp_off.shape[1] // 3, temp_off.shape[0] // 3))

                td["data"]["turn-on"] = temp_on
                td["data"]["turn-off"] = temp_off

                td["data"]["turn-on-mask"] = cv2.inRange(temp_on, np.array([0, 240, 0]), np.array([15, 255, 15]))
                td["data"]["turn-off-mask"] = cv2.inRange(temp_off, np.array([0, 0, 0]), np.array([15, 15, 15]))

    percentage_white = 0
    td["data"]["count_frames"] += 1
    image = robot.draw_info(image)

    current_state = False  # Default to OFF

    if robot:
        lower_white = np.array([225, 225, 225])
        upper_white = np.array([255, 255, 255])

        robot_info = robot.get_info()
        robot_position = robot_info.get("position_px")

        if robot_position:
            crop_x, crop_y = robot_position[0] + 80, robot_position[1] - 90
            crop_width, crop_height = 80, 180

            h, w, _ = image.shape
            crop_x = max(0, min(crop_x, w - crop_width))
            crop_y = max(0, min(crop_y, h - crop_height))

            crop_x, crop_y = int(crop_x), int(crop_y)
            crop_width, crop_height = int(crop_width), int(crop_height)

            cropped_image = image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]

            # Create mask for detecting white pixels
            mask = cv2.inRange(cropped_image, lower_white, upper_white)

            # Calculate white pixel percentage
            total_pixels = cropped_image.shape[0] * cropped_image.shape[1]
            white_pixels = cv2.countNonZero(mask)
            percentage_white = (white_pixels / total_pixels) * 100

            # Draw contours for visualization
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contour_image = cropped_image.copy()
            cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
            image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width] = contour_image

            # Use the same threshold as headlights function
            current_state = percentage_white > 2

            # Add to buffer for smoothing (use last 3 frames)
            td["data"]["state_buffer"].append(current_state)
            if len(td["data"]["state_buffer"]) > 3:
                td["data"]["state_buffer"].pop(0)

            # Determine smoothed state (majority vote)
            if len(td["data"]["state_buffer"]) >= 2:
                smoothed_state = sum(td["data"]["state_buffer"]) > len(td["data"]["state_buffer"]) / 2
            else:
                smoothed_state = current_state

            # Display current state with overlay images (only if loaded successfully)
            if smoothed_state:
                text = "Headlights ON"
                td["data"]["headlight_frames"] += 1
                if td["data"]["turn-on"] is not None and td["data"]["turn-on-mask"] is not None:
                    overlay_h, overlay_w = td["data"]["turn-on"].shape[:2]
                    if overlay_h + 30 <= image.shape[0] and overlay_w + 1080 <= image.shape[1]:
                        cv2.copyTo(td["data"]["turn-on"], td["data"]["turn-on-mask"],
                                  image[30:30 + overlay_h, 1080:1080 + overlay_w])
            else:
                text = "Headlights OFF"
                if td["data"]["turn-off"] is not None and td["data"]["turn-off-mask"] is not None:
                    overlay_h, overlay_w = td["data"]["turn-off"].shape[:2]
                    if overlay_h + 30 <= image.shape[0] and overlay_w + 1080 <= image.shape[1]:
                        cv2.copyTo(td["data"]["turn-off"], td["data"]["turn-off-mask"],
                                  image[30:30 + overlay_h, 1080:1080 + overlay_w])

            # Initialize state tracking
            if td["data"]["last_state"] is None:
                td["data"]["last_state"] = smoothed_state
                td["data"]["state_start_time"] = time.time()

            # Detect state change
            elif smoothed_state != td["data"]["last_state"]:
                duration = time.time() - td["data"]["state_start_time"]
                td["data"]["durations"].append(duration)

                td["data"]["last_state"] = smoothed_state
                td["data"]["state_start_time"] = time.time()
                td["data"]["changed"] += 1

    # Check for task completion
    if not td.get("finished", False):
        if td["end_time"] - time.time() < 0.5:
            td["finished"] = True
            td["finish_time"] = time.time()

            # Add final duration
            if td["data"]["state_start_time"]:
                final_duration = time.time() - td["data"]["state_start_time"]
                td["data"]["durations"].append(final_duration)

            # Check if durations are within acceptable range (0.75 to 1.25 seconds)
            valid_durations = [0.75 <= d <= 1.25 for d in td["data"]["durations"]]
            valid_ratio = sum(valid_durations) / len(td["data"]["durations"]) if td["data"]["durations"] else 0

            # Require at least 10 state changes and 75% valid timing
            if len(td["data"]["durations"]) >= 10 and valid_ratio >= 0.75:
                result["success"] = True
                result["description"] = "Success! The robot blinked correctly"
                result["score"] = 100
            else:
                result["success"] = False
                result["description"] = "Assignment failed"
                result["score"] = 0
    else:
        # Show result for 3 seconds before ending
        if time.time() - td["finish_time"] >= 3:
            # Keep final result state
            pass

    return image, td, text, result
