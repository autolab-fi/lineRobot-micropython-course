import cv2
import math
import time
import os
import numpy as np
import re

target_points = {
    'concept_of_error': [(22, 86),(0,-30)],           # Start: x=22, y=86, direction=-30
    'upgraded_relay_controller': [(40, 30), (30, 0)],   # Start: x=40, y=30
    'proportional_control': [(40, 30),(30, 0)],        # Start: x=40, y=30
    'tuning_and_kick': [(40, 30),(30, 0)],             # Start: x=40, y=30
    'adaptive_speed': [(40, 30),(30, 0)],              # Start: x=40, y=30
}

block_library_functions = {
    'concept_of_error': False,
    'upgraded_relay_controller': False,
    'proportional_control': False,
    'tuning_and_kick': False,
    'adaptive_speed': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])



# ============================================================================
# Task 5.1: Concept of Error
# ============================================================================
def concept_of_error(robot, image, td, user_code=None):
    """
    Verification for lesson: Concept of Error — 5.1
    Start: x=22, y=86, direction=-30
    """

    # ===== CONFIGURATION =====
    #TASK_DURATION = 30
    
    # Movement tracking
    MIN_FORWARD_DISTANCE = 25.0  # cm (target is 30cm, allow some tolerance)
    MAX_FORWARD_DISTANCE = 35.0  # cm
    
    # MQTT message tracking
    MIN_ERROR_MESSAGES = 8  # Each sweep prints 5 messages, expect at least 8 total
    # =========================

    # ── default result and text ───────────────────────────────────────────────
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for messages..."

    image = robot.draw_info(image)

    # ── first-frame initialisation ────────────────────────────────────────────
    if td is None:
        # ── code validation ───────────────────────────────────────────────────
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_track_line      = 'octoliner.track_line()' in active_code
        has_error_print     = 'print' in active_code and 'Error' in active_code
        sweep_count         = active_code.count('diagnostic_sweep(')
        has_two_sweeps      = sweep_count >= 2
        has_forward_move    = 'move_forward_distance(30)' in active_code
        
        code_valid = (
            has_track_line and has_error_print and has_two_sweeps and has_forward_move
        )

        missing = []
        if not has_track_line:   missing.append('octoliner.track_line()')
        if not has_error_print:  missing.append('print("Error:", ...)')
        if not has_two_sweeps:   missing.append('two diagnostic_sweep() calls')
        if not has_forward_move: missing.append('move_forward_distance(30)')

        # ── td state init ─────────────────────────────────────────────────────
        td = {
            "start_time": time.time(),
            "end_time":   time.time() + 10,
            "data": {
                "code_valid":            code_valid,
                "missing":               missing,
                "completed_verdict":     False,
                
                # Position tracking
                "start_position":        None,
                "max_distance_moved":    0.0,
                
                # MQTT message tracking
                "error_messages":        [],
                "error_values":          [],
                "left_sweep_values":     [],
                "right_sweep_values":    [],
                "left_sweep_detected":   False,
                "right_sweep_detected":  False,
                "last_message":          None,
                "sweep_phase":           "first",  # "first", "forward", "second"
            }
        }

    # ── code invalid notice ───────────────────────────────────────────────────
    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

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
        td["data"]["last_message"] = msg
        
        # Look for "Error: <value>" pattern
        match = re.search(r'Error:\s*([-+]?[0-9]*\.?[0-9]+)', msg)
        if match:
            error_value = float(match.group(1))
            td["data"]["error_messages"].append(msg)
            td["data"]["error_values"].append(error_value)
            
            # Separate errors by sweep phase (no value checking, just collect)
            if td["data"]["sweep_phase"] == "first":
                td["data"]["left_sweep_values"].append(error_value)
                    
            elif td["data"]["sweep_phase"] == "second":
                td["data"]["right_sweep_values"].append(error_value)
        
        # Detect phase transitions and sweep completion from MQTT messages
        if "Starting sweep" in msg:
            if td["data"]["sweep_phase"] == "first":
                td["data"]["left_sweep_detected"] = True
            elif td["data"]["sweep_phase"] == "forward":
                td["data"]["sweep_phase"] = "second"
                td["data"]["right_sweep_detected"] = True
                
        if "Sweep complete" in msg and td["data"]["sweep_phase"] == "first":
            td["data"]["sweep_phase"] = "forward"

    # ── live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        if td["data"]["last_message"] is not None:
            text = f"Last message: {td['data']['last_message']}"
        
        error_count = len(td["data"]["error_messages"])
        distance = td["data"]["max_distance_moved"]
        if error_count > 0 or distance > 0:
            text = f"Last message: {td['data']['last_message']} | Position errors: {error_count}, Distance: {distance:.1f}cm"

    # ── timeout / final verdict (fires exactly once) ──────────────────────────
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        
        else:
            # Evaluate mission performance
            error_count = len(td["data"]["error_messages"])
            distance_moved = td["data"]["max_distance_moved"]
            left_values = td["data"]["left_sweep_values"]
            right_values = td["data"]["right_sweep_values"]
            
            # Format sweep gradients for display
            left_gradient = ", ".join([f"{v:.2f}" for v in left_values]) if left_values else "none"
            right_gradient = ", ".join([f"{v:.2f}" for v in right_values]) if right_values else "none"
            
            # Success criteria
            has_enough_messages = error_count >= MIN_ERROR_MESSAGES
            moved_correct_distance = MIN_FORWARD_DISTANCE <= distance_moved <= MAX_FORWARD_DISTANCE
            detected_sweeps = td["data"]["left_sweep_detected"] and td["data"]["right_sweep_detected"]
            robot_moved = distance_moved > 5.0  # Robot moved at all
            
            if has_enough_messages and moved_correct_distance and detected_sweeps:
                result["success"]     = True
                result["score"]       = 100
                result["description"] = f"Perfect! Left sweep: [{left_gradient}], Right sweep: [{right_gradient}] | Distance: {distance_moved:.1f}cm | Score: 100"
                text = f"Mission complete! Left: [{left_gradient}], Right: [{right_gradient}]"
            
            elif has_enough_messages and detected_sweeps:
                # Got the error messages but movement was off
                result["success"]     = False
                result["score"]       = 70
                result["description"] = f"Error gradient correct. Left: [{left_gradient}], Right: [{right_gradient}] | Distance: {distance_moved:.1f}cm (expected ~30cm) | Score: 70"
                text = f"Error tracking successful. Left: [{left_gradient}], Right: [{right_gradient}]"
            
            elif has_enough_messages:
                # Got messages but didn't detect proper sweep gradient
                result["success"]     = False
                result["score"]       = 50
                result["description"] = f"Received {error_count} messages. Left: [{left_gradient}], Right: [{right_gradient}] | Sweeps unclear | Score: 50"
                text = f"Error messages received. Left: [{left_gradient}], Right: [{right_gradient}]"
            
            elif robot_moved:
                # Robot moved but no error messages
                result["success"]     = False
                result["score"]       = 30
                result["description"] = f"Robot moved {distance_moved:.1f}cm but no error messages detected | Score: 30"
                text = "Robot moved but error printing not working."
            
            else:
                # Nothing happened
                result["success"]     = False
                result["score"]       = 0
                result["description"] = f"Task incomplete. Messages: {error_count}, Distance: {distance_moved:.1f}cm | Score: 0"
                text = "Task incomplete. Check code execution."

    return image, td, text, result


