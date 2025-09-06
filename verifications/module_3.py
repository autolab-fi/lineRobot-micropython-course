import cv2
import math
import time
import os
import numpy as np

target_points = {
    'differential_drive': [(30, 50), (30, 0)],
    'move_function':[(50, 50), (30, 0)],
    'electric_motor': [(50, 50), (30, 0)]
}

block_library_functions = {
    'differential_drive': True,
    "move_function": True,
    'electric_motor': True
}

def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])








def move_function(robot, image, td: dict):
    """Test: Robot must turn 180 degrees."""
    # overlay robot info on image
    image = robot.draw_info(image)

    # initialize task data
    if not td:
        current_ang = robot.compute_angle_x()
        target_ang = current_ang + 180 if current_ang < 180 else current_ang - 180
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 7,
            "target_ang": target_ang,
            "completed": False,
        }

    # default text/result
    ang = robot.compute_angle_x()
    delta_ang = abs(ang - td["target_ang"])
    text = f"Robot must turn to: {delta_ang:0.0f}"
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100,
    }

    # if within 10° of target, give 2 more seconds to settle
    if delta_ang < 10 and not td["completed"]:
        td["end_time"] = time.time() + 2
        td["completed"] = True

    # failure: ran out of time without reaching within 10°
    if (td["end_time"] - time.time()) < 1 and delta_ang > 10:
        result["success"] = False
        result["score"] = 0
        result["description"] = (
            f"Robot did not turn 180 degrees. "
            f"Final error: {delta_ang:0.0f} degrees"
        )

    # append score to description
    result["description"] += f" | Score: {result['score']}"

    return image, td, text, result



def electric_motor(robot, image, td: dict):
    """Test for lesson 8: Electric motor"""
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"
    
    image = robot.draw_info(image)
    
    if not td:
        td = {
            "end_time": time.time() + 7,
            "data": {}
        }
        
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, 'auto_tests', 'images', 'flag_finish.jpg')
              
            flag = cv2.imread(filepath)
            
            flag = cv2.resize(flag, (int(flag.shape[1]/3), int(flag.shape[0]/3)))
            lower_green = np.array([0, 240, 0]) 
            upper_green = np.array([50, 255, 50]) 
            td["data"]["flag-mask"] = cv2.bitwise_not(cv2.inRange(flag, lower_green, upper_green))
            td["data"]["flag"] = flag
            td["data"]["reached"] = False
        except Exception as e:
            print(f"Error loading or processing image: {e}")
            td["data"]["image_error"] = True
            return image, td, f"Error processing image: {str(e)}", result

    # Only proceed with flag-related operations if we have a flag
    if not td["data"].get("image_error", False):
        # First, set the flag coordinates if they don't exist yet
        if "flag-coords" not in td["data"] and robot:
            robot_info = robot.get_info()
            position_px = robot_info["position_px"]
            
            if position_px is None:
                return image, td, "Robot position not detected", result
                
            angle = robot.compute_angle_x()
            
            x = position_px[0] + 150 if 90 < angle < 270 else position_px[0] - 120
            y = position_px[1] - 180 if 90 < angle < 270 else position_px[1] + 200
            td["data"]["flag-coords"] = (x, y)
            td["data"]["flag-coords-cm"] = (robot.pixels_to_cm(x), robot.pixels_to_cm(y))
        
        # Then, in a separate condition, draw the flag using those coordinates
        if "flag-coords" in td["data"]:
            flag = td["data"]["flag"]
            x_left = int(flag.shape[0]/2)
            x_right = flag.shape[0] - x_left
            y_bottom = int(flag.shape[1]/2)
            y_up = flag.shape[1] - y_bottom
            
            # Check if coordinates are within image bounds
            coords = td["data"]["flag-coords"]
            if (0 <= coords[0] - x_left < image.shape[0] and 
                coords[0] + x_right < image.shape[0] and
                0 <= coords[1] - y_bottom < image.shape[1] and
                coords[1] + y_up < image.shape[1]):
                
                if td["data"]["reached"]:
                    # Increased rotation angle from 25 to 45 degrees
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

    position = robot.get_info()["position"]
    if position and "flag-coords-cm" in td["data"]:
        delta = robot.delta_points((position[1], position[0]), td["data"]["flag-coords-cm"])
        
        # Increased threshold from 5.1 to 7.0 cm for better detection
        if delta < 7.0:
            td["data"]["reached"] = True
            text = "The robot has reached target point!"
        else:
            text = f'Distance to target point {delta:0.1f} cm'
            
    if td["end_time"] - time.time() < 1 and td["data"].get("reached", False) == False:
        result["success"] = False
        result["score"] = 0
        result["description"] = "Robot did not reach the target point"
  
    return image, td, text, result

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

