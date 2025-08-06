import cv2
import math
import time
import os
import numpy as np

target_points = {
    'line_sensor_intro': [(35, 50), (0,-200)],

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
        import re
        numbers = re.findall(r'-?\d+', str(msg))
        for num_str in numbers:
            if len(td["data"]["values"]) < 2:
                td["data"]["values"].append(int(num_str))

    cv2.putText(image, f"Values: {td['data']['values']}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    if len(td["data"]["values"]) == 2 or td["end_time"] - time.time() < 1:
        if len(td["data"]["values"]) == 2:
            first, second = td["data"]["values"]
            if first > 200 and second < 200:
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