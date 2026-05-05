import cv2
import math
import time
import os
import numpy as np
import re

import ast


target_points = {
    'navigation': [(30, 70), (30, 0)],
    'perimeter': [(50, 50), (30, 0)],
    'visual_telemetry': [(50, 60), (30, 0)],
    'adaptive_racing': [(80, 30), (-30, 0)],
}

block_library_functions = {
    'navigation': False,
    'perimeter': False,
    'visual_telemetry': False,
    'adaptive_racing': False,
}

def get_block_library_functions(task):
    global block_library_functions
    return block_library_functions[task]


# function to get value from dictionary target_point
def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])

def delta_points(point_0, point_1):
    return math.sqrt(((point_0[0] - point_1[0]) ** 2) +
                     ((point_0[1] - point_1[1]) ** 2))


def calculate_target_point(rb, targets):
    """Calculate the target points based on the robot's current position and movement directions."""
    
    # Get the robot's position properly
    pos = rb.get_info().get("position")
    
    if pos is None:
        print("Error: Robot position is None")
        return []

    point = [pos[0], pos[1]]
    direction = rb.compute_angle_x()

    res = []
    for target in targets:
        if isinstance(target, dict):
            point[0] += target['forward'] * math.cos(math.radians(direction))
            point[0] -= target['backward'] * math.cos(math.radians(direction))
            point[1] -= target['forward'] * math.sin(math.radians(direction))
            point[1] += target['backward'] * math.sin(math.radians(direction))
            res.append((point[0], point[1]))
        else:
            # Handle reversed y-axis
            direction += target[0]['left']
            direction -= target[0]['right']

    res.reverse()
    return res

def draw_trajectory(image, points, color, width, restore):
    """Function for drawing point trajectory"""
    prev_point = None
    for point in points:
        cv2.circle(image, point, width, color, -1)
        if restore and prev_point is not None and math.sqrt(
                (prev_point[0] - point[0]) ** 2 + (prev_point[1] - point[1]) ** 2) > 1:
            restore_trajectory(image, prev_point, point, color, int(width * 2))
        prev_point = point

def restore_trajectory(image, prev_point, point, color, width):
    """Function for restoring trajectory if robot was not recognized"""
    cv2.line(image, prev_point, point, color, width)

# Task 1: Navigation

