import ast
import cv2
import numpy as np
import time

target_points = {
    'line_sensor_leds': [(45, 50), (30, 0)],
    'telemetry_heartbeat_health': [(30, 50), (30, 0)],
}

block_library_functions = {
    'line_sensor_leds': False,
    'telemetry_heartbeat_health': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])
    
def telemetry_heartbeat_health(robot, image, td, user_code=None):
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
            "end_time": time.time() + 15,
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


def line_sensor_leds(robot, image, td: dict, user_code=None):
    """Verification: Check if LEDs flash with 2-second ON and 2-second OFF intervals"""

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
            "end_time": time.time() + 30,
            "data": {
                "flash_count": 0,
                "last_state": None,
                "state_start_time": None,
                "on_durations": [],
                "off_durations": [],
                "state_buffer": []
            },
            "finished": False,
            "finish_time": None
        }

    percentage_white = 0
    current_state = False

    if robot:
        lower_white = np.array([245, 245, 245])
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

            # Detect state change - measure duration of previous state
            elif smoothed_state != td["data"]["last_state"]:
                duration = time.time() - td["data"]["state_start_time"]
                
                # Store duration based on what state just ENDED
                if td["data"]["last_state"]:  # Was ON, now OFF
                    td["data"]["on_durations"].append(duration)
                else:  # Was OFF, now ON
                    td["data"]["off_durations"].append(duration)
                    td["data"]["flash_count"] += 1  # Count when turning ON
                
                td["data"]["last_state"] = smoothed_state
                td["data"]["state_start_time"] = time.time()
    
    if len(td["data"]["off_durations"]) > 0:
        off_text = ", ".join([f"{d:.1f}s" for d in td["data"]["off_durations"]])
        cv2.putText(image, f"OFF: {off_text}", 
                    (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Check for task completion
    if not td.get("finished", False):
        if td["data"]["flash_count"] >= 7 or time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            
            # Add final duration if still in a state
            if td["data"]["state_start_time"]:
                final_duration = time.time() - td["data"]["state_start_time"]
                if td["data"]["last_state"]:
                    td["data"]["on_durations"].append(final_duration)
                else:
                    td["data"]["off_durations"].append(final_duration)
            
            # Validation: Must have 5-7 flashes
            if 5 <= td["data"]["flash_count"] <= 7:
                # Check ON durations (should be ~2 seconds, tolerance ±0.5s)
                valid_on = [1.5 <= d <= 2.5 for d in td["data"]["on_durations"]]
                on_ratio = sum(valid_on) / len(valid_on) if valid_on else 0
                
                # Check OFF durations (should be ~2 seconds, tolerance ±0.5s)
                valid_off = [1.5 <= d <= 2.5 for d in td["data"]["off_durations"]]
                off_ratio = sum(valid_off) / len(valid_off) if valid_off else 0
                
                # Need at least 60% of both ON and OFF durations to be valid
                if on_ratio >= 0.6 and off_ratio >= 0.6:
                    result["success"] = True
                    result["description"] = "Success! LED flashed with correct intervals."
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