def differential_drive(robot, image, td):
    """Verification function for driving straight assignment"""
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Drive the robot in a straight line for 3 seconds"
    
    # Draw robot info on image
    image = robot.draw_info(image)

    # Initialize td if it's the first call
    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,  # Verification lasts for 10 seconds
            "data": {
                "task-failed": "",
                "failed-cone": {},
                "direction_0": None,
                "prev_robot_position": None,
                "robot_start_move_time": None,
                "robot_end_move_time": None,
                "max_angle_deviation": 0,
                "straight_driving_start": None,
                "straight_driving_duration": 0
            }
        }
        
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "traffic-sign.jpg")

            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "traffic-sign.jpg")
                
            if not os.path.exists(filepath):
                # Create a simple colored cone as fallback
                cone = np.zeros((100, 100, 3), dtype=np.uint8)
                cone[:, :] = (0, 0, 255)  # Red rectangle
            else:
                cone = cv2.imread(filepath)
                cone = cv2.resize(cone, (int(cone.shape[1]), int(cone.shape[0])))
                
            # Define green color range
            lower_green = np.array([0, 240, 0]) 
            upper_green = np.array([35, 255, 35])
            
            td["data"]["cone-mask"] = cv2.bitwise_not(cv2.inRange(cone, lower_green, upper_green))
            td["data"]["cone"] = cone
            td["data"]["cones-coords"] = []
        except Exception as e:
            print(f"Error initializing drive straight test: {e}")
            td["data"]["image_error"] = True

    # Set up cone coordinates if robot detected and coordinates not set
    if robot and robot.position_px and len(td["data"].get("cones-coords", [])) == 0:
        # Define cone positions to create a corridor
        y_u = robot.position_px[1] - 150  # Upper row of cones
        y_d = robot.position_px[1] + 150  # Lower row of cones
        for i in range(10):
            x = robot.position_px[0] + (i % 5) * 200
            if i < 5:
                td["data"]["cones-coords"].append((y_u, x))
            else:
                td["data"]["cones-coords"].append((y_d, x))
        
        # Save initial direction when robot is first detected
        if td["data"]["direction_0"] is None:
            td["data"]["direction_0"] = robot.compute_angle_x()
            if td["data"]["direction_0"] > 180:
                td["data"]["direction_0"] -= 360

    # Draw cones if we have coordinates and cone image
    if "cones-coords" in td["data"] and "cone" in td["data"] and len(td["data"]["cones-coords"]) > 0:
        try:
            cone = td["data"]["cone"]
            x_left = int(cone.shape[0] / 2)
            x_right = cone.shape[0] - x_left
            y_bottom = int(cone.shape[1] / 2)
            y_up = cone.shape[1] - y_bottom
            
            for i in range(min(10, len(td["data"]["cones-coords"]))):
                coords = td["data"]["cones-coords"][i]
                
                # Check if coordinates are within image bounds
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

    # Process robot movement
    if robot and robot.position is not None:
        # Get current angle
        angle_x = robot.compute_angle_x()
        angle_x_disp = angle_x
        
        if angle_x > 180:
            angle_x -= 360
        
        # Calculate angle difference (account for wrap-around at 360°)
        if td["data"]["direction_0"] is not None:
            angle_diff = abs(td["data"]["direction_0"] - angle_x)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
                
            # Track maximum deviation
            td["data"]["max_angle_deviation"] = max(td["data"]["max_angle_deviation"], angle_diff)
            
            text = f'Robot angle with x: {angle_x_disp:0.0f}°, Deviation: {angle_diff:.1f}°'
            
            # Check robot movement
            if td["data"]["prev_robot_position"] is not None:
                delta_pos = robot.delta_points(robot.position, td["data"]["prev_robot_position"])
                
                # Detect when robot starts moving
                if td["data"]["robot_start_move_time"] is None and delta_pos > 1:
                    td["data"]["robot_start_move_time"] = time.time()
                    td["data"]["straight_driving_start"] = time.time()
                    text = f"Robot started moving at angle {angle_x_disp:0.0f}°"
                
                # While robot is moving, check if it's staying within deviation limits
                if td["data"]["robot_start_move_time"] is not None and delta_pos > 0.5:
                    # If deviation is within limits and we're tracking straight driving
                    if angle_diff <= 10 and td["data"]["straight_driving_start"] is not None:
                        # Calculate current straight driving duration
                        current_time = time.time()
                        td["data"]["straight_driving_duration"] = current_time - td["data"]["straight_driving_start"]
                        
                        # Update text to show progress
                        if td["data"]["straight_driving_duration"] >= 3.0:
                            text = f"Success! Robot drove straight for {td['data']['straight_driving_duration']:.1f}s"
                            td["data"]["task-failed"] = ""  # Clear any failure state
                        else:
                            text = f"Straight: {td['data']['straight_driving_duration']:.1f}/3.0s, Deviation: {angle_diff:.1f}°"
                    
                    # If deviation exceeds limits
                    elif angle_diff > 10:
                        # Reset straight driving timer
                        td["data"]["straight_driving_start"] = None
                        td["data"]["straight_driving_duration"] = 0
                        
                        # Set task as failed if not already
                        if not td["data"]["task-failed"]:
                            td["data"]["task-failed"] = f"Robot deviated {angle_diff:.1f}° (max allowed: 10°)"
                            
                            # Find closest cone to knock down
                            if robot.position_px is not None and len(td["data"]["cones-coords"]) > 0:
                                min_index = closest_node((robot.position_px[1], robot.position_px[0]), 
                                                       td["data"]["cones-coords"])
                                if min_index not in td["data"]["failed-cone"]:
                                    td["data"]["failed-cone"][min_index] = -20
                
                # Detect when robot stops moving
                if td["data"]["robot_start_move_time"] is not None and delta_pos < 0.5:
                    if td["data"]["robot_end_move_time"] is None:
                        td["data"]["robot_end_move_time"] = time.time()
                        
                        # If it didn't drive straight for 3 seconds before stopping
                        if td["data"]["straight_driving_duration"] < 3.0 and not td["data"]["task-failed"]:
                            td["data"]["task-failed"] = f"Robot only drove straight for {td['data']['straight_driving_duration']:.1f}s (need 3.0s)"
        
        # Store current position for next frame
        td["data"]["prev_robot_position"] = robot.position

    # Check for task completion or failure
    if td["end_time"] - time.time() < 1:
        if td["data"]["task-failed"]:
            result["success"] = False
            result["description"] = td["data"]["task-failed"]
            result["score"] = 0
        elif td["data"].get("robot_start_move_time") is None:
            result["success"] = False
            result["description"] = "Robot didn't start moving"
            result["score"] = 0
        elif td["data"]["straight_driving_duration"] >= 3.0:
            result["success"] = True
            result["description"] = f"Success! Robot drove straight for {td['data']['straight_driving_duration']:.1f} seconds with max deviation of {td['data']['max_angle_deviation']:.1f}°"
            result["score"] = 100
        else:
            result["success"] = False
            result["description"] = f"Robot only drove straight for {td['data']['straight_driving_duration']:.1f}s (need 3.0s)"
            result["score"] = 0
    
    return image, td, text, result