# ============================================================================
# Task 5.2: Upgraded Relay Controller
# ============================================================================
def upgraded_relay_controller(robot, image, td, user_code=None):
    """
    Verification for lesson: Upgraded Relay Controller — 5.2
    Start: x=40, y=30
    Checkpoints: (105, 60), (60, 90), (80, 30) - visual feedback only
    """

    # ===== CONFIGURATION =====
    #TASK_DURATION = 90 #Just a reference
    
    # Movement tracking
    MIN_MOVEMENT_DISTANCE = 30.0  # cm - should move at least this far
    
    # Checkpoints (visual only, not required for scoring)
    CHECKPOINT_RADIUS = 10.0  # cm
    CHECKPOINTS = [(105, 60), (60, 90), (80, 30)]  # Full lap challenge
    # =========================

    # ── default result and text ───────────────────────────────────────────────
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for messages..."

    image = robot.draw_info(image)

    # ── first-frame initialisation ────────────────────────────────────────────
    if td is None:
        # ── code validation ───────────────────────────────────────────────────
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_while_true      = 'while True' in active_code
        has_analog_read     = 'analog_read_all()' in active_code
        has_track_line      = 'track_line()' in active_code
        has_max_check       = 'max(' in active_code and '< 700' in active_code
        has_robot_stop      = 'robot.stop()' in active_code
        has_break           = 'break' in active_code
        has_left_threshold  = '< -0.3' in active_code or '<-0.3' in active_code
        has_right_threshold = '> 0.3' in active_code or '>0.3' in active_code
        
        code_valid = (
            has_while_true and has_analog_read and has_track_line
            and has_max_check and has_robot_stop and has_break
            and has_left_threshold and has_right_threshold
        )

        missing = []
        if not has_while_true:      missing.append('while True loop')
        if not has_analog_read:     missing.append('analog_read_all()')
        if not has_track_line:      missing.append('track_line()')
        if not has_max_check:       missing.append('max(sensor_array) < 700 failsafe')
        if not has_robot_stop:      missing.append('robot.stop()')
        if not has_break:           missing.append('break statement')
        if not has_left_threshold:  missing.append('left threshold (< -0.3)')
        if not has_right_threshold: missing.append('right threshold (> 0.3)')

        # ── td state init ─────────────────────────────────────────────────────
        td = {
            "start_time": time.time(),
            "end_time":   time.time() + 90,
            "data": {
                "code_valid":            code_valid,
                "missing":               missing,
                "completed_verdict":     False,
                
                # Position tracking
                "start_position":        None,
                "max_distance_moved":    0.0,
                
                # MQTT message tracking
                "last_message":          None,
                "critical_message_seen": False,
                
                # Checkpoint tracking (visual only)
                "checkpoints_hit":       [],
                "checkpoints_remaining": list(CHECKPOINTS),
                
                # Flag image assets
                "flag":                  None,
                "flag_mask":             None,
                "flag_green":            None,
                "flag_green_mask":       None,
                "image_error":           False,
            }
        }

        # ── flag image loading (dual-path fallback) ───────────────────────────
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "flag_finish.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "flag_finish.jpg")
            flag = cv2.imread(filepath)
            if flag is None:
                raise FileNotFoundError(f"flag_finish.jpg not found at {filepath}")
            flag = cv2.resize(flag, (int(flag.shape[1] / 3), int(flag.shape[0] / 3)))
            mask = cv2.bitwise_not(cv2.inRange(flag,
                                               np.array([0, 240, 0]),
                                               np.array([50, 255, 50])))
            td["data"]["flag"]      = flag
            td["data"]["flag_mask"] = mask
            flag_green = flag.copy()
            flag_green[mask > 0] = (0, 200, 0)
            td["data"]["flag_green"]      = flag_green
            td["data"]["flag_green_mask"] = mask
        except Exception as e:
            print(f"Flag load error: {e} — falling back to circle markers")
            td["data"]["image_error"] = True

    # ── code invalid notice ───────────────────────────────────────────────────
    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

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

    # ── checkpoint detection (visual feedback only) ───────────────────────────
    if pos is not None and td["data"]["checkpoints_remaining"]:
        next_cp = td["data"]["checkpoints_remaining"][0]
        dist = math.sqrt((pos[0] - next_cp[0])**2 + (pos[1] - next_cp[1])**2)
        if dist < CHECKPOINT_RADIUS:
            td["data"]["checkpoints_hit"].append(next_cp)
            td["data"]["checkpoints_remaining"].pop(0)

    # ── MQTT message parsing ──────────────────────────────────────────────────
    msg = robot.get_msg()
    if msg is not None:
        td["data"]["last_message"] = msg
        
        # Detect failsafe trigger
        if "CRITICAL" in msg or "Line lost" in msg or "Emergency Stop" in msg:
            td["data"]["critical_message_seen"] = True

    # ── live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        if td["data"]["last_message"] is not None:
            text = f"Last message: {td['data']['last_message']}"
        
        distance = td["data"]["max_distance_moved"]
        checkpoints_hit = len(td["data"]["checkpoints_hit"])
        total_checkpoints = len(CHECKPOINTS)
        
        if distance > 0:
            text = f"Last message: {td['data']['last_message']} | Distance: {distance:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}"

    # ── overlay drawing (checkpoints with flags) ──────────────────────────────
    pos_px = robot.position_px
    if pos is not None and pos_px is not None and pos[0] != 0:
        px_per_cm  = pos_px[0] / pos[0]
        radius_px  = int(CHECKPOINT_RADIUS * px_per_cm)
        flag       = td["data"]["flag"]
        flag_mask  = td["data"]["flag_mask"]
        flag_green = td["data"]["flag_green"]
        use_flag   = not td["data"]["image_error"] and flag is not None
        hits       = td["data"]["checkpoints_hit"]

        for cp_cm in CHECKPOINTS:
            cp_px = (int(cp_cm[0] * px_per_cm), int(cp_cm[1] * px_per_cm))
            hit   = cp_cm in hits
            cv2.circle(image, cp_px, radius_px, (0, 200, 0) if hit else (0, 200, 255), 1)
            
            if use_flag:
                draw_flag = flag_green if hit else flag
                half_w = draw_flag.shape[1] // 2
                half_h = draw_flag.shape[0] // 2
                r0 = cp_px[1] - half_h
                r1 = cp_px[1] + (draw_flag.shape[0] - half_h)
                c0 = cp_px[0] - half_w
                c1 = cp_px[0] + (draw_flag.shape[1] - half_w)
                if 0 <= r0 and r1 < image.shape[0] and 0 <= c0 and c1 < image.shape[1]:
                    cv2.copyTo(draw_flag, flag_mask, image[r0:r1, c0:c1])
            else:
                cv2.circle(image, cp_px, 5, (0, 200, 0) if hit else (0, 200, 255), -1)

    # ── timeout / final verdict (fires exactly once) ──────────────────────────
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        
        else:
            # Evaluate mission performance
            distance_moved = td["data"]["max_distance_moved"]
            robot_moved = distance_moved >= MIN_MOVEMENT_DISTANCE
            checkpoints_hit = len(td["data"]["checkpoints_hit"])
            total_checkpoints = len(CHECKPOINTS)
            
            # Success criteria
            if robot_moved:
                result["success"]     = True
                result["score"]       = 100
                result["description"] = f"Perfect! Relay controller working. Distance: {distance_moved:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints} | Score: 100"
                text = f"Mission complete! Distance: {distance_moved:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}"
            
            elif distance_moved >= 10.0:
                # Robot moved some but not enough
                result["success"]     = False
                result["score"]       = 60
                result["description"] = f"Robot moved {distance_moved:.1f}cm (expected ≥{MIN_MOVEMENT_DISTANCE}cm), Checkpoints: {checkpoints_hit}/{total_checkpoints} | Score: 60"
                text = f"Relay controller works but robot stopped early. Checkpoints: {checkpoints_hit}/{total_checkpoints}"
            
            else:
                # Robot barely moved
                result["success"]     = False
                result["score"]       = 0
                result["description"] = f"Robot barely moved ({distance_moved:.1f}cm) | Score: 0"
                text = "Task incomplete. Check code execution."

    return image, td, text, result


