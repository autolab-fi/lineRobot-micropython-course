import ast
import cv2
import numpy as np
import time

target_points = {
    'line_sensor_leds': [(30, 50), (0, -200)],
    'analog_led_fade': [(30, 50), (0, -200)],
    'telemetry_heartbeat_health': [(30, 50), (30,0)],
}

block_library_functions = {
    'line_sensor_leds': False,
    'analog_led_fade': False,
    'telemetry_heartbeat_health': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])

def telemetry_heartbeat_health(robot, image, td):
    result = {
        "success": True,
        "description": "Verifying robot status messages...",
        "score": 0
    }
    text = "Waiting for robot status messages..."

    image = robot.draw_info(image)

    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "data": {
                "messages": [],
                "robots": {}
            },
            "finished": False,
            "finish_time": None
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        
        # Parse message format: "robot1 status=critical battery=3"
        import re
        pattern = r'(robot\d+)\s+status=(\w+)\s+battery=(\d+)'
        match = re.search(pattern, msg)
        
        if match:
            robot_name = match.group(1)
            status = match.group(2)
            battery = int(match.group(3))
            
            # Only store if it's one of the expected robots
            if robot_name in ["robot1", "robot2", "robot3"]:
                td["data"]["robots"][robot_name] = {
                    "status": status,
                    "battery": battery
                }

    # Display detected robots
    status_y = 150
    for robot_name, data in td["data"]["robots"].items():
        cv2.putText(image, f"{robot_name}: {data['status']}, battery={data['battery']}", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        status_y += 25

    # Expected values - ALL must match exactly
    expected = {
        "robot1": {"status": "critical", "battery": 3},
        "robot2": {"status": "warn", "battery": 8},
        "robot3": {"status": "ok", "battery": 10}
    }

    # Only mark as finished once
    if not td.get("finished", False):
        if len(td["data"]["robots"]) == 3:
            td["finished"] = True
            td["finish_time"] = time.time()
            
            # Check if ALL expected robots match EXACTLY
            all_match = (
                len(td["data"]["robots"]) == 3 and
                td["data"]["robots"].get("robot1", {}).get("status") == "critical" and
                td["data"]["robots"].get("robot1", {}).get("battery") == 3 and
                td["data"]["robots"].get("robot2", {}).get("status") == "warn" and
                td["data"]["robots"].get("robot2", {}).get("battery") == 8 and
                td["data"]["robots"].get("robot3", {}).get("status") == "ok" and
                td["data"]["robots"].get("robot3", {}).get("battery") == 10
            )
            
            if all_match:
                result["success"] = True
                result["description"] = "Success! All robot statuses are correct."
                result["score"] = 100
                text = "Verification successful!"
            else:
                result["success"] = False
                result["description"] = "Assignment failed."
                result["score"] = 0
                text = "Assignment failed."
                
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = "Assignment failed."
            result["score"] = 0
            text = "Assignment failed."
        else:
            # Keep running
            result["success"] = True
            result["description"] = f"Waiting for robot messages... ({len(td['data']['robots'])}/3 received)"
    else:
        # Show result for 3 seconds before ending
        if time.time() - td["finish_time"] >= 3:
            # Keep final result state (don't change success/score)
            pass
    
    return image, td, text, result

def line_sensor_leds(robot, image, td: dict):
    """Verification: Check if LEDs flash 6 times with 2-second intervals"""

    result = {
        "success": True,
        "description": "Verifying LED flashes...",
        "score": 0
    }
    text = "Monitoring LED flashes..."

    image = robot.draw_info(image)

    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 35,
            "data": {
                "flash_count": 0,
                "last_state": None,
                "state_start_time": None,
                "intervals": [],
                "state_buffer": []
            },
            "finished": False,
            "finish_time": None
        }

    percentage_white = 0
    current_state = False

    if robot:
        lower_white = np.array([215, 215, 215])
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

            mask = cv2.inRange(cropped_image, lower_white, upper_white)

            total_pixels = cropped_image.shape[0] * cropped_image.shape[1]
            white_pixels = cv2.countNonZero(mask)
            percentage_white = (white_pixels / total_pixels) * 100

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contour_image = cropped_image.copy()
            cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
            image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width] = contour_image

            current_state = percentage_white > 2

            # Smoothing with buffer (last 3 frames)
            td["data"]["state_buffer"].append(current_state)
            if len(td["data"]["state_buffer"]) > 3:
                td["data"]["state_buffer"].pop(0)

            if len(td["data"]["state_buffer"]) >= 2:
                smoothed_state = sum(td["data"]["state_buffer"]) > len(td["data"]["state_buffer"]) / 2
            else:
                smoothed_state = current_state

            if smoothed_state:
                text = "LED ON"
            else:
                text = "LED OFF"

            # Initialize state tracking
            if td["data"]["last_state"] is None:
                td["data"]["last_state"] = smoothed_state
                td["data"]["state_start_time"] = time.time()

            # Detect state change (OFF to ON = one flash)
            elif smoothed_state != td["data"]["last_state"]:
                duration = time.time() - td["data"]["state_start_time"]
                
                # Count flash when LED turns ON
                if smoothed_state:
                    td["data"]["flash_count"] += 1
                    if len(td["data"]["intervals"]) > 0:
                        # Store interval between flashes
                        td["data"]["intervals"].append(duration)
                
                td["data"]["last_state"] = smoothed_state
                td["data"]["state_start_time"] = time.time()

    # Display status information
    cv2.putText(image, f"Flashes detected: {td['data']['flash_count']}/6", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(image, f"Time remaining: {td['end_time'] - time.time():.1f}s", 
                (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Check for task completion
    if not td.get("finished", False):
        if td["data"]["flash_count"] >= 6 or time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            
            # Validation: Must have exactly 6 flashes
            if td["data"]["flash_count"] == 6:
                # Check intervals (should be ~2 seconds each, tolerance ±0.3s)
                valid_intervals = [1.7 <= interval <= 2.3 for interval in td["data"]["intervals"]]
                valid_ratio = sum(valid_intervals) / len(valid_intervals) if valid_intervals else 0
                
                # Need at least 80% of intervals to be valid
                if valid_ratio >= 0.8:
                    result["success"] = True
                    result["description"] = "Success! LED flashed 6 times with correct intervals."
                    result["score"] = 100
                    text = "Verification successful!"
                else:
                    result["success"] = False
                    result["description"] = "Assignment failed."
                    result["score"] = 0
                    text = "Assignment failed."
            else:
                result["success"] = False
                result["description"] = "Assignment failed."
                result["score"] = 0
                text = "Assignment failed."
        else:
            # Keep running
            result["success"] = True
            result["description"] = f"Monitoring... ({td['data']['flash_count']}/6 flashes)"
    else:
        # Show result for 3 seconds before ending
        if time.time() - td["finish_time"] >= 3:
            # Keep final result state
            pass

    return image, td, text, result
