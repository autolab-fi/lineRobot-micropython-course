"""Additive pilot checkers for the HAMK block-course movement module."""

import time


def get_target_points(task):
    targets = {
        "hamk_blocks_first_move": ([0, 0], [1, 0]),
        "hamk_blocks_turn_route": ([0, 0], [1, 0]),
    }
    return targets[task]


def _pending_calibration(_robot, frame, td, _code):
    if td is None:
        td = {"end_time": time.time() + 5, "data": {}}
    return frame, td, "Checker requires camera calibration", {
        "success": False,
        "description": "Pilot checker is not calibrated yet.",
        "score": 0,
    }


hamk_blocks_first_move = _pending_calibration
hamk_blocks_turn_route = _pending_calibration


def get_block_library_functions():
    return []
