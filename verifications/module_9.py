import cv2
import time
import numpy as np

# Starting point configuration for module 9 tasks
# Adjust points if the simulator expects a specific spawn zone
# Format: "task": [(x, y), (angle, speed)]
target_points = {
    "fog_of_war_survey": [(35, 50), (30, 0)],
}

# Library call restrictions to discourage bypassing the assignment
block_library_functions = {
    "fog_of_war_survey": False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])


def _init_tracking_data():
    """Initialize shared tracking data for the fog-of-war sweep."""
    return {
        "start_time": time.time(),
        "end_time": time.time() + 60,
        "data": {
            "rows": 8,
            "cols": 12,
            "visited": np.zeros((8, 12), dtype=bool),
            "coverage": 0.0,
            "path": [],
        },
        "finished": False,
        "finish_time": None,
    }


def _draw_grid(image, rows, cols, visited):
    """Draw a coverage grid overlay and shade visited cells."""
    h, w, _ = image.shape
    cell_h = h // rows
    cell_w = w // cols

    for r in range(rows):
        for c in range(cols):
            x0, y0 = c * cell_w, r * cell_h
            x1, y1 = x0 + cell_w, y0 + cell_h
            color = (0, 255, 0) if visited[r, c] else (80, 80, 80)
            cv2.rectangle(image, (x0, y0), (x1, y1), color, 1)

    return cell_h, cell_w


def fog_of_war_survey(robot, image, td: dict):
    """Verify that the robot reveals at least 90% of the map with a sweep algorithm."""

    result = {
        "success": True,
        "description": "Sweeping the foggy map...",
        "score": 0,
    }

    if not td:
        td = _init_tracking_data()

    rows = td["data"]["rows"]
    cols = td["data"]["cols"]
    visited = td["data"]["visited"]

    cell_h, cell_w = _draw_grid(image, rows, cols, visited)

    text = "Waiting for robot position..."
    image = robot.draw_info(image)

    if robot and robot.position_px is not None:
        x_px, y_px = robot.position_px
        col = min(max(int(x_px // cell_w), 0), cols - 1)
        row = min(max(int(y_px // cell_h), 0), rows - 1)

        visited[row, col] = True
        td["data"]["path"].append((x_px, y_px))

        revealed_cells = int(visited.sum())
        total_cells = rows * cols
        coverage = (revealed_cells / total_cells) * 100
        td["data"]["coverage"] = coverage

        text = f"Coverage: {coverage:.1f}% ({revealed_cells}/{total_cells} cells)"

        if not td["finished"] and coverage >= 90.0:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = True
            result["description"] = "Success! Coverage reached at least 90%."
            result["score"] = 100

    # Timeout handling
    if not td["finished"] and time.time() > td["end_time"]:
        td["finished"] = True
        td["finish_time"] = time.time()
        result["success"] = False
        result["description"] = f"Timeout. Coverage reached {td['data']['coverage']:.1f}%"
        result["score"] = 0
        text = result["description"]

    # Keep final result visible for a short period
    if td["finished"] and td["finish_time"]:
        if time.time() - td["finish_time"] >= 3:
            pass

    return image, td, text, result