# ============================================================================
# Task 5.3: Proportional Control
# ============================================================================
def proportional_control(robot, image, td, user_code=None):
    """
    Verification for lesson: Proportional Control — 5.3
    Start: x=40, y=30
    Checkpoints: (105, 60), (60, 90), (80, 30) - visual feedback only
    """

    # ===== CONFIGURATION =====
    TASK_DURATION = 60
    
    # Movement tracking
    MIN_MOVEMENT_DISTANCE = 10.0  # cm - anti-cheat minimum
    
    # Checkpoints (visual only, not required for scoring)
    CHECKPOINT_RADIUS = 10.0  # cm
    CHECKPOINTS = [(105, 60), (60, 90), (80, 30)]  # Full lap challenge
    # =========================

    # ── default result and text ───────────────────────────────────────────────
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for messages..."

    image = robot.draw_info(image)

    # ── first-frame initialisation ────────────────────────────────────────────
    if td is None:
        # ── code validation ───────────────────────────────────────────────────
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_while_true      = 'while True' in active_code
        has_analog_read     = 'analog_read_all()' in active_code
        has_track_line      = 'track_line()' in active_code
        has_max_check       = 'max(' in active_code and '< 700' in active_code
        has_robot_stop      = 'robot.stop()' in active_code
        has_break           = 'break' in active_code
        
        # P-controller checks
        has_base_speed = 'base_speed' in active_code
        has_kp         = 'kp' in active_code or 'Kp' in active_code or 'KP' in active_code
        has_p_calc     = '* position' in active_code  # P = kp * position
        has_left_speed = 'left_speed' in active_code
        has_right_speed = 'right_speed' in active_code
        has_add_subtract = ('+' in active_code and '-' in active_code)
        
        code_valid = (
            has_while_true and has_analog_read and has_track_line
            and has_max_check and has_robot_stop and has_break
            and has_base_speed and has_kp and has_p_calc
            and has_left_speed and has_right_speed and has_add_subtract
        )

        missing = []
        if not has_while_true:      missing.append('while True loop')
        if not has_analog_read:     missing.append('analog_read_all()')
        if not has_track_line:      missing.append('track_line()')
        if not has_max_check:       missing.append('max(sensor_array) < 700 failsafe')
        if not has_robot_stop:      missing.append('robot.stop()')
        if not has_break:           missing.append('break statement')
        if not has_base_speed:      missing.append('base_speed variable')
        if not has_kp:              missing.append('kp variable')
        if not has_p_calc:          missing.append('P = kp * position')
        if not has_left_speed:      missing.append('left_speed calculation')
        if not has_right_speed:     missing.append('right_speed calculation')
        if not has_add_subtract:    missing.append('+ and - operations for steering')

        # ── td state init ─────────────────────────────────────────────────────
        td = {
            "start_time": time.time(),
            "end_time":   time.time() + 60,
            "data": {
                "code_valid":               code_valid,
                "missing":                  missing,
                "completed_verdict":        False,
                
                # Position tracking
                "start_position":           None,
                "max_distance_moved":       0.0,
                
                # MQTT message tracking
                "last_message":             None,
                
                # Checkpoint tracking (visual only)
                "checkpoints_hit":          [],
                "checkpoints_remaining":    list(CHECKPOINTS),
                
                # Flag image assets
                "flag":                     None,
                "flag_mask":                None,
                "flag_green":               None,
                "flag_green_mask":          None,
                "image_error":              False,
            }
        }

        # ── flag image loading (dual-path fallback) ───────────────────────────
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "flag_finish.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "flag_finish.jpg")
            flag = cv2.imread(filepath)
            if flag is None:
                raise FileNotFoundError(f"flag_finish.jpg not found at {filepath}")
            flag = cv2.resize(flag, (int(flag.shape[1] / 3), int(flag.shape[0] / 3)))
            mask = cv2.bitwise_not(cv2.inRange(flag,
                                               np.array([0, 240, 0]),
                                               np.array([50, 255, 50])))
            td["data"]["flag"]      = flag
            td["data"]["flag_mask"] = mask
            flag_green = flag.copy()
            flag_green[mask > 0] = (0, 200, 0)
            td["data"]["flag_green"]      = flag_green
            td["data"]["flag_green_mask"] = mask
        except Exception as e:
            print(f"Flag load error: {e} — falling back to circle markers")
            td["data"]["image_error"] = True

    # ── code invalid notice ───────────────────────────────────────────────────
    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

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

    # ── checkpoint detection (visual feedback only) ───────────────────────────
    if pos is not None and td["data"]["checkpoints_remaining"]:
        next_cp = td["data"]["checkpoints_remaining"][0]
        dist = math.sqrt((pos[0] - next_cp[0])**2 + (pos[1] - next_cp[1])**2)
        if dist < CHECKPOINT_RADIUS:
            td["data"]["checkpoints_hit"].append(next_cp)
            td["data"]["checkpoints_remaining"].pop(0)

    # ── MQTT message parsing ──────────────────────────────────────────────────
    msg = robot.get_msg()
    if msg is not None:
        td["data"]["last_message"] = msg

    # ── live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        if td["data"]["last_message"] is not None:
            text = f"Last message: {td['data']['last_message']}"
        
        distance = td["data"]["max_distance_moved"]
        checkpoints_hit = len(td["data"]["checkpoints_hit"])
        total_checkpoints = len(CHECKPOINTS)
        
        if distance > 0:
            text = f"Last message: {td['data']['last_message']} | Distance: {distance:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}"

    # ── overlay drawing (checkpoints with flags) ──────────────────────────────
    pos_px = robot.position_px
    if pos is not None and pos_px is not None and pos[0] != 0:
        px_per_cm  = pos_px[0] / pos[0]
        radius_px  = int(CHECKPOINT_RADIUS * px_per_cm)
        flag       = td["data"]["flag"]
        flag_mask  = td["data"]["flag_mask"]
        flag_green = td["data"]["flag_green"]
        use_flag   = not td["data"]["image_error"] and flag is not None
        hits       = td["data"]["checkpoints_hit"]

        for cp_cm in CHECKPOINTS:
            cp_px = (int(cp_cm[0] * px_per_cm), int(cp_cm[1] * px_per_cm))
            hit   = cp_cm in hits
            cv2.circle(image, cp_px, radius_px, (0, 200, 0) if hit else (0, 200, 255), 1)
            
            if use_flag:
                draw_flag = flag_green if hit else flag
                half_w = draw_flag.shape[1] // 2
                half_h = draw_flag.shape[0] // 2
                r0 = cp_px[1] - half_h
                r1 = cp_px[1] + (draw_flag.shape[0] - half_h)
                c0 = cp_px[0] - half_w
                c1 = cp_px[0] + (draw_flag.shape[1] - half_w)
                if 0 <= r0 and r1 < image.shape[0] and 0 <= c0 and c1 < image.shape[1]:
                    cv2.copyTo(draw_flag, flag_mask, image[r0:r1, c0:c1])
            else:
                cv2.circle(image, cp_px, 5, (0, 200, 0) if hit else (0, 200, 255), -1)

    # ── timeout / final verdict (fires exactly once) ──────────────────────────
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        
        else:
            # Evaluate mission performance
            distance_moved = td["data"]["max_distance_moved"]
            robot_moved = distance_moved >= MIN_MOVEMENT_DISTANCE
            checkpoints_hit = len(td["data"]["checkpoints_hit"])
            total_checkpoints = len(CHECKPOINTS)
            
            # Success criteria
            if robot_moved:
                result["success"]     = True
                result["score"]       = 100
                result["description"] = f"Perfect! P-controller working. Distance: {distance_moved:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints} | Score: 100"
                text = f"Mission complete! Distance: {distance_moved:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}"
            
            else:
                # Robot didn't move
                result["success"]     = False
                result["score"]       = 0
                result["description"] = f"Robot barely moved ({distance_moved:.1f}cm) | Score: 0"
                text = "Task incomplete. Check code execution."

    return image, td, text, result


