import cv2
import math
import time
import numpy as np

target_points = {
    # expected reset point + expected reset angle
    'Parking': [(20, 30), (43, 0)],

    # final parking point + final parking angle
    'Parking_final': [(115.3, 55.1), (177, 0)]
}

block_library_functions = {
    'Parking': False
}


def get_block_library_functions(task):
    global block_library_functions
    return block_library_functions[task]


def get_target_points(task):
    global target_points
    return target_points[task]

# HELPERS

def delta_points(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)



def angle_diff(a, b):
    """Smallest difference between angles in degrees."""
    return abs((a - b + 180) % 360 - 180)



# PARKING VERIFICATION 

def Parking(robot, image, td: dict):
    """Lesson 15: Parking verification"""

    result = {
        "success": True,
        "description": "Parking completed successfully",
        "score": 100
    }

    text = "Not recognized"

    image = robot.draw_info(image)


    # Init task state
    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 30,
            "data": {},
            "parked": False,
            "reset_checked": False
        }

    # -------------------------------------------------
    # 1) CHECK RESET POSITION + ANGLE (like other tasks)
    # -------------------------------------------------
    if not td["reset_checked"] and robot:
        expected_reset_pos, expected_reset_ang_tuple = get_target_points("Parking")
        expected_reset_ang = expected_reset_ang_tuple[0]

        real_pos = robot.get_info().get("position")
        real_ang = robot.compute_angle_x()

        if real_pos is not None:
            reset_d = delta_points(real_pos, expected_reset_pos)
            reset_a = angle_diff(real_ang, expected_reset_ang)

            # We DON'T fail if reset is off, we just report it.
            # Reset in OnDroid is approximate.
            text = (
                f"Reset check → dist error: {reset_d:.1f} cm, "
                f"angle error: {reset_a:.1f}°"
            )

        td["reset_checked"] = True

    # -------------------------------------------------
    # 2) PARKING SUCCESS CHECK (fixed final target)
    # -------------------------------------------------
    final_pos, final_ang_tuple = get_target_points("Parking_final")
    final_ang = final_ang_tuple[0]

    pos = robot.get_info().get("position")
    if pos is not None:
        d = delta_points(pos, final_pos)
        a = angle_diff(robot.compute_angle_x(), final_ang)

        text = f"Distance to parking point: {d:.1f} cm | Angle error: {a:.1f}°"

        # position tolerance + angle tolerance
        if d < 4 and a < 10:
            td["parked"] = True
            td["end_time"] = time.time() + 2

    # -------------------------------------------------
    # 3) FAIL ON TIMEOUT
    # -------------------------------------------------
    if time.time() > td["end_time"] and not td["parked"]:
        result["success"] = False
        result["score"] = 0
        result["description"] = (
            f"Robot failed to park in time. "
            f"Target: ({final_pos[0]}, {final_pos[1]}) @ {final_ang}°"
        )

    return image, td, text, result


# ---------------------------------------------------------
# TASK DISPATCHER
# ---------------------------------------------------------

def run_task(task, robot, image, td):
    if task == "Parking":
        return Parking(robot, image, td)

    return image, td, "Unknown task", {
        "success": False,
        "description": "Task name not recognized",
        "score": 0
    }