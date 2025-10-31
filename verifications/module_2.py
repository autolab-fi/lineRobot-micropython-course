import cv2
import math
import time
import os
import numpy as np

target_points = {
    'headlights': [(30, 50), (30, 0)],
    'alarm': [(30, 50), (30, 0)],
}

block_library_functions = {
    'headlights': False,
    'alarm': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])


def headlights(robot, image, td: dict):
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
        lower_white = np.array([215, 215, 215])
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


def alarm(robot, image, td: dict):
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
                "state_buffer": []  # Buffer to smooth state changes
            }
        }

        basepath = os.path.abspath(os.path.dirname(__file__))

        temp_on = cv2.imread(os.path.join(basepath,"auto_tests", "images", "headlight-on.jpg"))
        temp_off = cv2.imread(os.path.join(basepath, "auto_tests","images", "headlight-off.jpg"))

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

            # Create mask for detecting white pixels
            mask = cv2.inRange(cropped_image, lower_white, upper_white)

            # Calculate white pixel percentage (same method as headlights function)
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

            # Display current state
            if smoothed_state:
                text = "Headlights ON"
                td["data"]["headlight_frames"] += 1
                cv2.copyTo(td["data"]["turn-on"], td["data"]["turn-on-mask"],
                          image[30:30 + td["data"]["turn-on"].shape[0], 1080:1080 + td["data"]["turn-on"].shape[1]])
            else:
                text = "Headlights OFF"
                cv2.copyTo(td["data"]["turn-off"], td["data"]["turn-off-mask"],
                          image[30:30 + td["data"]["turn-off"].shape[0], 1080:1080 + td["data"]["turn-off"].shape[1]])

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
    if td["end_time"] - time.time() < 0.5:
        # Add final duration
        if td["data"]["state_start_time"]:
            final_duration = time.time() - td["data"]["state_start_time"]
            td["data"]["durations"].append(final_duration)

        # Check if durations are within acceptable range (0.75 to 1.25 seconds)
        valid_durations = [0.75 <= d <= 1.25 for d in td["data"]["durations"]]
        valid_ratio = sum(valid_durations) / len(td["data"]["durations"]) if td["data"]["durations"] else 0

        # Require at least 13 state changes (7 full blink cycles) and 80% valid timing
        if len(td["data"]["durations"]) >= 13 and valid_ratio >= 0.8:
            result["success"] = True
            result["description"] = f"Success! The robot blinked correctly"
            result["score"] = 100
        else:
            result["success"] = False
            result["description"] = f"Failed. Please Try Again"
            result["score"] = 0

    return image, td, text, result