# ============================================================================
# Task 5.4: Tuning and Kick
# ============================================================================
def tuning_and_kick(robot, image, td, user_code=None):
    """
    Verification for lesson: Tuning and Kick — 5.4
    Start: x=40, y=30
    """

    # ===== CONFIGURATION =====
    TASK_DURATION = 30
    
    # Movement tracking
    MIN_MOVEMENT_DISTANCE = 10.0  # cm - anti-cheat minimum
    
    # Kick tracking
    MIN_KICKS_EXPECTED = 2  # Should see at least 2 kicks during the check window
    # =========================

    # ── default result and text ───────────────────────────────────────────────
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for messages..."

    def apply_verdict(result, td, ended_early=False):
        distance_moved = td["data"]["max_distance_moved"]
        kick_count = td["data"]["kick_count"]
        robot_moved = distance_moved >= MIN_MOVEMENT_DISTANCE
        has_kicks = kick_count >= MIN_KICKS_EXPECTED
        early_reason = td["data"].get("early_finish_reason")

        if robot_moved and has_kicks:
            result["success"] = True
            result["score"] = 100
            result["description"] = f"Perfect! P-controller with kicks working. Distance: {distance_moved:.1f}cm, Kicks: {kick_count} | Score: 100"
            return f"Mission complete! Distance: {distance_moved:.1f}cm, Kicks: {kick_count}"

        if robot_moved and kick_count >= 1:
            result["success"] = False
            result["score"] = 80
            if ended_early and early_reason:
                result["description"] = f"Good! Robot moved {distance_moved:.1f}cm with {kick_count} kick(s), expected {MIN_KICKS_EXPECTED}+ before early stop ({early_reason}) | Score: 80"
                return f"Good work, but attempt ended early after {kick_count} kick(s): {early_reason}"
            result["description"] = f"Good! Robot moved {distance_moved:.1f}cm with {kick_count} kick(s), expected {MIN_KICKS_EXPECTED}+ | Score: 80"
            return f"Good work, but expected more kicks over {TASK_DURATION}s."

        if robot_moved:
            result["success"] = False
            result["score"] = 60
            if ended_early and early_reason:
                result["description"] = f"Robot moved {distance_moved:.1f}cm but no KICK messages detected before early stop ({early_reason}). Check timer logic. | Score: 60"
                return f"P-controller works but attempt ended early before a kick: {early_reason}"
            result["description"] = f"Robot moved {distance_moved:.1f}cm but no KICK messages detected. Check timer logic. | Score: 60"
            return "P-controller works but kick timer not triggering."

        if kick_count > 0:
            result["success"] = False
            result["score"] = 40
            if ended_early and early_reason:
                result["description"] = f"{kick_count} kicks detected but robot barely moved ({distance_moved:.1f}cm) before early stop ({early_reason}) | Score: 40"
                return f"Kick timer works but robot not moving properly before early stop: {early_reason}"
            result["description"] = f"{kick_count} kicks detected but robot barely moved ({distance_moved:.1f}cm) | Score: 40"
            return "Kick timer works but robot not moving properly."

        result["success"] = False
        result["score"] = 0
        if ended_early and early_reason:
            result["description"] = f"Task incomplete. Kicks: {kick_count}, Distance: {distance_moved:.1f}cm. Attempt ended early: {early_reason} | Score: 0"
            return f"Task incomplete. Attempt ended early: {early_reason}"
        result["description"] = f"Task incomplete. Kicks: {kick_count}, Distance: {distance_moved:.1f}cm | Score: 0"
        return "Task incomplete. Check code execution."

    image = robot.draw_info(image)

    # ── first-frame initialisation ────────────────────────────────────────────
    if td is None:
        # ── code validation ───────────────────────────────────────────────────
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_while_true      = 'while True' in active_code
        has_analog_read     = 'analog_read_all()' in active_code
        has_track_line      = 'track_line()' in active_code
        has_max_check       = 'max(' in active_code and '< 700' in active_code
        has_robot_stop      = 'robot.stop()' in active_code
        has_break           = 'break' in active_code
        
        # P-controller checks (from 5.3)
        has_base_speed = 'base_speed' in active_code
        has_kp         = 'kp' in active_code or 'Kp' in active_code or 'KP' in active_code
        has_p_calc     = '* position' in active_code  # P = kp * position
        has_left_speed = 'left_speed' in active_code
        has_right_speed = 'right_speed' in active_code
        has_add_subtract = ('+' in active_code and '-' in active_code)
        
        # NEW: Kick timer checks
        has_last_kick_time = 'last_kick_time' in active_code
        has_elapsed_time   = 'elapsed_time' in active_code or 'elapsed' in active_code
        has_time_check     = '> 5' in active_code or '>5' in active_code  # Check if elapsed > 5
        has_kick_print     = 'KICK' in active_code
        has_time_reset     = 'last_kick_time = time.time()' in active_code or 'last_kick_time=time.time()' in active_code
        
        code_valid = (
            has_while_true and has_analog_read and has_track_line
            and has_robot_stop and has_break
            and has_base_speed and has_kp and has_p_calc
            and has_left_speed and has_right_speed and has_add_subtract
            and has_last_kick_time and has_elapsed_time and has_time_check
            and has_kick_print and has_time_reset
        )

        missing = []
        if not has_while_true:      missing.append('while True loop')
        if not has_analog_read:     missing.append('analog_read_all()')
        if not has_track_line:      missing.append('track_line()')
        if not has_robot_stop:      missing.append('robot.stop()')
        if not has_break:           missing.append('break statement')
        if not has_base_speed:      missing.append('base_speed variable')
        if not has_kp:              missing.append('kp variable')
        if not has_p_calc:          missing.append('P = kp * position')
        if not has_left_speed:      missing.append('left_speed calculation')
        if not has_right_speed:     missing.append('right_speed calculation')
        if not has_add_subtract:    missing.append('+ and - operations for steering')
        if not has_last_kick_time:  missing.append('last_kick_time variable')
        if not has_elapsed_time:    missing.append('elapsed_time calculation')
        if not has_time_check:      missing.append('time check (> 5 seconds)')
        if not has_kick_print:      missing.append('KICK print statement')
        if not has_time_reset:      missing.append('timer reset (last_kick_time = time.time())')

        # ── td state init ─────────────────────────────────────────────────────
        td = {
            "start_time": time.time(),
            "end_time":   time.time() + 30,
            "data": {
                "code_valid":               code_valid,
                "missing":                  missing,
                "completed_verdict":        False,
                
                # Position tracking
                "start_position":           None,
                "max_distance_moved":       0.0,
                
                # MQTT message tracking
                "last_message":             None,
                "kick_count":               0,
                "kick_messages":            [],
                "early_finish_reason":      None,
            }
        }

    # ── code invalid notice ───────────────────────────────────────────────────
    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

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
        td["data"]["last_message"] = msg
        
        # Detect KICK messages
        if "KICK" in msg:
            td["data"]["kick_count"] += 1
            td["data"]["kick_messages"].append(msg)
        if "Problem" in msg:
            td["data"]["early_finish_reason"] = "Problem"

    # ── live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        if td["data"]["last_message"] is not None:
            text = f"Last message: {td['data']['last_message']}"
        
        distance = td["data"]["max_distance_moved"]
        kick_count = td["data"]["kick_count"]
        
        if distance > 0:
            text = f"Last message: {td['data']['last_message']} | Distance: {distance:.1f}cm, Kicks: {kick_count}"

    ended_early = td["data"].get("early_finish_reason") is not None

    # ── timeout / final verdict (fires exactly once) ──────────────────────────
    if (td["end_time"] - time.time() < 1 or ended_early) and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        
        else:
            text = apply_verdict(result, td, ended_early=ended_early)

    return image, td, text, result


