import cv2
import math
import time
import os
import numpy as np

target_points = {
    'basic_line_follower': [(25, 50), (0,-200)],
    'pi': [(100, 25), (30, 0)],
    'pid': [(100, 25), (30, 0)],
}

block_library_functions = {
    'basic_line_follower': False,
    'pi': False,
    'pid': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])


def basic_line_follower(robot, image, td: dict):
    basic_line_follower_checkpoints = [(25.4,26.5),(24.2, 46.2)]
    return checkpoint_verification(robot, image, td, basic_line_follower_checkpoints, 20)


def pi(robot, image, td: dict):
    pi_checkpoints = [(31, 116),(48, 99),(53, 113),(74, 114),(85,65.5)]
    return checkpoint_verification(robot, image, td, pi_checkpoints,30)

def pid(robot, image, td: dict):
    pid_checkpoints = [(31, 116),(48, 99),(53, 113),(74, 114),(89,63.5),(46,55.4),(57.7,73.9),(61.2,26.6),(24.2, 46.2)]
    return checkpoint_verification(robot, image, td, pid_checkpoints, 50)


def checkpoint_verification(robot, image, td, checkpoint_positions, verification_time):
    """
    Crops the image to a region of interest (ROI), divides it into a 3x3 grid,
    and places one checkpoint per cell as close as possible to the cell center on the black line.
    Skips cells where no line is detected. Grid lines are NOT drawn.
    """
    import cv2
    import numpy as np
    import time
    import random
    import os

    # --- CROP SETTINGS: Adjust these values to select your paper area ---
    top = 120
    bottom = 800
    left = 100
    right = 1150
    # ---------------------------------------------------------------

    result = {
        "success": True,
        "description": "Verifying",
        "score": 100
    }
    text = "Follow the line through all checkpoints"

    image = robot.draw_info(image)

    # Only place checkpoints once
    if not td or "checkpoints" not in td.get("data", {}):
        roi = image[top:bottom, left:right].copy()
        roi_h, roi_w = roi.shape[:2]
        cell_h = roi_h // 3
        cell_w = roi_w // 3

        checkpoint_positions = []
        for row in range(3):
            for col in range(3):
                y1 = row * cell_h
                y2 = (row + 1) * cell_h if row < 2 else roi_h
                x1 = col * cell_w
                x2 = (col + 1) * cell_w if col < 2 else roi_w

                cell = roi[y1:y2, x1:x2]
                gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
                binary = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
                )
                kernel = np.ones((7, 7), np.uint8)
                binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
                contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                min_area = 800
                filtered = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

                if filtered:
                    # Calculate cell center
                    cell_center = (cell_w // 2, cell_h // 2)
                    min_dist = float('inf')
                    closest_pt = None
                    for cnt in filtered:
                        for pt in cnt.reshape(-1, 2):
                            dist = (pt[0] - cell_center[0])**2 + (pt[1] - cell_center[1])**2
                            if dist < min_dist:
                                min_dist = dist
                                closest_pt = pt
                    if closest_pt is not None:
                        checkpoint_y = top + y1 + closest_pt[1]
                        checkpoint_x = left + x1 + closest_pt[0]
                        checkpoint_positions.append((checkpoint_y, checkpoint_x))
        # Initialize test data
        td = {
            "start_time": time.time(),
            "end_time": time.time() + verification_time,
            "data": {
                "checkpoints": checkpoint_positions,
                "reached_checkpoints": [False] * len(checkpoint_positions),
                "task_completed": False
            }
        }
        # Load checkpoint image (cone) if needed
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "traffic-sign.jpg")
            if not os.path.exists(filepath):
                cone = np.zeros((60, 60, 3), dtype=np.uint8)
                cone[:, :] = (0, 255, 0)
            else:
                cone = cv2.imread(filepath)
                cone = cv2.resize(cone, (60, 60))
            mask = cv2.bitwise_not(cv2.inRange(cone, np.array([0, 240, 0]), np.array([35, 255, 35])))
            td["data"]["cone"] = cone
            td["data"]["cone-mask"] = mask
        except Exception as e:
            print(f"Error loading checkpoint image: {e}")

    checkpoint_positions = td["data"]["checkpoints"]

    # (Grid lines are NOT drawn)

    # Place checkpoint markers (cones) on all uncompleted checkpoints
    for i, (y, x) in enumerate(checkpoint_positions):
        if not td["data"]["reached_checkpoints"][i]:
            y_start = max(0, y - 30)
            y_end = min(image.shape[0], y + 30)
            x_start = max(0, x - 30)
            x_end = min(image.shape[1], x + 30)
            roi_img = image[y_start:y_end, x_start:x_end]
            if roi_img.shape[0] > 0 and roi_img.shape[1] > 0:
                if roi_img.shape != (60, 60, 3):
                    resized_cone = cv2.resize(td["data"]["cone"], (roi_img.shape[1], roi_img.shape[0]))
                    resized_mask = cv2.resize(td["data"]["cone-mask"], (roi_img.shape[1], roi_img.shape[0]))
                    cv2.copyTo(resized_cone, resized_mask, roi_img)
                else:
                    cv2.copyTo(td["data"]["cone"], td["data"]["cone-mask"], roi_img)

    # Check if robot passes through checkpoints
    if robot and robot.position_px:
        robot_x, robot_y = robot.position_px
        for i, (y, x) in enumerate(checkpoint_positions):
            if not td["data"]["reached_checkpoints"][i] and np.linalg.norm([robot_x - x, robot_y - y]) < 100:
                td["data"]["reached_checkpoints"][i] = True
                y_start = max(0, y - 30)
                y_end = min(image.shape[0], y + 30)
                x_start = max(0, x - 30)
                x_end = min(image.shape[1], x + 30)
                cv2.circle(image, (x, y), 30, (255, 255, 255), -1)
                text = f"Checkpoint {i+1}/{len(checkpoint_positions)} reached!"
        if all(td["data"]["reached_checkpoints"]):
            td["data"]["task_completed"] = True
            td["end_time"] = time.time() + 1
            text = "All checkpoints passed!"
            result["description"] = "The robot successfully passed through all checkpoints!"

    # Check for time limit
    if td["end_time"] - time.time() < 1:
        if td["data"]["task_completed"]:
            result["success"] = True
            result["description"] = "Success! The robot passed through all checkpoints."
            result["score"] = 100
        else:
            result["success"] = False
            result["score"] = 0
            completed = sum(td["data"]["reached_checkpoints"])
            total = len(td["data"]["reached_checkpoints"])
            result["description"] = f"❌ The robot only passed {completed}/{total} checkpoints in the allotted time."
    return image, td, text, result


