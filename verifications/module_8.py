import cv2
import math
import time
import os
import numpy as np

target_points = {
    'basic_line_follower': [(25, 85), (0,-200)],
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
    """Place checkpoints only in cells 1 and 2 (first row, first two cells)"""
    cell_indices = [0, 1,4]  # Cells 1, 2
    return checkpoint_verification_grid(robot, image, td, cell_indices, 20, "basic_line_follower")


def pi(robot, image, td: dict):
    """Place checkpoints in cells 2, 3, 5, 6, 8, 9"""
    cell_indices = [3,6,7,10,11]  # Cells 2, 3, 5, 6, 8, 9 (0-indexed)
    return checkpoint_verification_grid(robot, image, td, cell_indices, 30, "pi")


def pid(robot, image, td: dict):
    """Place checkpoints in all 12 cells"""
    cell_indices = [0,1,3,4,5,6,7,8,9,10,11]  # All cells
    return checkpoint_verification_grid(robot, image, td, cell_indices, 50, "pid")


def checkpoint_verification_grid(robot, image, td, cell_indices, verification_time, task_name):
    """
    Crops the image to a region of interest (ROI), divides it into a 3x4 grid (3 rows, 4 cols),
    and places checkpoints only in specified cells on the black line.
    
    Grid layout (0-indexed):
    [0]  [1]  [2]  [3]
    [4]  [5]  [6]  [7]
    [8]  [9]  [10] [11]
    """
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
    msg = robot.get_msg()
    if msg is not None:
        text = f"Message received: {msg}"

    image = robot.draw_info(image)

    # Only place checkpoints once
    if not td or "checkpoints" not in td.get("data", {}):
        roi = image[top:bottom, left:right].copy()
        roi_h, roi_w = roi.shape[:2]
        
        # 3x4 grid: 3 rows, 4 columns
        num_rows = 3
        num_cols = 4
        cell_h = roi_h // num_rows
        cell_w = roi_w // num_cols

        checkpoint_positions = []
        
        # Process only the specified cells
        for cell_index in cell_indices:
            row = cell_index // num_cols
            col = cell_index % num_cols
            
            y1 = row * cell_h
            y2 = (row + 1) * cell_h if row < num_rows - 1 else roi_h
            x1 = col * cell_w
            x2 = (col + 1) * cell_w if col < num_cols - 1 else roi_w

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
                "task_completed": False,
                "task_name": task_name,
                "show_grid": True,  # Flag to show grid temporarily
                "grid_start_time": time.time()
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

    # Draw grid lines temporarily (for first 3 seconds)
    if td["data"].get("show_grid", False):
        elapsed = time.time() - td["data"].get("grid_start_time", 0)
        if elapsed < 3.0:  # Show grid for 3 seconds
            roi_h = bottom - top
            roi_w = right - left
            num_rows = 3
            num_cols = 4
            cell_h = roi_h // num_rows
            cell_w = roi_w // num_cols
            
            # Draw vertical lines
            for col in range(1, num_cols):
                x = left + col * cell_w
                cv2.line(image, (x, top), (x, bottom), (0, 255, 255), 2)
            
            # Draw horizontal lines
            for row in range(1, num_rows):
                y = top + row * cell_h
                cv2.line(image, (left, y), (right, y), (0, 255, 255), 2)
            
            # Draw ROI boundary
            cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 3)
            
            # Label cells
            for row in range(num_rows):
                for col in range(num_cols):
                    cell_index = row * num_cols + col
                    y_center = top + row * cell_h + cell_h // 2
                    x_center = left + col * cell_w + cell_w // 2
                    cv2.putText(image, str(cell_index + 1), (x_center - 10, y_center), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
        else:
            td["data"]["show_grid"] = False  # Stop showing grid after 3 seconds

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