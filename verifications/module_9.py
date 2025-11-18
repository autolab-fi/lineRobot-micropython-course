import cv2
import time
import numpy as np

# Starting point configuration for module 9 tasks
# Adjust points if the simulator expects a specific spawn zone
# Format: "task": [(x, y), (angle, speed)]
target_points = {
    "fog_of_war_survey": [(25,25), (30, 0)],
}

# Library call restrictions to discourage bypassing the assignment
block_library_functions = {
    "fog_of_war_survey": False,
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
