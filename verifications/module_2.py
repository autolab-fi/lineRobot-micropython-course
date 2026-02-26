import cv2
import math
import time
import os
import numpy as np
import re

target_points = {
    'electric_motors': [(30, 50), (30, 0)],
}

block_library_functions = {
    'electric_motors': False,
}

def get_block_library_functions(task):
    return block_library_functions.get(task, False)

def get_target_points(task):
    return target_points.get(task, [])

def electric_motors(robot, image, td, user_code=None):
    result = {"success": True, "description": "test", "score": 100}
    image = robot.draw_info(image)
    if not td:
        td = {"end_time": time.time() + 5}
    if time.time() > td["end_time"]:
        result["success"] = False
    return image, td, "test", result