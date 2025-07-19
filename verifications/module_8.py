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
    """Verification function for line following with multiple checkpoints"""
    result = {
        "success": True,
        "description": "Verifying",
        "score": 100
    }
    text = "Follow the line through all checkpoints"
    
    # Draw robot info on image
    image = robot.draw_info(image)
    
    # Initialize test data
    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + verification_time,  # Extended time for multiple checkpoints
            "data": {
                "reached_checkpoints": [False] * len(checkpoint_positions),
                "task_completed": False
            }
        }
        
        # Load checkpoint image
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "traffic-sign.jpg")
                
            if not os.path.exists(filepath):
                # Create a simple colored checkpoint as fallback
                cone = np.zeros((60, 60, 3), dtype=np.uint8)
                cone[:, :] = (0, 255, 0)  # Green 
            else:
                cone = cv2.imread(filepath)
                cone = cv2.resize(cone, (60, 60))
                
            mask = cv2.bitwise_not(cv2.inRange(cone, np.array([0, 240, 0]), np.array([35, 255, 35])))
            td["data"]["cone"] = cone
            td["data"]["cone-mask"] = mask
        except Exception as e:
            print(f"Error loading checkpoint image: {e}")
    
    # Update text if task is already completed
    if td["data"]["task_completed"]:
        text = "Robot passed all checkpoints!"
        result["description"] = "The robot successfully passed through all checkpoints!"
        return image, td, text, result
    
    # Place checkpoint markers on all uncompleted checkpoints
    for i, (y, x) in enumerate(checkpoint_positions):
        if not td["data"]["reached_checkpoints"][i]:
            # Make sure we stay within image bounds
            y_start = max(0, robot.cm_to_pixel(y,2) - 30)
            y_end = min(image.shape[0], robot.cm_to_pixel(y,2) + 30)
            x_start = max(0, robot.cm_to_pixel(x,1) - 30)
            x_end = min(image.shape[1], robot.cm_to_pixel(x,1) + 30)
            
            # Get region of interest
            roi = image[y_start:y_end, x_start:x_end]
            
            # Only draw if we have a valid ROI
            if roi.shape[0] > 0 and roi.shape[1] > 0:
                # Create resized cone for this specific ROI if needed
                if roi.shape != (60, 60, 3):
                    resized_cone = cv2.resize(td["data"]["cone"], (roi.shape[1], roi.shape[0]))
                    resized_mask = cv2.resize(td["data"]["cone-mask"], (roi.shape[1], roi.shape[0]))
                    cv2.copyTo(resized_cone, resized_mask, roi)
                else:
                    cv2.copyTo(td["data"]["cone"], td["data"]["cone-mask"], roi)
    
    # Check if robot passes through checkpoints
    if robot and robot.position_px:
        robot_x, robot_y = robot.position
        
        # Check each checkpoint
        for i, (y, x) in enumerate(checkpoint_positions):
            if not td["data"]["reached_checkpoints"][i] and np.linalg.norm([robot_x - x, robot_y - y]) < 10:
                td["data"]["reached_checkpoints"][i] = True
                
                # Mark checkpoint as reached with white circle
                y_start = max(0, robot.cm_to_pixel(y,2) - 30)
                y_end = min(image.shape[0], robot.cm_to_pixel(y,2) + 30)
                x_start = max(0, robot.cm_to_pixel(x,1) - 30)
                x_end = min(image.shape[1], robot.cm_to_pixel(x,1) + 30)
                cv2.circle(image, (robot.cm_to_pixel(x,1), robot.cm_to_pixel(y,2)), 30, (255, 255, 255), -1)
                
                text = f"Checkpoint {i+1}/{len(checkpoint_positions)} reached!"
                
        # Check if all checkpoints are reached
        if all(td["data"]["reached_checkpoints"]):
            td["data"]["task_completed"] = True
            # Set the end time to 1 second from now to stop the video quickly
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
            result["description"] = f" The robot only passed {completed}/{total} checkpoints in the allotted time."
    
    return image, td, text, result