def navigation(robot, image, td: dict, user_code): 
    """Test for task 1 navigation"""

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"
    image = robot.draw_info(image)

    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 30,
            "data": {},
            "delta": 4,
            "reached_point": False
        }

    # Code style check
    comments_count = user_code.count('#')
    has_variables = bool(re.search(r'\w+\s*=\s*\d+', user_code))

    style_ok = (comments_count >= 2) and has_variables

    if not td["data"] and robot:
        route = [
            {'forward': 20, 'backward': 0},
            [{'left': 45, 'right': 0}],
            {'forward': 40, 'backward': 0},
            [{'left': 0, 'right': 45}],
            {'forward': 20, 'backward': 0},
            [{'left': 0, 'right': 90}],
            {'forward': 40, 'backward': 0},
        ]

        td["data"]['targets'] = calculate_target_point(robot, route)
        td["data"]['delta'] = 4
        td["data"]['reached_point'] = False

        # Load single mineral image
        basepath = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(basepath, 'images', 'mineral.png')
        
        mineral_img = cv2.imread(filepath)
        
        if mineral_img is None:
            print("Error: Could not load mineral.png")
            td["data"]["mineral"] = None
            td["data"]["mask"] = None
        else:
            # Resize mineral to match original fruit size
            original_height = mineral_img.shape[0]
            original_width = mineral_img.shape[1]
            new_height = int(original_height * 0.2)
            new_width = int(original_width * 0.2)
            mineral_img = cv2.resize(mineral_img, (new_width, new_height))
            
            # Create mask: non-black pixels are visible
            gray = cv2.cvtColor(mineral_img, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
            
            td["data"]["mineral"] = mineral_img
            td["data"]["mask"] = mask
        
        # Track which checkpoints are still visible
        td["data"]["checkpoint_visible"] = [True] * 4
        
        td["data"]['coordinates'] = [
            (robot.cm_to_pixel(x), robot.cm_to_pixel(y)) for x, y in td["data"]['targets']
        ]

    d = None

    if robot:
        robot_position = robot.get_info().get("position")
        if robot_position is not None:
            d = delta_points(robot_position, td["data"]['targets'][-1])
            text = (
                f'The distance to the next ({td["data"]["targets"][-1][0]:0.0f}, '
                f'{td["data"]["targets"][-1][1]:0.0f}) point is {d:0.0f}'
            )

            if d < td["data"]['delta']:
                if len(td["data"]['targets']) > 1:
                    # Mark this checkpoint as collected
                    checkpoint_index = len(td["data"]['targets']) - 1
                    td["data"]["checkpoint_visible"][checkpoint_index] = False
                    
                    td["data"]['delta'] += 1.3
                    td["data"]['targets'].pop()
                elif not td["data"]['reached_point']:
                    # Final checkpoint collected
                    td["data"]["checkpoint_visible"][0] = False
                    td["data"]['reached_point'] = True
                    td["end_time"] = time.time() + 4

    if d is not None and td["end_time"] - time.time() < 2 and (
            len(td["data"]['targets']) != 1 or d > td["data"]['delta']):
        if len(td["data"]['targets']) > 1:
            text = "Robot missed several checkpoints"
        else:
            text = (
                f'It is disappointing, but robot failed the task, '
                f'because it is {d:0.0f} centimeters away from the target point'
            )
        result["description"] = text
        result["success"] = False
        result["score"] = 0

    # Final check
    time_up = time.time() > td["end_time"]
    if td["data"].get('reached_point') or time_up:
        if not style_ok and result["success"]:
            result.update({"success": False, "score": 0, 
                           "description": "Task failed. Use variables (e.g., dist = 20) and at least 2 comments (#) in your code."})

    # Draw minerals at checkpoint locations with masking
    if td["data"] and td["data"]["mineral"] is not None and td["data"]["mask"] is not None:
        mineral = td["data"]["mineral"]
        mask = td["data"]["mask"]
        
        # Use same positioning as original code
        ymin = mineral.shape[0] // 2
        ymax = mineral.shape[0] - ymin
        xmin = mineral.shape[1] // 2
        xmax = mineral.shape[1] - xmin
        
        for i, (x, y) in enumerate(td["data"]['coordinates']):
            # Only draw if checkpoint is still visible
            if i < len(td["data"]["checkpoint_visible"]) and td["data"]["checkpoint_visible"][i]:
                # Check bounds before drawing
                if (y - ymin >= 0 and y + ymax <= image.shape[0] and 
                    x - xmin >= 0 and x + xmax <= image.shape[1]):
                    # Use cv2.copyTo to apply mask (only non-black pixels)
                    cv2.copyTo(mineral, mask, image[y - ymin:y + ymax, x - xmin:x + xmax])

    return image, td, text, result

# Task 2: Perimeter

def perimeter(robot, image, td: dict, user_code=None):
    """Test for task 2 perimeter"""

    TASK_DURATION = 30
    TRAJECTORY_COLOR = (255, 0, 0)
    TRAJECTORY_WIDTH = 3

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Analyzing code..."

    image = robot.draw_info(image)

    if not td:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        
        syntax_ok = True
        has_for_loop = False
        try:
            tree = ast.parse(active_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.For):
                    has_for_loop = True
        except SyntaxError:
            syntax_ok = False

        td = {
            "start_time": time.time(),
            "end_time": time.time() + TASK_DURATION,
            "data": {
                "syntax_ok": syntax_ok,
                "has_for_loop": has_for_loop,
                "total_distance": 0.0,
                "last_pos": None,
                "completed_verdict": False
            },
            "trajectory": []
        }

    if not td["data"]["syntax_ok"]:
        text = "Syntax/Indentation Error!"
    elif not td["data"]["has_for_loop"]:
        text = "No 'for' loop detected!"

    info = robot.get_info()
    robot_position_px = info["position_px"]
    robot_position = info["position"]

    MIN_DIST_PX = 5

    if robot_position is not None:
        if td["data"]["last_pos"] is not None:
            dx = robot_position[0] - td["data"]["last_pos"][0]
            dy = robot_position[1] - td["data"]["last_pos"][1]
            dist = (dx**2 + dy**2)**0.5
            td["data"]["total_distance"] += dist
        td["data"]["last_pos"] = robot_position

        if len(td["trajectory"]) == 0:
            td["trajectory"].append(robot_position_px)
        else:
            last = td["trajectory"][-1]
            dx_px = robot_position_px[0] - last[0]
            dy_px = robot_position_px[1] - last[1]
            if (dx_px**2 + dy_px**2) ** 0.5 >= MIN_DIST_PX:
                td["trajectory"].append(robot_position_px)
        
        if td["data"]["syntax_ok"] and td["data"]["has_for_loop"]:
            text = f'Dist: {td["data"]["total_distance"]:0.1f} cm | Pos: x: {robot_position[0]:0.1f} y: {robot_position[1]:0.1f}'

    if len(td["trajectory"]) > 0:
        try:
            draw_trajectory(image, td["trajectory"], TRAJECTORY_COLOR, TRAJECTORY_WIDTH, True)
        except NameError:
            pass

    if td["end_time"] - time.time() < 1 and not td["data"]["completed_verdict"]:
        td["data"]["completed_verdict"] = True
        
        total_dist = td["data"]["total_distance"]
        
        if not td["data"]["syntax_ok"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Mission Failed: Syntax or Indentation Error. Check your spaces! | Score: 0"
            text = "Syntax Error"
            
        elif not td["data"]["has_for_loop"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Mission Failed: You must use a 'for' loop to automate the patrol! | Score: 0"
            text = "Missing loop"
            
        elif total_dist < 100.0:
            result["success"] = False
            result["score"] = 20
            result["description"] = f"Mission Failed: Perimeter incomplete! Traveled only {total_dist:.1f}cm out of ~120cm. | Score: 20"
            text = "Incomplete perimeter"
            
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = "You are amazing! Perimeter patrol complete! | Score: 100"
            text = "Task completed!"

    return image, td, text, result

# Task 3: Led

def visual_telemetry(robot, image, td: dict, user_code):
    """Test for task 3: visual telemetry"""

    TASK_DURATION = 35 
    
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Initializing..." 
    
    image = robot.draw_info(image)

    if not td:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        
        has_while = 'while' in active_code
        has_break = 'break' in active_code
        has_pin15 = '15' in active_code and 'Pin' in active_code
        has_led_toggle = '.on()' in active_code and '.off()' in active_code
        has_stop = 'stop(' in active_code or 'speed(0' in active_code
        
        has_sensor_idx = bool(re.search(r'[\[\(][34][\]\)]', active_code))
        
        code_valid = (has_while and has_break and has_pin15 and 
                      has_led_toggle and has_stop and has_sensor_idx)

        fail_reason = ""
        if not has_pin15:
            fail_reason = "LED on Pin 15 is not configured correctly."
        elif not has_while:
            fail_reason = "Missing 'while' loop for active monitoring."
        elif not has_sensor_idx:
            fail_reason = "You must check the central sensors (Index 3 or 4)."
        elif not has_break:
            fail_reason = "Missing 'break' statement to exit the loop."
        elif not has_stop:
            fail_reason = "Missing command to stop the motors (e.g., robot.stop())."
        elif not has_led_toggle:
            fail_reason = "LED is not blinking (missing .on() or .off())."

        info = robot.get_info()
        start_pos = info["position"] if info["position"] else [0, 0]

        td = {
            "start_time": time.time(),
            "end_time": time.time() + TASK_DURATION,
            "data": {
                "code_valid": code_valid,
                "fail_reason": fail_reason,
                "start_pos": start_pos,
                "last_pos": start_pos, 
                "has_stopped": False,
                "was_moving": False
            }
        }

    if not td["data"]["code_valid"]:
        text = f'Code Error: {td["data"]["fail_reason"]}'

    info = robot.get_info()
    current_pos = info.get("position")

    if current_pos is not None:
        dx_start = current_pos[0] - td["data"]["start_pos"][0]
        dy_start = current_pos[1] - td["data"]["start_pos"][1]
        dist_moved = math.sqrt(dx_start**2 + dy_start**2)

        last_pos = td["data"]["last_pos"]
        dx_frame = current_pos[0] - last_pos[0]
        dy_frame = current_pos[1] - last_pos[1]
        dist_frame = math.sqrt(dx_frame**2 + dy_frame**2)
        
        td["data"]["last_pos"] = current_pos

        if dist_moved > 3.0:
            td["data"]["was_moving"] = True
            text = "Robot is scanning for the crevasse."
        
        if td["data"]["was_moving"] and dist_frame < 0.05:
            td["data"]["has_stopped"] = True

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = f'Task failed: {td["data"]["fail_reason"]}'
            text = "Task failed."
        elif not td["data"]["has_stopped"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Task failed: Robot did not stop at the line."
            text = "Emergency stop failed."
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = "You are amazing! The Robot has completed the assignment | Score: 100"
            text = "Telemetry signal complete!"

    return image, td, text, result



def adaptive_racing(robot, frame, td: dict, user_code):
    """
    Verification for Mission 11.4: Code Clinic (Adaptive Racing)
    Students must fix 5 bugs:
    1. SyntaxError (missing colon)
    2. Missing 'import time'
    3. Empty set_sensitivity()
    4. analog_read_all() -> track_line()
    5. time.sleep(5) -> time.sleep(0.05)
    """
    # ===== CONFIGURATION =====
    TASK_DURATION = 40.0  # seconds
    MIN_MOVEMENT_DISTANCE = 30.0  # cm
    # =========================

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Analyzing code for bugs..."

    frame = robot.draw_info(frame)

    # ── First-frame initialization ────────────────────────────────────────────
    if td is None:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        
        # 1. Syntax check
        syntax_ok = True
        try:
            ast.parse(active_code)
        except SyntaxError:
            syntax_ok = False

        # Regex and keyword checks
        has_time_import = bool(re.search(r'import\s+time', active_code))
        has_sensitivity = bool(re.search(r'set_sensitivity\(\s*[^)]+\s*\)', active_code))
        has_track_line = 'track_line(' in active_code
        has_good_sleep = bool(re.search(r'time\.sleep\(\s*0?\.[0-9]+\s*\)', active_code))

        code_valid = syntax_ok and has_time_import and has_sensitivity and has_track_line and has_good_sleep

        # Quest-like bug names (No spoilers!)
        missing = []
        if not syntax_ok:
            missing.append("The Syntax Bug")
        if not has_time_import:
            missing.append("The Import Bug")
        if not has_sensitivity:
            missing.append("The Setup Bug")
        if not has_track_line:
            missing.append("The Array Bug")
        if not has_good_sleep:
            missing.append("The Coma Bug")

        info = robot.get_info()
        start_pos = info.get("position")

        td = {
            "start_time": time.time(),
            "end_time": time.time() + TASK_DURATION,
            "data": {
                "code_valid": code_valid,
                "missing": missing,
                "completed_verdict": False,
                "start_position": start_pos,
                "max_distance_moved": 0.0
            }
        }

    # ── Position tracking ─────────────────────────────────────────────────────
    pos = robot.get_info().get("position")
    if pos is not None:
        if td["data"]["start_position"] is None:
            td["data"]["start_position"] = pos
        else:
            dx = pos[0] - td["data"]["start_position"][0]
            dy = pos[1] - td["data"]["start_position"][1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > td["data"]["max_distance_moved"]:
                td["data"]["max_distance_moved"] = dist

    # ── Live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        distance = td["data"]["max_distance_moved"]
        
        if td["data"]["code_valid"]:
            # Сообщение об устранении багов висит только пока робот на старте (проехал меньше 2 см)
            if distance < 2.0:
                text = "All bugs fixed! Launching rover..."
            else:
                # Дальше спамится только аккуратная дистанция
                text = f"Racing... Distance: {distance:.1f} cm"
        else:
            # Если есть баги, показываем интригующие названия (максимум 2 за раз, чтобы не ломать UI)
            text = f"Bugs remaining: {', '.join(td['data']['missing'][:2])}..."

    # ── Timeout / Final verdict ───────────────────────────────────────────────
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        distance_moved = td["data"]["max_distance_moved"]
        robot_moved = distance_moved >= MIN_MOVEMENT_DISTANCE
        
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            # Интригующее финальное сообщение без явных подсказок
            result["description"] = f"Mission Failed. Unresolved issues: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code contains bugs!"
            
        elif not robot_moved:
            result["success"] = False
            result["score"] = 20
            result["description"] = f"Code fixed, but robot barely moved ({distance_moved:.1f}cm). Check logic! | Score: 20"
            text = "Robot failed to navigate."
            
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = "You are amazing! All bugs fixed and racing complete | Score: 100"
            text = "Exam Complete!"
