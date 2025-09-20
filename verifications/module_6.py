import cv2
import math
import time
import os
import numpy as np

target_points = {
    'line_sensor_intro': [(30, 50), (0,200)],

}

block_library_functions = {
    'line_sensor_intro': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])

def line_sensor_intro(robot, image, td):
    result = {
        "success": True,
        "description": "Verifying sensor values...",
        "score": 100
    }
    text = "Waiting for sensor values..."

    image = robot.draw_info(image)

    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "data": {
                "values": []
            }
        }

    msg = robot.get_msg()
    if msg is not None:
        text = f"Message received: {msg}"
        # message processing. Message format should be: [20, 30, 40, ..., 40]
        # then calculate average of the array. First readed message average should be more 100 and of the second less 100
        pattern = r'\[([\d\s,]+)\]'
        import re
        match = re.search(pattern, msg)
        if match:
            if len(td["data"]["values"]) < 2:
                numbers_str = match.group(1)
                numbers = [int(num) for num in re.findall(r'\d+', numbers_str)]
                average = sum(numbers) / len(numbers) if numbers else 0
                td["data"]["values"].append(average)

    cv2.putText(image, f"Values: {td['data']['values']}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    if len(td["data"]["values"]) == 2 or td["end_time"] - time.time() < 1:
        if len(td["data"]["values"]) == 2:
            first, second = td["data"]["values"]
            if first > 100 and second < 100:
                result["success"] = True
                result["description"] = "Conditions met."
                result["score"] = 100
                text = "Assignment complete."
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

    return image, td, text, result
