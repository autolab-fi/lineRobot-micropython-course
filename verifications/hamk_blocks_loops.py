"""Additive pilot checker for the HAMK block-course square lesson."""

import time


def get_target_points(task):
    if task != "hamk_blocks_square":
        raise KeyError(task)
    return [0, 0], [1, 0]


def hamk_blocks_square(_robot, frame, td, _code):
    if td is None:
        td = {"end_time": time.time() + 5, "data": {}}
    return frame, td, "Checker requires camera calibration", {
        "success": False,
        "description": "Pilot checker is not calibrated yet.",
        "score": 0,
    }


def get_block_library_functions():
    return []