# ============================================================================
# Task 5.5: Adaptive Speed
# ============================================================================
def adaptive_speed(robot, image, td, user_code=None):
    """
    Verification for lesson: Adaptive Speed — 5.5
    Start: x=40, y=30
    Checkpoints: (105, 60), (60, 90), (80, 30) - visual feedback only
    """

    # ===== CONFIGURATION =====
    TASK_DURATION = 60
    
    # Movement tracking
    MIN_MOVEMENT_DISTANCE = 10.0  # cm - anti-cheat minimum
    
    # Checkpoints (visual only, not required for scoring)
    CHECKPOINT_RADIUS = 10.0  # cm
    CHECKPOINTS = [(105, 60), (60, 90), (80, 30)]  # Full lap challenge
    # =========================

    # ── default result and text ───────────────────────────────────────────────
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for messages..."

    image = robot.draw_info(image)

    # ── first-frame initialisation ────────────────────────────────────────────
    if td is None:
        # ── code validation ───────────────────────────────────────────────────
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_while_true      = 'while True' in active_code
        has_analog_read     = 'analog_read_all()' in active_code
        has_track_line      = 'track_line()' in active_code
        has_max_check       = 'max(' in active_code and '< 700' in active_code
        has_robot_stop      = 'robot.stop()' in active_code
        has_break           = 'break' in active_code
        
        # P-controller checks
        has_kp         = 'kp' in active_code or 'Kp' in active_code or 'KP' in active_code
        has_p_calc     = '* position' in active_code  # P = kp * position
        has_left_speed = 'left_speed' in active_code
        has_right_speed = 'right_speed' in active_code
        has_add_subtract = ('+' in active_code and '-' in active_code)
        
        # NEW: Adaptive speed checks
        has_max_speed      = 'max_speed' in active_code
        has_braking_force  = 'braking_force' in active_code
        has_dynamic_speed  = 'dynamic_speed' in active_code
        has_abs_function   = 'abs(position)' in active_code or 'abs( position)' in active_code
        has_int_wrapper    = 'int(' in active_code  # Check for int() usage
        
        # Should NOT have base_speed (replaced by adaptive speed)
        has_base_speed = 'base_speed' in active_code
        
        code_valid = (
            has_while_true and has_analog_read and has_track_line
            and has_max_check and has_robot_stop and has_break
            and has_kp and has_p_calc
            and has_left_speed and has_right_speed and has_add_subtract
            and has_max_speed and has_braking_force and has_dynamic_speed
            and has_abs_function and has_int_wrapper
            and not has_base_speed  # Should NOT have base_speed
        )

        missing = []
        if not has_while_true:      missing.append('while True loop')
        if not has_analog_read:     missing.append('analog_read_all()')
        if not has_track_line:      missing.append('track_line()')
        if not has_max_check:       missing.append('max(sensor_array) < 700 failsafe')
        if not has_robot_stop:      missing.append('robot.stop()')
        if not has_break:           missing.append('break statement')
        if not has_kp:              missing.append('kp variable')
        if not has_p_calc:          missing.append('P = kp * position')
        if not has_left_speed:      missing.append('left_speed calculation')
        if not has_right_speed:     missing.append('right_speed calculation')
        if not has_add_subtract:    missing.append('+ and - operations for steering')
        if not has_max_speed:       missing.append('max_speed variable')
        if not has_braking_force:   missing.append('braking_force variable')
        if not has_dynamic_speed:   missing.append('dynamic_speed calculation')
        if not has_abs_function:    missing.append('abs(position) function')
        if not has_int_wrapper:     missing.append('int() wrapper for speeds')
        if has_base_speed:          missing.append('remove base_speed (use dynamic_speed)')

        # ── td state init ─────────────────────────────────────────────────────
        td = {
            "start_time": time.time(),
            "end_time":   time.time() + 60,
            "data": {
                "code_valid":               code_valid,
                "missing":                  missing,
                "completed_verdict":        False,
                
                # Position tracking
                "start_position":           None,
                "max_distance_moved":       0.0,
                
                # MQTT message tracking
                "last_message":             None,
                
                # Checkpoint tracking (visual only)
                "checkpoints_hit":          [],
                "checkpoints_remaining":    list(CHECKPOINTS),
                
                # Flag image assets
                "flag":                     None,
                "flag_mask":                None,
                "flag_green":               None,
                "flag_green_mask":          None,
                "image_error":              False,
            }
        }

        # ── flag image loading (dual-path fallback) ───────────────────────────
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "flag_finish.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "flag_finish.jpg")
            flag = cv2.imread(filepath)
            if flag is None:
                raise FileNotFoundError(f"flag_finish.jpg not found at {filepath}")
            flag = cv2.resize(flag, (int(flag.shape[1] / 3), int(flag.shape[0] / 3)))
            mask = cv2.bitwise_not(cv2.inRange(flag,
                                               np.array([0, 240, 0]),
                                               np.array([50, 255, 50])))
            td["data"]["flag"]      = flag
            td["data"]["flag_mask"] = mask
            flag_green = flag.copy()
            flag_green[mask > 0] = (0, 200, 0)
            td["data"]["flag_green"]      = flag_green
            td["data"]["flag_green_mask"] = mask
        except Exception as e:
            print(f"Flag load error: {e} — falling back to circle markers")
            td["data"]["image_error"] = True

    # ── code invalid notice ───────────────────────────────────────────────────
    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

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

    # ── checkpoint detection (visual feedback only) ───────────────────────────
    if pos is not None and td["data"]["checkpoints_remaining"]:
        next_cp = td["data"]["checkpoints_remaining"][0]
        dist = math.sqrt((pos[0] - next_cp[0])**2 + (pos[1] - next_cp[1])**2)
        if dist < CHECKPOINT_RADIUS:
            td["data"]["checkpoints_hit"].append(next_cp)
            td["data"]["checkpoints_remaining"].pop(0)

    # ── MQTT message parsing ──────────────────────────────────────────────────
    msg = robot.get_msg()
    if msg is not None:
        td["data"]["last_message"] = msg

    # ── live status text ──────────────────────────────────────────────────────
    if not td["data"].get("completed_verdict"):
        if td["data"]["last_message"] is not None:
            text = f"Last message: {td['data']['last_message']}"
        
        distance = td["data"]["max_distance_moved"]
        checkpoints_hit = len(td["data"]["checkpoints_hit"])
        total_checkpoints = len(CHECKPOINTS)
        
        if distance > 0:
            text = f"Last message: {td['data']['last_message']} | Distance: {distance:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}"

    # ── overlay drawing (checkpoints with flags) ──────────────────────────────
    pos_px = robot.position_px
    if pos is not None and pos_px is not None and pos[0] != 0:
        px_per_cm  = pos_px[0] / pos[0]
        radius_px  = int(CHECKPOINT_RADIUS * px_per_cm)
        flag       = td["data"]["flag"]
        flag_mask  = td["data"]["flag_mask"]
        flag_green = td["data"]["flag_green"]
        use_flag   = not td["data"]["image_error"] and flag is not None
        hits       = td["data"]["checkpoints_hit"]

        for cp_cm in CHECKPOINTS:
            cp_px = (int(cp_cm[0] * px_per_cm), int(cp_cm[1] * px_per_cm))
            hit   = cp_cm in hits
            cv2.circle(image, cp_px, radius_px, (0, 200, 0) if hit else (0, 200, 255), 1)
            
            if use_flag:
                draw_flag = flag_green if hit else flag
                half_w = draw_flag.shape[1] // 2
                half_h = draw_flag.shape[0] // 2
                r0 = cp_px[1] - half_h
                r1 = cp_px[1] + (draw_flag.shape[0] - half_h)
                c0 = cp_px[0] - half_w
                c1 = cp_px[0] + (draw_flag.shape[1] - half_w)
                if 0 <= r0 and r1 < image.shape[0] and 0 <= c0 and c1 < image.shape[1]:
                    cv2.copyTo(draw_flag, flag_mask, image[r0:r1, c0:c1])
            else:
                cv2.circle(image, cp_px, 5, (0, 200, 0) if hit else (0, 200, 255), -1)

    # ── timeout / final verdict (fires exactly once) ──────────────────────────
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        
        else:
            # Evaluate mission performance
            distance_moved = td["data"]["max_distance_moved"]
            robot_moved = distance_moved >= MIN_MOVEMENT_DISTANCE
            checkpoints_hit = len(td["data"]["checkpoints_hit"])
            total_checkpoints = len(CHECKPOINTS)
            
            # Success criteria
            if robot_moved:
                result["success"]     = True
                result["score"]       = 100
                result["description"] = f"Perfect! Adaptive speed controller working. Distance: {distance_moved:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints} | Score: 100"
                text = f"Mission complete! Distance: {distance_moved:.1f}cm, Checkpoints: {checkpoints_hit}/{total_checkpoints}"
            
            else:
                # Robot didn't move
                result["success"]     = False
                result["score"]       = 0
                result["description"] = f"Task incomplete. Robot barely moved ({distance_moved:.1f}cm) | Score: 0"
                text = "Task incomplete. Check code execution."

    return image, td, text, result
