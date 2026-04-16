import cv2
import math
import time
import os
import numpy as np
import ast

target_points = {
    'art_of_debugging': [(50, 94), (30, 0)],           # Start: x=50, y=94, direction=30°
    'hardware_safety_net': [(60, 40), (0, 0)],         # Start: x=60, y=40, direction=0° (spins in place)
    'code_clinic': [(50, 30), (30, 0)],                # Start: x=50, y=30, direction=30°
}

block_library_functions = {
    'art_of_debugging': False,
    'hardware_safety_net': False,
    'code_clinic': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])


# ============================================================================
# Task 6.1: The Art of Debugging
# ============================================================================
def art_of_debugging(robot, frame, td, user_code=None):
    """
    Verification for lesson: The Art of Debugging — 6.1
    Start: x=50, y=94, dir=30°
    Checkpoints: (105, 60), (80, 30)
    """

    # ===== CONFIGURATION =====
    MIN_MOVEMENT_DISTANCE = 30.0  # cm
    CHECKPOINT_RADIUS = 10.0  # cm
    CHECKPOINTS = [(105, 60), (80, 30)]
    # =========================

    # ── default result and text ───────────────────────────────────────────────
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Debugging mission running..."

    frame = robot.draw_info(frame)

    # ── first-frame initialisation ────────────────────────────────────────────
    if td is None:
        # ── code validation ───────────────────────────────────────────────────
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        # Bug detection (progressive hints)
        bugs_remaining = []
        bug_categories = []

        # Bug 1: Missing colon after while True
        has_while_colon = 'while True:' in active_code
        if not has_while_colon:
            bugs_remaining.append('syntax_colon')
            bug_categories.append('SYNTAX')

        # Bug 2: NameError - print(sensor) should be print(sensor_array)
        # Only flag as bug if the WRONG pattern exists
        has_wrong_print = 'print(sensor)' in active_code
        if has_wrong_print:
            bugs_remaining.append('runtime_name')
            bug_categories.append('RUNTIME')

        # Bug 3: Failsafe max(sensor_array) < (not >)
        has_correct_failsafe = 'max(sensor_array) <' in active_code
        has_wrong_failsafe = 'max(sensor_array) >' in active_code
        if has_wrong_failsafe or not has_correct_failsafe:
            bugs_remaining.append('logic_threshold')
            bug_categories.append('LOGIC')

        # Bug 4: P calculation - kp * position (not +)
        has_correct_p = 'kp * position' in active_code or 'position * kp' in active_code
        has_wrong_p = 'kp + position' in active_code
        if has_wrong_p or not has_correct_p:
            bugs_remaining.append('logic_calculation')
            bug_categories.append('LOGIC')

        # Bug 5: Left motor differential - base_speed - P
        has_correct_left = 'base_speed - P' in active_code
        has_wrong_left = 'base_speed + P' in active_code
        left_motor_assignments = active_code.count('base_speed + P')
        if left_motor_assignments > 1 or not has_correct_left:
            bugs_remaining.append('logic_steering')
            bug_categories.append('LOGIC')

        # Bug 6: Method typo - run_motors_speed (not run_motor_speed)
        has_correct_method = 'run_motors_speed' in active_code
        has_wrong_method = 'run_motor_speed' in active_code and not has_correct_method
        if has_wrong_method or not has_correct_method:
            bugs_remaining.append('runtime_method')
            bug_categories.append('RUNTIME')

        bugs_fixed = 6 - len(bugs_remaining)
        code_valid = len(bugs_remaining) == 0

        # Build category summary
        syntax_count = bug_categories.count('SYNTAX')
        runtime_count = bug_categories.count('RUNTIME')
        logic_count = bug_categories.count('LOGIC')
        
        category_summary = []
        if syntax_count > 0:
            category_summary.append(f'SYNTAX ({syntax_count})')
        if runtime_count > 0:
            category_summary.append(f'RUNTIME ({runtime_count})')
        if logic_count > 0:
            category_summary.append(f'LOGIC ({logic_count})')

        # ── td state init ─────────────────────────────────────────────────────
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 60,
            "data": {
                "code_valid": code_valid,
                "bugs_remaining": len(bugs_remaining),
                "bugs_fixed": bugs_fixed,
                "category_summary": ', '.join(category_summary),
                "completed_verdict": False,
                
                "start_position": None,
                "max_distance_moved": 0.0,
                
                "checkpoints_hit": [],
                "checkpoints_remaining": list(CHECKPOINTS),
                
                "flag": None,
                "flag_mask": None,
                "flag_green": None,
                "flag_green_mask": None,
                "image_error": False,
            }
        }

        # ── load checkpoint flag images ───────────────────────────────────────
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "flag_finish.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "flag_finish.jpg")
            flag = cv2.imread(filepath)
            if flag is None:
                raise FileNotFoundError(f"flag_finish.jpg not found")
            flag = cv2.resize(flag, (int(flag.shape[1] / 3), int(flag.shape[0] / 3)))
            mask = cv2.bitwise_not(cv2.inRange(flag,
                                               np.array([0, 240, 0]),
                                               np.array([50, 255, 50])))
            td["data"]["flag"] = flag
            td["data"]["flag_mask"] = mask
            flag_green = flag.copy()
            flag_green[mask > 0] = (0, 200, 0)
            td["data"]["flag_green"] = flag_green
            td["data"]["flag_green_mask"] = mask
        except Exception as e:
            print(f"Flag load error: {e}")
            td["data"]["image_error"] = True

    # ── progressive hints display ─────────────────────────────────────────────
    if td["data"]["bugs_remaining"] > 0:
        text = (f"🐛 Bugs remaining: {td['data']['bugs_remaining']}/6 | "
                f"Types: {td['data']['category_summary']}")

    # ── position tracking ─────────────────────────────────────────────────────
    pos = robot.position
    if pos is not None:
        if td["data"]["start_position"] is None:
            td["data"]["start_position"] = pos
        else:
            dx = pos[0] - td["data"]["start_position"][0]
            dy = pos[1] - td["data"]["start_position"][1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > td["data"]["max_distance_moved"]:
                td["data"]["max_distance_moved"] = dist

    # ── checkpoint detection (sequential) ─────────────────────────────────────
    if pos is not None and td["data"]["checkpoints_remaining"]:
        next_cp = td["data"]["checkpoints_remaining"][0]
        dist = math.sqrt((pos[0] - next_cp[0])**2 + (pos[1] - next_cp[1])**2)
        if dist < CHECKPOINT_RADIUS:
            td["data"]["checkpoints_hit"].append(next_cp)
            td["data"]["checkpoints_remaining"].pop(0)

    # ── live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        distance = td["data"]["max_distance_moved"]
        checkpoints_hit = len(td["data"]["checkpoints_hit"])
        total_checkpoints = len(CHECKPOINTS)
        
        if td["data"]["code_valid"]:
            text = f"Distance: {distance:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}"
        elif distance > 0:
            text = (f"🐛 Bugs: {td['data']['bugs_remaining']}/6 ({td['data']['category_summary']}) | "
                   f"Distance: {distance:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}")

    # ── overlay drawing (checkpoints with flags) ──────────────────────────────
    pos_px = robot.position_px
    if pos is not None and pos_px is not None and pos[0] != 0:
        px_per_cm = pos_px[0] / pos[0]
        radius_px = int(CHECKPOINT_RADIUS * px_per_cm)
        flag = td["data"]["flag"]
        flag_mask = td["data"]["flag_mask"]
        flag_green = td["data"]["flag_green"]
        use_flag = not td["data"]["image_error"] and flag is not None
        hits = td["data"]["checkpoints_hit"]

        for cp_cm in CHECKPOINTS:
            cp_px = (int(cp_cm[0] * px_per_cm), int(cp_cm[1] * px_per_cm))
            hit = cp_cm in hits
            cv2.circle(frame, cp_px, radius_px, (0, 200, 0) if hit else (0, 200, 255), 1)
            
            if use_flag:
                draw_flag = flag_green if hit else flag
                half_w = draw_flag.shape[1] // 2
                half_h = draw_flag.shape[0] // 2
                r0 = cp_px[1] - half_h
                r1 = cp_px[1] + (draw_flag.shape[0] - half_h)
                c0 = cp_px[0] - half_w
                c1 = cp_px[0] + (draw_flag.shape[1] - half_w)
                if 0 <= r0 and r1 < frame.shape[0] and 0 <= c0 and c1 < frame.shape[1]:
                    cv2.copyTo(draw_flag, flag_mask, frame[r0:r1, c0:c1])
            else:
                cv2.circle(frame, cp_px, 5, (0, 200, 0) if hit else (0, 200, 255), -1)

    # ── timeout / final verdict (fires exactly once) ──────────────────────────
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        distance_moved = td["data"]["max_distance_moved"]
        checkpoints_hit = len(td["data"]["checkpoints_hit"])
        total_checkpoints = len(CHECKPOINTS)
        all_checkpoints = checkpoints_hit == total_checkpoints
        
        if td["data"]["code_valid"] and all_checkpoints:
            result["success"] = True
            result["score"] = 100
            result["description"] = (
                f"All bugs fixed! Perfect debugging. "
                f"Checkpoints: {checkpoints_hit}/{total_checkpoints} | Score: 100"
            )
            text = "All bugs fixed! Mission complete!"
        
        elif checkpoints_hit >= 1 and distance_moved >= MIN_MOVEMENT_DISTANCE:
            result["success"] = True
            result["score"] = 85
            result["description"] = (
                f"Good debugging! Distance: {distance_moved:.1f}cm, "
                f"Checkpoints: {checkpoints_hit}/{total_checkpoints} | Score: 85"
            )
            text = "Most bugs fixed, good progress!"
        
        elif td["data"]["bugs_fixed"] > 0:
            partial_score = int((td["data"]["bugs_fixed"] / 6) * 50)
            result["success"] = False
            result["score"] = partial_score
            result["description"] = (
                f"Fixed {td['data']['bugs_fixed']}/6 bugs, but robot didn't complete lap. "
                f"Distance: {distance_moved:.1f}cm | Score: {partial_score}"
            )
            text = f"Fixed {td['data']['bugs_fixed']}/6 bugs. Keep debugging!"
        
        else:
            result["success"] = False
            result["score"] = 0
            result["description"] = "No bugs fixed. Review the code carefully! | Score: 0"
            text = "Start debugging! Find and fix the 6 bugs."

    return frame, td, text, result


# ============================================================================
# Task 6.2: The Hardware Safety Net
# ============================================================================
def hardware_safety_net(robot, frame, td, user_code=None):
    """
    Verification for lesson: The Hardware Safety Net — 6.2
    Start: x=60, y=40, dir=0°
    No checkpoints (robot spins in place)
    """

    # ===== CONFIGURATION =====
    MIN_ROTATION = 10.0  # cm - robot must move (spinning counts)
    EXPECTED_SCANS = 10
    MIN_SCANS_SUCCESS = 9
    # =========================

    # ── default result and text ───────────────────────────────────────────────
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Processing scans..."

    frame = robot.draw_info(frame)

    # ── first-frame initialisation ────────────────────────────────────────────
    if td is None:
        # ── code validation ───────────────────────────────────────────────────
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        missing = []
        
        has_try = 'try:' in active_code
        if not has_try:
            missing.append('try: block')
        
        has_except_zero = 'except ZeroDivisionError' in active_code
        if not has_except_zero:
            missing.append('except ZeroDivisionError:')
        
        has_error_print = 'CRITICAL' in active_code or 'Sensor Blind' in active_code
        if not has_error_print:
            missing.append('error warning message')
        
        has_return_unknown = 'return "Unknown"' in active_code or "return 'Unknown'" in active_code
        if not has_return_unknown:
            missing.append('return "Unknown"')
        
        code_valid = len(missing) == 0

        # ── td state init ─────────────────────────────────────────────────────
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 30,
            "data": {
                "code_valid": code_valid,
                "missing": missing,
                "completed_verdict": False,
                
                "start_position": None,
                "max_distance_moved": 0.0,
                
                "scans_received": 0,
                "sector_messages": [],
                "analysis_messages": [],
                "unknown_detections": 0,
                "completion_message": False,
            }
        }

    # ── code invalid notice ───────────────────────────────────────────────────
    if not td["data"]["code_valid"]:
        text = f"Missing: {', '.join(td['data']['missing'])}"

    # ── position tracking ─────────────────────────────────────────────────────
    pos = robot.position
    if pos is not None:
        if td["data"]["start_position"] is None:
            td["data"]["start_position"] = pos
        else:
            dx = pos[0] - td["data"]["start_position"][0]
            dy = pos[1] - td["data"]["start_position"][1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > td["data"]["max_distance_moved"]:
                td["data"]["max_distance_moved"] = dist

    # ── MQTT message parsing ──────────────────────────────────────────────────
    msg = robot.get_msg()
    if msg is not None:
        if "Sector #" in msg:
            td["data"]["sector_messages"].append(msg)
            td["data"]["scans_received"] += 1
        
        elif "ANALYSIS:" in msg:
            td["data"]["analysis_messages"].append(msg)
            if "Unknown" in msg:
                td["data"]["unknown_detections"] += 1
        
        elif "Survey Complete" in msg or "Complete" in msg:
            td["data"]["completion_message"] = True

    # ── live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        scans = td["data"]["scans_received"]
        unknowns = td["data"]["unknown_detections"]
        
        if td["data"]["code_valid"]:
            text = f"Scans: {scans}/{EXPECTED_SCANS}, Shadow zones handled: {unknowns}/4"
        else:
            text = f"Fix code first! Missing: {', '.join(td['data']['missing'][:2])}..."

    # ── timeout / final verdict (fires exactly once) ──────────────────────────
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        distance_moved = td["data"]["max_distance_moved"]
        scans_received = td["data"]["scans_received"]
        unknown_count = td["data"]["unknown_detections"]
        
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = (
                f"Code missing try-except: {', '.join(td['data']['missing'])} | Score: 0"
            )
            text = "Implement try-except block first!"
        
        elif scans_received >= EXPECTED_SCANS and unknown_count >= 3:
            result["success"] = True
            result["score"] = 100
            result["description"] = (
                f"Perfect! Processed {scans_received} scans, "
                f"handled {unknown_count}/4 shadow zones gracefully. "
                f"No crashes! | Score: 100"
            )
            text = "All scans completed! Safety net working!"
        
        elif scans_received >= MIN_SCANS_SUCCESS and unknown_count >= 2:
            result["success"] = True
            result["score"] = 85
            result["description"] = (
                f"Good! Processed {scans_received}/{EXPECTED_SCANS} scans, "
                f"handled {unknown_count} shadow zones. | Score: 85"
            )
            text = "Try-except working! Almost all scans completed."
        
        elif scans_received >= MIN_SCANS_SUCCESS:
            result["success"] = True
            result["score"] = 70
            result["description"] = (
                f"Scans completed ({scans_received}), but only {unknown_count}/4 "
                f"shadow zones returned 'Unknown'. Check try-except implementation. | Score: 70"
            )
            text = "Code runs, but error handling might be incomplete."
        
        elif scans_received > 5:
            result["success"] = False
            result["score"] = 50
            result["description"] = (
                f"Robot processed {scans_received}/{EXPECTED_SCANS} scans, "
                f"but task incomplete. Did program crash on (0,0,0)? | Score: 50"
            )
            text = "Partial execution. Likely crashed on shadow zone."
        
        else:
            result["success"] = False
            result["score"] = 0
            result["description"] = (
                f"Robot moved {distance_moved:.1f}cm, only {scans_received} scans received. "
                f"Code crashed early - add try-except! | Score: 0"
            )
            text = "Task failed. Code likely crashed on first (0,0,0)."

    return frame, td, text, result


# ============================================================================
# Task 6.3: Code Clinic (Refactoring)
# ============================================================================
def code_clinic(robot, frame, td, user_code=None):
    """
    Verification for lesson: Code Clinic (Refactoring) — 6.3
    Start: x=50, y=30, dir=0°
    Checkpoints: (105, 60), (60, 90), (80, 30)
    """

    # ===== CONFIGURATION =====
    MIN_MOVEMENT_DISTANCE = 30.0  # cm
    CHECKPOINT_RADIUS = 10.0  # cm
    CHECKPOINTS = [(105, 60), (60, 90), (80, 30)]
    # =========================

    # ── default result and text ───────────────────────────────────────────────
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Refactoring mission running..."

    frame = robot.draw_info(frame)

    # ── first-frame initialisation ────────────────────────────────────────────
    if td is None:
        # ── AST-based code validation ─────────────────────────────────────────
        missing = []
        code_valid = False
        
        try:
            tree = ast.parse(user_code)
            
            # Find UPPERCASE constants
            constants = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            constants.add(target.id)
            
            # Check required constants
            if 'SENSITIVITY' not in constants:
                missing.append('SENSITIVITY constant')
            if not any(c in constants for c in ['LINE_LIMIT', 'LINE_THRESHOLD']):
                missing.append('LINE_LIMIT constant')
            if 'BASE_SPEED' not in constants:
                missing.append('BASE_SPEED constant')
            if not any(c in constants for c in ['KP', 'Kp']):
                missing.append('KP constant')
            
            # Find functions with properties
            functions = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    has_try = any(isinstance(n, ast.Try) for n in ast.walk(node))
                    params = [arg.arg for arg in node.args.args]
                    
                    functions[node.name] = {
                        'has_try_except': has_try,
                        'params': params
                    }
            
            # Check required functions
            if 'get_mineral_color' not in functions:
                missing.append('get_mineral_color() function')
            elif not functions['get_mineral_color']['has_try_except']:
                missing.append('try-except in get_mineral_color()')
            
            if 'calculate_steering' not in functions:
                missing.append('calculate_steering() function')
            
            if 'apply_movement' not in functions:
                missing.append('apply_movement() function')
            
            code_valid = len(missing) == 0
            
        except SyntaxError as e:
            missing.append(f'syntax error at line {e.lineno}')
            code_valid = False

        # ── td state init ─────────────────────────────────────────────────────
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 60,
            "data": {
                "code_valid": code_valid,
                "missing": missing,
                "completed_verdict": False,
                
                "start_position": None,
                "max_distance_moved": 0.0,
                
                "checkpoints_hit": [],
                "checkpoints_remaining": list(CHECKPOINTS),
                
                "minerals_detected": [],
                
                "flag": None,
                "flag_mask": None,
                "flag_green": None,
                "flag_green_mask": None,
                "image_error": False,
            }
        }

        # ── load checkpoint flag images ───────────────────────────────────────
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "flag_finish.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "flag_finish.jpg")
            
            flag = cv2.imread(filepath)
            if flag is None:
                raise FileNotFoundError(f"flag_finish.jpg not found")
            
            flag = cv2.resize(flag, (int(flag.shape[1] / 3), int(flag.shape[0] / 3)))
            mask = cv2.bitwise_not(cv2.inRange(flag,
                                               np.array([0, 240, 0]),
                                               np.array([50, 255, 50])))
            td["data"]["flag"] = flag
            td["data"]["flag_mask"] = mask
            
            flag_green = flag.copy()
            flag_green[mask > 0] = (0, 200, 0)
            td["data"]["flag_green"] = flag_green
            td["data"]["flag_green_mask"] = mask
        except Exception as e:
            print(f"Flag load error: {e}")
            td["data"]["image_error"] = True

    # ── code invalid notice ───────────────────────────────────────────────────
    if not td["data"]["code_valid"]:
        text = f"Missing refactoring: {', '.join(td['data']['missing'][:3])}..."

    # ── position tracking ─────────────────────────────────────────────────────
    pos = robot.position
    if pos is not None:
        if td["data"]["start_position"] is None:
            td["data"]["start_position"] = pos
        else:
            dx = pos[0] - td["data"]["start_position"][0]
            dy = pos[1] - td["data"]["start_position"][1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist > td["data"]["max_distance_moved"]:
                td["data"]["max_distance_moved"] = dist

    # ── checkpoint detection (sequential) ─────────────────────────────────────
    if pos is not None and td["data"]["checkpoints_remaining"]:
        next_cp = td["data"]["checkpoints_remaining"][0]
        dist = math.sqrt((pos[0] - next_cp[0])**2 + (pos[1] - next_cp[1])**2)
        if dist < CHECKPOINT_RADIUS:
            td["data"]["checkpoints_hit"].append(next_cp)
            td["data"]["checkpoints_remaining"].pop(0)

    # ── MQTT message parsing ──────────────────────────────────────────────────
    msg = robot.get_msg()
    if msg is not None:
        if "Mineral Detected" in msg or "mineral" in msg.lower():
            if msg not in td["data"]["minerals_detected"]:
                td["data"]["minerals_detected"].append(msg)

    # ── live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        distance = td["data"]["max_distance_moved"]
        checkpoints_hit = len(td["data"]["checkpoints_hit"])
        total_checkpoints = len(CHECKPOINTS)
        minerals = len(td["data"]["minerals_detected"])
        
        if td["data"]["code_valid"]:
            text = (f"Distance: {distance:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}, "
                   f"Minerals: {minerals}")
        else:
            text = f"Refactor code first! Missing: {', '.join(td['data']['missing'][:2])}..."

    # ── overlay drawing (checkpoints with flags) ──────────────────────────────
    pos_px = robot.position_px
    if pos is not None and pos_px is not None and pos[0] != 0:
        px_per_cm = pos_px[0] / pos[0]
        radius_px = int(CHECKPOINT_RADIUS * px_per_cm)
        
        flag = td["data"]["flag"]
        flag_mask = td["data"]["flag_mask"]
        flag_green = td["data"]["flag_green"]
        use_flag = not td["data"]["image_error"] and flag is not None
        hits = td["data"]["checkpoints_hit"]

        for cp_cm in CHECKPOINTS:
            cp_px = (int(cp_cm[0] * px_per_cm), int(cp_cm[1] * px_per_cm))
            hit = cp_cm in hits
            
            cv2.circle(frame, cp_px, radius_px, (0, 200, 0) if hit else (0, 200, 255), 1)
            
            if use_flag:
                draw_flag = flag_green if hit else flag
                half_w = draw_flag.shape[1] // 2
                half_h = draw_flag.shape[0] // 2
                r0 = cp_px[1] - half_h
                r1 = cp_px[1] + (draw_flag.shape[0] - half_h)
                c0 = cp_px[0] - half_w
                c1 = cp_px[0] + (draw_flag.shape[1] - half_w)
                
                if 0 <= r0 and r1 < frame.shape[0] and 0 <= c0 and c1 < frame.shape[1]:
                    cv2.copyTo(draw_flag, flag_mask, frame[r0:r1, c0:c1])
            else:
                cv2.circle(frame, cp_px, 5, (0, 200, 0) if hit else (0, 200, 255), -1)

    # ── timeout / final verdict (fires exactly once) ──────────────────────────
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        distance_moved = td["data"]["max_distance_moved"]
        robot_moved = distance_moved >= MIN_MOVEMENT_DISTANCE
        checkpoints_hit = len(td["data"]["checkpoints_hit"])
        total_checkpoints = len(CHECKPOINTS)
        all_checkpoints = checkpoints_hit == total_checkpoints
        minerals_found = len(td["data"]["minerals_detected"])
        
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = (
                f"Code not refactored: {', '.join(td['data']['missing'])} | Score: 0"
            )
            text = "Complete refactoring requirements first!"
        
        elif all_checkpoints and minerals_found >= 1:
            result["success"] = True
            result["score"] = 100
            result["description"] = (
                f"Perfect refactoring! Clean code, all checkpoints hit, "
                f"{minerals_found} minerals detected! | Score: 100"
            )
            text = "Clean code works perfectly!"
        
        elif checkpoints_hit >= 2 and robot_moved:
            result["success"] = True
            result["score"] = 85
            result["description"] = (
                f"Good refactoring! Checkpoints: {checkpoints_hit}/{total_checkpoints}, "
                f"Minerals: {minerals_found} | Score: 85"
            )
            text = "Refactored code working well!"
        
        elif robot_moved:
            result["success"] = True
            result["score"] = 70
            result["description"] = (
                f"Code refactored, robot moved {distance_moved:.1f}cm, "
                f"but only {checkpoints_hit}/{total_checkpoints} checkpoints | Score: 70"
            )
            text = "Refactoring complete, navigation needs tuning."
        
        else:
            result["success"] = False
            result["score"] = 30
            result["description"] = (
                f"Code refactored, but robot barely moved ({distance_moved:.1f}cm). "
                f"Check for bugs! | Score: 30"
            )
            text = "Refactoring done, but code has bugs."

    return frame, td, text, result
