"""Verified copies of the first two physical checks from legacy module_1."""

import math
import time


TARGET_POINTS = {
    "hamk_blocks_welcome": [(35, 50), (30, 0)],
    "hamk_blocks_test_drive": [(35, 50), (30, 0)],
}


def get_target_points(task):
    return TARGET_POINTS.get(task, [])


def get_block_library_functions(_task):
    return False


def _delta_points(point_0, point_1):
    return math.sqrt(((point_0[0] - point_1[0]) ** 2) + ((point_0[1] - point_1[1]) ** 2))


def hamk_blocks_welcome(robot, image, td, _user_code=None):
    result = {
        "success": True,
        "description": "Connection established! System check complete.",
        "score": 100,
    }
    image = robot.draw_info(image)
    msg = robot.get_msg()

    if not td:
        td = {"start_time": time.time(), "end_time": time.time() + 10}

    if time.time() > td["end_time"]:
        text = "Link: Stable"
        if msg is not None:
            text = f"Message received: {msg}"
        return image, td, text, result

    text = "Checking connection..."
    if msg is not None:
        text = f"Message received: {msg}"
    return image, td, text, result


def hamk_blocks_test_drive(robot, image, td, _user_code=None):
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100,
    }
    if not td:
        td = {
            "end_time": time.time() + 10,
            "time_for_task": 3,
            "prev_robot_center": None,
        }

    robot_position = robot.get_info()["position"]
    text = "Not recognized"
    image = robot.draw_info(image)

    if td["prev_robot_center"] is not None and robot_position is not None:
        delta_pos = _delta_points(robot_position, td["prev_robot_center"])
        text = f"Robot position: x: {robot_position[0]:0.1f} y: {robot_position[1]:0.1f}"
        if "robot_start_move_time" not in td and delta_pos > 0.7:
            td["robot_start_move_time"] = time.time()
            td["end_time"] = time.time() + td["time_for_task"] + 3
        if "robot_start_move_time" in td and "robot_end_move_time" not in td and delta_pos < 0.7:
            td["robot_end_move_time"] = time.time()

    too_late = "robot_end_move_time" not in td and td["end_time"] - 1 < time.time()
    wrong_duration = (
        "robot_start_move_time" in td
        and "robot_end_move_time" in td
        and not td["time_for_task"] - 0.8
        <= td["robot_end_move_time"] - td["robot_start_move_time"]
        <= td["time_for_task"] + 0.8
    )
    if too_late or wrong_duration:
        result["success"] = False
        result["score"] = 0
        if "robot_start_move_time" in td and (
            "robot_end_move_time" not in td
            or td["robot_start_move_time"] + td["time_for_task"] + 0.7 < td["robot_end_move_time"]
        ):
            result["description"] = "The robot moved more than it should have."
        else:
            result["description"] = "The robot moved less than it should have."

    if robot_position:
        td["prev_robot_center"] = robot_position
    return image, td, text, result
