import cv2
import time
import numpy as np

# Starting point configuration for module 9 tasks
# Adjust points if the simulator expects a specific spawn zone
# Format: "task": [(x, y), (angle, speed)]
target_points = {
    "fog_of_war_survey": [(25,25), (30, 0)],
    "miniral_scanner_sweep" : [(30,50), (30, 0)]
}

# Library call restrictions to discourage bypassing the assignment
block_library_functions = {
    "fog_of_war_survey": False,
    "miniral_scanner_sweep": False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])

def fog_of_war_survey(robot, image, td):
    """
    Assignment 1: Fog of War - Explore and reveal the map
    Students write movement sequences to reveal >50-60% of the map
    """
    result = {
        "success": True,
        "description": "Exploring the map...",
        "score": 0
    }
    text = "Explore to reveal the map!"
    
    image = robot.draw_info(image)
    
    # Define the map area (exclude right debug panel)
    map_width = 1015  # Width of map area (before debug panel starts)
    
    if not td:
        # Initialize fog of war overlay (only for map area)
        fog_overlay = np.zeros_like(image)
        fog_overlay[:, :map_width] = (150, 150, 150)  # Dark gray fog only on map
        
        # Create revealed areas mask (only for map area)
        revealed_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 60,  # 20 seconds to explore
            "data": {
                "fog_overlay": fog_overlay,
                "revealed_mask": revealed_mask,
                "map_width": map_width,
                "total_pixels": image.shape[0] * map_width,  # Only count map pixels
                "revealed_pixels": 0,
                "reveal_radius": 100,  # Radius around robot that gets revealed
                "target_percentage": 85,  # Need to reveal 85% of map
                "task_completed": False,
                "completion_time": None
            },
            "finished": False,
            "finish_time": None
        }
    
    # Get robot position
    if robot and robot.position_px:
        robot_x, robot_y = robot.position_px
        
        # Only reveal if robot is in map area
        if robot_x < td["data"]["map_width"]:
            # Reveal area around robot
            cv2.circle(td["data"]["revealed_mask"], (robot_x, robot_y), 
                       td["data"]["reveal_radius"], 255, -1)
        
        # Calculate revealed percentage (only in map area)
        map_revealed_mask = td["data"]["revealed_mask"][:, :td["data"]["map_width"]]
        td["data"]["revealed_pixels"] = cv2.countNonZero(map_revealed_mask)
        revealed_percentage = (td["data"]["revealed_pixels"] / td["data"]["total_pixels"]) * 100
        
        # Apply fog where not revealed (only on map area)
        fog_mask = cv2.bitwise_not(td["data"]["revealed_mask"])
        fog_colored = cv2.bitwise_and(td["data"]["fog_overlay"], td["data"]["fog_overlay"], 
                                       mask=fog_mask)
        
        # Only apply fog to map area, leave debug panel clear
        image[:, :td["data"]["map_width"]] = cv2.addWeighted(
            image[:, :td["data"]["map_width"]], 1.0, 
            fog_colored[:, :td["data"]["map_width"]], 0.7, 0
        )
        
        # Draw exploration percentage
        cv2.putText(image, f"Map Revealed: {revealed_percentage:.1f}%", 
                    (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(image, f"Target: {td['data']['target_percentage']}%", 
                    (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(image, f"Time: {td['end_time'] - time.time():.1f}s", 
                    (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Check if target reached
        if revealed_percentage >= td["data"]["target_percentage"] and not td["data"]["task_completed"]:
            td["data"]["task_completed"] = True
            td["data"]["completion_time"] = time.time()
            text = f"Map explored! {revealed_percentage:.1f}% revealed!"
    
    # Check completion
    if not td.get("finished", False):
        if td["data"]["task_completed"] and td["data"]["completion_time"]:
            if time.time() - td["data"]["completion_time"] >= 2:
                td["finished"] = True
                td["finish_time"] = time.time()
                result["success"] = True
                result["score"] = 100
                result["description"] = f"Success! Explored {revealed_percentage:.1f}% of the map!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["score"] = 0
            result["description"] = f"Time expired. Only explored {revealed_percentage:.1f}% of map."
    else:
        if time.time() - td["finish_time"] >= 2:
            pass  # Keep final state
    
    return image, td, text, result
    
def miniral_scanner_sweep(robot, image, td):
    """
    Lesson 2.7: Multi-Point Mineral Survey
    Visit 5 scanning zones and activate scanner at each zone
    """
    # ===== SURVEY ZONE POSITIONS (ADJUST THESE) =====
    SURVEY_ZONES = [
        {"x": 300, "y": 200, "name": "Zone 1"},
        {"x": 1100, "y": 200, "name": "Zone 2"},
        {"x": 300, "y": 800, "name": "Zone 3"},
        {"x": 1100, "y": 800, "name": "Zone 4"},
        {"x": 650, "y": 500, "name": "Zone 5"}
    ]
    # =================================================
    
    result = {
        "success": True,
        "description": "Surveying mineral zones...",
        "score": 0
    }
    text = "Navigate to zones and activate scanner!"
    
    msg = robot.get_msg()
    if msg is not None:
        text = f"Message: {msg}"
    
    image = robot.draw_info(image)
    
    if not td:
        # Load mineral images for each zone
        minerals_data = []
        basepath = os.path.abspath(os.path.dirname(__file__))
        
        for i in range(5):
            mineral_info = {
                "type": ["Iron", "Gold", "Crystal", "Uranium", "Platinum"][i],
                "color": [(100, 100, 255), (0, 215, 255), (255, 0, 255), (0, 255, 0), (255, 200, 0)][i],
                "revealed": False
            }
            minerals_data.append(mineral_info)
        
        # Try to load zone marker image
        try:
            zone_marker_path = os.path.join(basepath, "auto_tests", "images", "traffic-sign.jpg")
            if os.path.exists(zone_marker_path):
                zone_marker = cv2.imread(zone_marker_path)
                zone_marker = cv2.resize(zone_marker, (60, 60))
                zone_mask = cv2.bitwise_not(cv2.inRange(zone_marker, np.array([0, 240, 0]), np.array([35, 255, 35])))
            else:
                zone_marker = np.zeros((60, 60, 3), dtype=np.uint8)
                zone_marker[:, :] = (0, 200, 200)
                zone_mask = np.ones((60, 60), dtype=np.uint8) * 255
        except:
            zone_marker = np.zeros((60, 60, 3), dtype=np.uint8)
            zone_marker[:, :] = (0, 200, 200)
            zone_mask = np.ones((60, 60), dtype=np.uint8) * 255
        
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 60,  # 60 seconds time limit
            "data": {
                "zones": SURVEY_ZONES,
                "minerals": minerals_data,
                "current_zone": 0,
                "zone_scanned": [False] * 5,
                "zone_led_on": [False] * 5,
                "zone_led_off": [False] * 5,
                "zone_marker": zone_marker,
                "zone_mask": zone_mask,
                "zone_radius": 80,  # Distance to consider "at zone"
                "at_zone": False,
                "scanner_active": False,
                "last_led_state": False,
                "task_completed": False,
                "completion_time": None
            },
            "finished": False,
            "finish_time": None
        }
    
    # Draw all zone markers
    for i, zone in enumerate(td["data"]["zones"]):
        zone_x, zone_y = zone["x"], zone["y"]
        
        # Determine zone color based on status
        if td["data"]["zone_scanned"][i]:
            # Scanned - show mineral with checkmark
            mineral = td["data"]["minerals"][i]
            cv2.circle(image, (zone_x, zone_y), 25, mineral["color"], -1)
            cv2.putText(image, "✓", (zone_x - 10, zone_y + 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        elif i == td["data"]["current_zone"]:
            # Current target zone
            y_start = max(0, zone_y - 30)
            y_end = min(image.shape[0], zone_y + 30)
            x_start = max(0, zone_x - 30)
            x_end = min(image.shape[1], zone_x + 30)
            roi_img = image[y_start:y_end, x_start:x_end]
            if roi_img.shape[0] > 0 and roi_img.shape[1] > 0:
                resized_marker = cv2.resize(td["data"]["zone_marker"], (roi_img.shape[1], roi_img.shape[0]))
                resized_mask = cv2.resize(td["data"]["zone_mask"], (roi_img.shape[1], roi_img.shape[0]))
                cv2.copyTo(resized_marker, resized_mask, roi_img)
        else:
            # Future zones
            cv2.circle(image, (zone_x, zone_y), 25, (150, 150, 150), 2)
        
        # Draw zone label
        cv2.putText(image, zone["name"], (zone_x - 30, zone_y - 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # LED detection using white color threshold
    current_time = time.time()
    current_zone_idx = td["data"]["current_zone"]
    led_detected = False
    
    if robot and robot.position_px:
        robot_x, robot_y = robot.position_px
        
        # Define crop region for LED detection (same as hazard lights)
        crop_x = robot_x + 80
        crop_y = robot_y - 90
        crop_width = 80
        crop_height = 180
        
        h, w, _ = image.shape
        crop_x = max(0, min(crop_x, w - crop_width))
        crop_y = max(0, min(crop_y, h - crop_height))
        crop_x, crop_y = int(crop_x), int(crop_y)
        crop_width, crop_height = int(crop_width), int(crop_height)
        
        cropped_image = image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]
        
        # White color detection
        lower_white = np.array([215, 215, 215])
        upper_white = np.array([255, 255, 255])
        
        blurred = cv2.GaussianBlur(cropped_image, (5, 5), 0)
        mask = cv2.inRange(blurred, lower_white, upper_white)
        
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = [contour for contour in contours if cv2.contourArea(contour) > 500]
        
        # Draw contours for visualization
        contour_image = cropped_image.copy()
        cv2.drawContours(contour_image, valid_contours, -1, (0, 255, 0), 2)
        image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width] = contour_image
        
        # LED state detection
        led_detected = len(valid_contours) > 0
        
        # Check robot position for zone
        if current_zone_idx < len(td["data"]["zones"]):
            zone = td["data"]["zones"][current_zone_idx]
            distance = np.sqrt((robot_x - zone["x"])**2 + (robot_y - zone["y"])**2)
            
            # Check if at zone
            if distance < td["data"]["zone_radius"]:
                if not td["data"]["at_zone"]:
                    td["data"]["at_zone"] = True
                    text = f"Arrived at {zone['name']}. Turn LED ON then OFF!"
                
                # Process LED state changes
                if td["data"]["at_zone"] and current_zone_idx < 5:
                    # LED turned ON
                    if led_detected and not td["data"]["last_led_state"]:
                        if not td["data"]["zone_led_on"][current_zone_idx]:
                            td["data"]["zone_led_on"][current_zone_idx] = True
                            td["data"]["scanner_active"] = True
                            text = f"Scanner activated at {zone['name']}!"
                    
                    # LED turned OFF
                    elif not led_detected and td["data"]["last_led_state"]:
                        if td["data"]["zone_led_on"][current_zone_idx] and not td["data"]["zone_led_off"][current_zone_idx]:
                            td["data"]["zone_led_off"][current_zone_idx] = True
                            td["data"]["scanner_active"] = False
                            
                            # Check if both ON and OFF received
                            if td["data"]["zone_led_on"][current_zone_idx] and td["data"]["zone_led_off"][current_zone_idx]:
                                td["data"]["zone_scanned"][current_zone_idx] = True
                                td["data"]["minerals"][current_zone_idx]["revealed"] = True
                                td["data"]["at_zone"] = False
                                td["data"]["current_zone"] += 1
                                
                                if td["data"]["current_zone"] >= 5:
                                    td["data"]["task_completed"] = True
                                    td["data"]["completion_time"] = current_time
                                    text = "All zones surveyed! Mission complete!"
                                else:
                                    text = f"Zone complete! Moving to next zone..."
        
        # Update last LED state
        td["data"]["last_led_state"] = led_detected
    
    # Draw scanner visualization
    if td["data"]["scanner_active"] and robot and robot.position_px:
        robot_x, robot_y = robot.position_px
        cv2.circle(image, (robot_x, robot_y), 100, (0, 255, 0), 3)
        cv2.putText(image, "SCANNING...", (robot_x - 60, robot_y - 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Draw LED status indicator
    if led_detected:
        cv2.putText(image, "LED: ON", (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(image, "LED: OFF", (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 100), 2)
    
    # Draw mission status
    completed_zones = sum(td["data"]["zone_scanned"])
    cv2.putText(image, f"Zones Surveyed: {completed_zones}/5", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv2.putText(image, f"Current: {td['data']['zones'][td['data']['current_zone']]['name'] if td['data']['current_zone'] < 5 else 'Complete'}", 
                (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(image, f"Time: {td['end_time'] - current_time:.1f}s", 
                (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Check completion
    if not td.get("finished", False):
        if td["data"]["task_completed"] and td["data"]["completion_time"]:
            if current_time - td["data"]["completion_time"] >= 2:
                td["finished"] = True
                td["finish_time"] = current_time
                result["success"] = True
                result["score"] = 100
                result["description"] = "Success! All 5 zones surveyed!"
                        
        elif current_time > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = current_time
            result["success"] = False
            result["score"] = 0
            result["description"] = f"Time expired. Only completed {completed_zones}/5 zones."
    else:
        if current_time - td["finish_time"] >= 2:
            pass
    
    return image, td, text, result
