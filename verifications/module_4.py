import cv2
import math
import time
import os
import re
import numpy as np

target_points = {
    'python_lists':        [(75, 30), (30, 0)],
    'telemetry':           [(75, 30), (30, 0)],
    'color_sensor_basics': [(128, 98), (0, -30)],
    'color_classification':[(128, 99), (0, -30)],
    'multiple_sensors':    [(45, 29), (30, 0)],
    'data_logging':        [(45, 29), (30, 0)],
}

block_library_functions = {
    'python_lists':         False,
    'telemetry':            False,
    'color_sensor_basics':  False,
    'color_classification': False,
    'multiple_sensors':     False,
    'data_logging':         False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])





# ──────────────────────────────────────────────────────────────────────────────
# 4.1 Python Lists
# ──────────────────────────────────────────────────────────────────────────────

def python_lists(robot, image, td, user_code=None):
    """
    Verification for lesson: Python Lists (Waypoints) — 4.1
    Start: x=75, y=30, direction x=30, y=0
    Checkpoints: (130,30), (130,90), (60,90)
    """

    TASK_DURATION     = 30
    CHECKPOINT_RADIUS = 10.0
    CHECKPOINTS       = [(130, 30), (130, 90), (60, 90)]

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }

    hit_so_far = 0 if td is None else len(td["data"]["checkpoints_hit"])
    text = f"Checkpoints reached: {hit_so_far}/{len(CHECKPOINTS)}"

    image = robot.draw_info(image)

    if td is None:
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_in_route        = "in route" in active_code
        has_move_forward    = "move_forward_distance" in active_code
        has_turn_right      = "turn_right" in active_code
        has_len_route       = "len(route)" in active_code
        has_waypoints_print = "waypoints" in active_code
        code_valid = (
            has_in_route and has_move_forward and has_turn_right
            and has_len_route and has_waypoints_print
        )

        missing = []
        if not has_in_route:        missing.append("for loop with 'in route'")
        if not has_move_forward:    missing.append("move_forward_distance()")
        if not has_turn_right:      missing.append("turn_right()")
        if not has_len_route:       missing.append("len(route)")
        if not has_waypoints_print: missing.append("waypoint count print")

        td = {
            "start_time": time.time(),
            "end_time":   time.time() + TASK_DURATION,
            "data": {
                "code_valid":            code_valid,
                "missing":               missing,
                "completed_verdict":     False,
                "checkpoints_hit":       [],
                "checkpoints_remaining": list(CHECKPOINTS),
                "flag":                  None,
                "flag_mask":             None,
                "flag_green":            None,
                "flag_green_mask":       None,
                "image_error":           False,
            }
        }

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

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

    pos = robot.position
    if pos is not None and td["data"]["checkpoints_remaining"]:
        next_cp = td["data"]["checkpoints_remaining"][0]
        dist = math.sqrt((pos[0] - next_cp[0])**2 + (pos[1] - next_cp[1])**2)
        if dist < CHECKPOINT_RADIUS:
            td["data"]["checkpoints_hit"].append(next_cp)
            td["data"]["checkpoints_remaining"].pop(0)

    hit_now = len(td["data"]["checkpoints_hit"])
    text = f"Checkpoints reached: {hit_now}/{len(CHECKPOINTS)}"

    msg = robot.get_msg()
    if msg is not None:
        text = f"Message: {msg}"

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

    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        hit   = len(td["data"]["checkpoints_hit"])
        total = len(CHECKPOINTS)
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif hit < total:
            result["success"]     = False
            result["score"]       = int((hit / total) * 100)
            result["description"] = f"Only {hit}/{total} checkpoints reached | Score: {result['score']}"
            text = f"Only {hit}/{total} checkpoints reached."
        else:
            result["success"]     = True
            result["score"]       = 100
            result["description"] = f"You are amazing! All {total} checkpoints reached | Score: 100"
            text = "Route complete!"

    return image, td, text, result


# ──────────────────────────────────────────────────────────────────────────────
# 4.2 Telemetry
# ──────────────────────────────────────────────────────────────────────────────

def telemetry(robot, image, td, user_code=None):
    """
    Verification for lesson: Telemetry — 4.2
    Start: x=75, y=30, direction x=30, y=0
    """

    TASK_DURATION  = 20
    START_POS_CM   = (75, 30)
    MIN_MOVE_CM    = 35.0
    REQUIRED_KEYS  = {"name", "dist", "time", "speed", "ready"}

    result = {
        "success": True,
        "description": "Telemetry report received and validated",
        "score": 100
    }
    text = "Speed test underway..."

    image = robot.draw_info(image)

    if td is None:
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_move_forward  = "move_forward_distance(" in active_code
        has_time_time     = active_code.count("time.time()") >= 2
        has_robot_name    = "robot_name" in active_code
        has_is_ready      = "is_ready" in active_code
        has_fstring_print = "print(f" in active_code
        code_valid = (
            has_move_forward and has_time_time and has_robot_name
            and has_is_ready and has_fstring_print
        )

        missing = []
        if not has_move_forward:  missing.append("move_forward_distance(")
        if not has_time_time:     missing.append("time.time() used twice (start + end)")
        if not has_robot_name:    missing.append("robot_name variable")
        if not has_is_ready:      missing.append("is_ready variable")
        if not has_fstring_print: missing.append("f-string inside print()")

        td = {
            "start_time": time.time(),
            "end_time":   time.time() + TASK_DURATION,
            "data": {
                "code_valid":        code_valid,
                "missing":           missing,
                "completed_verdict": False,
                "phase":             1,
                "moved":             False,
                "max_dist":          0.0,
                "msg_valid":         False,
                "msg_keys_found":    [],
                "msg_raw":           None,
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"
        return image, td, text, result

    if not td["data"]["msg_valid"]:
        msg = robot.get_msg()
        if msg is not None and msg.startswith("STATUS:"):
            td["data"]["msg_raw"] = msg
            body         = msg[len("STATUS:"):]
            pairs        = dict(re.findall(r'(\w+)=([^;]+)', body))
            keys_found   = set(pairs.keys())
            missing_keys = REQUIRED_KEYS - keys_found
            td["data"]["msg_keys_found"] = list(keys_found)
            if not missing_keys:
                td["data"]["msg_valid"] = True
                text = "Telemetry validated!"
            else:
                text = f"STATUS message missing keys: {', '.join(missing_keys)}"
        elif msg is not None:
            text = f"Message received but wrong format: {msg[:40]}"

    if td["data"]["phase"] == 1:
        pos = robot.position
        if pos is not None:
            dist = math.sqrt((pos[0] - START_POS_CM[0])**2 + (pos[1] - START_POS_CM[1])**2)
            if not td["data"]["msg_valid"]:
                text = f"Waiting for movement... {dist:.1f}/{MIN_MOVE_CM}cm"
            if dist > td["data"]["max_dist"]:
                td["data"]["max_dist"] = dist
            if dist >= MIN_MOVE_CM:
                td["data"]["moved"] = True
                td["data"]["phase"] = 2
        else:
            if not td["data"]["msg_valid"]:
                text = "Waiting for robot marker..."

    if td["data"]["phase"] == 2 and not td["data"]["msg_valid"]:
        text = "Movement confirmed! Waiting for telemetry..."

    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        if not td["data"]["moved"] and not td["data"]["msg_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = (
                f"Robot moved only {td['data']['max_dist']:.1f}cm, "
                f"required ≥{MIN_MOVE_CM}cm | Score: 0"
            )
            text = f"Robot moved only {td['data']['max_dist']:.1f}cm."
        elif not td["data"]["msg_valid"]:
            result["success"]     = False
            result["score"]       = 50
            result["description"] = "Robot moved but no valid STATUS message received | Score: 50"
            text = "No valid telemetry message received."
        else:
            result["success"]     = True
            result["score"]       = 100
            result["description"] = "Telemetry report received with all required fields | Score: 100"
            text = "Telemetry complete!"

    return image, td, text, result


# ──────────────────────────────────────────────────────────────────────────────
# 4.3 Color Sensor Basics
# ──────────────────────────────────────────────────────────────────────────────

def color_sensor_basics(robot, image, td, user_code=None):
    """
    Verification for lesson: Color Sensor Basics — 4.3
    Start: x=128, y=98, direction x=0, y=-30
    """

    TASK_DURATION   = 20
    MIN_VALID_SCANS = 5

    result = {
        "success": True,
        "description": "Color scan complete! All zones reported.",
        "score": 100
    }
    text = "Waiting for scan data..."

    image = robot.draw_info(image)

    if td is None:
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_i2c        = "machine.I2C" in active_code
        has_tcs3472    = "tcs3472" in active_code
        has_range6     = "range(6)" in active_code
        has_rgb        = ".rgb()" in active_code
        has_move       = "move_forward_distance(10)" in active_code
        has_scan_print = "Scan - R:" in active_code
        code_valid = (
            has_i2c and has_tcs3472 and has_range6
            and has_rgb and has_move and has_scan_print
        )

        missing = []
        if not has_i2c:        missing.append("machine.I2C initialization")
        if not has_tcs3472:    missing.append("tcs3472 sensor")
        if not has_range6:     missing.append("range(6) loop")
        if not has_rgb:        missing.append(".rgb() call")
        if not has_move:       missing.append("move_forward_distance(10)")
        if not has_scan_print: missing.append('print format "Scan - R:..."')

        td = {
            "start_time": time.time(),
            "end_time":   time.time() + TASK_DURATION,
            "data": {
                "code_valid":        code_valid,
                "missing":           missing,
                "completed_verdict": False,
                "valid_scans":       [],
                "last_scan":         None,
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"
        return image, td, text, result

    msg = robot.get_msg()
    if msg is not None:
        match = re.search(r'Scan - R:(\d+) G:(\d+) B:(\d+)', msg)
        if match:
            r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                td["data"]["valid_scans"].append((r, g, b))
                td["data"]["last_scan"] = (r, g, b)

    valid = len(td["data"]["valid_scans"])
    last  = td["data"].get("last_scan")
    if last:
        text = f"Valid scans: {valid}/{MIN_VALID_SCANS} | Last: R:{last[0]} G:{last[1]} B:{last[2]}"
    else:
        text = f"Valid scans received: {valid}/{MIN_VALID_SCANS}"

    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        valid = len(td["data"]["valid_scans"])
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif valid < MIN_VALID_SCANS:
            result["success"]     = False
            result["score"]       = int((valid / MIN_VALID_SCANS) * 100)
            result["description"] = f"Only {valid}/{MIN_VALID_SCANS} valid scans received | Score: {result['score']}"
            text = f"Only {valid}/{MIN_VALID_SCANS} valid scans received."
        else:
            result["success"]     = True
            result["score"]       = 100
            result["description"] = f"Color scan complete! {valid} valid zones reported | Score: 100"
            text = "Scan complete!"

    return image, td, text, result


# ──────────────────────────────────────────────────────────────────────────────
# 4.4 Color Classification
# ──────────────────────────────────────────────────────────────────────────────

def color_classification(robot, image, td, user_code=None):
    """
    Verification for lesson: Color Classification — 4.4
    Start: x=128, y=99, direction x=0, y=-30
    """

    TASK_DURATION   = 20
    MIN_VALID_SCANS = 5
    VALID_COLORS    = {"Red", "Green", "Blue", "Floor", "Unknown"}

    result = {
        "success": True,
        "description": "Smart scan complete! All zones classified.",
        "score": 100
    }
    text = "Waiting for scan data..."

    image = robot.draw_info(image)

    if td is None:
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_i2c           = "machine.I2C" in active_code
        has_tcs3472       = "tcs3472" in active_code
        has_detect_func   = "def detect_color_name" in active_code
        has_normalization = ("r_ratio" in active_code
                             and "g_ratio" in active_code
                             and "b_ratio" in active_code)
        has_range6        = "range(6)" in active_code
        has_rgb           = ".rgb()" in active_code
        has_move          = "move_forward_distance(10)" in active_code
        has_detect_call   = "detect_color_name(r, g, b)" in active_code
        has_scan_print    = "Scan complete:" in active_code
        code_valid = (
            has_i2c and has_tcs3472 and has_detect_func and has_normalization
            and has_range6 and has_rgb and has_move
            and has_detect_call and has_scan_print
        )

        missing = []
        if not has_i2c:           missing.append("machine.I2C initialization")
        if not has_tcs3472:       missing.append("tcs3472 sensor")
        if not has_detect_func:   missing.append("detect_color_name() function")
        if not has_normalization: missing.append("r_ratio / g_ratio / b_ratio normalization")
        if not has_range6:        missing.append("range(6) loop")
        if not has_rgb:           missing.append(".rgb() call")
        if not has_move:          missing.append("move_forward_distance(10)")
        if not has_detect_call:   missing.append("detect_color_name(r, g, b) call in loop")
        if not has_scan_print:    missing.append('print format "Scan complete:..."')

        td = {
            "start_time": time.time(),
            "end_time":   time.time() + TASK_DURATION,
            "data": {
                "code_valid":        code_valid,
                "missing":           missing,
                "completed_verdict": False,
                "valid_scans":       [],
                "last_scan":         None,
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"
        return image, td, text, result

    msg = robot.get_msg()
    if msg is not None:
        match = re.search(r'Scan complete: (\w+) \(Raw: R:(\d+) G:(\d+) B:(\d+)\)', msg)
        if match:
            color_name = match.group(1)
            r, g, b    = int(match.group(2)), int(match.group(3)), int(match.group(4))
            if (color_name in VALID_COLORS
                    and 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                td["data"]["valid_scans"].append((color_name, r, g, b))
                td["data"]["last_scan"] = (color_name, r, g, b)

    valid = len(td["data"]["valid_scans"])
    last  = td["data"].get("last_scan")
    if last:
        text = f"Valid scans: {valid}/{MIN_VALID_SCANS} | Last: {last[0]} R:{last[1]} G:{last[2]} B:{last[3]}"
    else:
        text = f"Valid scans received: {valid}/{MIN_VALID_SCANS}"

    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        valid = len(td["data"]["valid_scans"])
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif valid < MIN_VALID_SCANS:
            result["success"]     = False
            result["score"]       = int((valid / MIN_VALID_SCANS) * 100)
            result["description"] = f"Only {valid}/{MIN_VALID_SCANS} valid scans received | Score: {result['score']}"
            text = f"Only {valid}/{MIN_VALID_SCANS} valid scans received."
        else:
            result["success"]     = True
            result["score"]       = 100
            result["description"] = f"Smart scan complete! {valid} zones classified | Score: 100"
            text = "Smart scan complete!"

    return image, td, text, result


# ──────────────────────────────────────────────────────────────────────────────
# 4.5 Multiple Sensors
# ──────────────────────────────────────────────────────────────────────────────

def multiple_sensors(robot, image, td, user_code=None):
    """
    Verification for lesson: Multiple Sensors — 4.5
    Start: x=45, y=29, direction x=30, y=0
    LED confirmed via MQTT "Green: led on" — camera crop abandoned (LED too small).
    Stop confirmed via MQTT + robot stationary near blue zone for 1s.
    """

    TASK_DURATION      = 30
    GREEN_ZONE_CENTER  = (75, 32)
    GREEN_ZONE_SIZE    = 10
    BLUE_ZONE_CENTER   = (100, 55)
    BLUE_ZONE_RADIUS   = 15
    STOP_DRIFT_CM      = 3.0
    STOP_CHECK_DELAY   = 1.0
    VALID_COLORS       = {"Red", "Green", "Blue", "Floor", "Unknown"}
    LED_ON_MSG         = "Green: led on"
    STOP_MSG           = "Blue: Mission complete."

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Following track..."

    image = robot.draw_info(image)

    if td is None:
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_i2c           = "machine.I2C" in active_code
        has_tcs3472       = "tcs3472" in active_code
        has_octoliner     = "Octoliner" in active_code
        has_pin15         = "Pin(15" in active_code
        has_detect_func   = "def detect_color_name" in active_code
        has_normalization = ("r_ratio" in active_code
                             and "g_ratio" in active_code
                             and "b_ratio" in active_code)
        has_while         = "while True" in active_code
        has_last_color    = "last_color" in active_code
        has_break         = "break" in active_code
        has_read_all      = "analog_read_all()" in active_code
        has_elif          = "elif" in active_code

        code_valid = (
            has_i2c and has_tcs3472 and has_octoliner and has_pin15
            and has_detect_func and has_normalization and has_while
            and has_last_color and has_break and has_read_all and has_elif
        )

        missing = []
        if not has_i2c:           missing.append("machine.I2C")
        if not has_tcs3472:       missing.append("tcs3472 sensor")
        if not has_octoliner:     missing.append("Octoliner")
        if not has_pin15:         missing.append("Pin(15) LED")
        if not has_detect_func:   missing.append("detect_color_name() function")
        if not has_normalization: missing.append("r_ratio / g_ratio / b_ratio normalization")
        if not has_while:         missing.append("while True loop")
        if not has_last_color:    missing.append("last_color spam filter")
        if not has_break:         missing.append("break statement")
        if not has_read_all:      missing.append("analog_read_all()")
        if not has_elif:          missing.append("elif statement")

        td = {
            "start_time": time.time(),
            "end_time":   time.time() + TASK_DURATION,
            "data": {
                "code_valid":        code_valid,
                "missing":           missing,
                "completed_verdict": False,
                "color_msgs":        [],
                "led_on_received":   False,
                "stop_received":     False,
                "last_msg":          None,
                "mqtt_led_state":    False,
                "stop_msg_time":     None,
                "stop_msg_pos":      None,
                "stopped_confirmed": False,
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["last_msg"] = msg

        match = re.search(r'(\w+) \(Raw: R:(\d+) G:(\d+) B:(\d+)\)', msg)
        if match and match.group(1) in VALID_COLORS:
            td["data"]["color_msgs"].append(msg)

        if LED_ON_MSG in msg:
            td["data"]["led_on_received"] = True
            td["data"]["mqtt_led_state"]  = True

        if "Floor" in msg and td["data"]["mqtt_led_state"]:
            td["data"]["mqtt_led_state"] = False

        if STOP_MSG in msg and not td["data"]["stop_received"]:
            td["data"]["stop_received"] = True
            td["data"]["stop_msg_time"] = time.time()
            pos = robot.position
            td["data"]["stop_msg_pos"]  = pos if pos is not None else None

    if (td["data"]["stop_received"]
            and not td["data"]["stopped_confirmed"]
            and td["data"]["stop_msg_time"] is not None):
        if time.time() - td["data"]["stop_msg_time"] >= STOP_CHECK_DELAY:
            pos      = robot.position
            stop_pos = td["data"]["stop_msg_pos"]
            if pos is not None and stop_pos is not None:
                drift        = math.sqrt((pos[0] - stop_pos[0])**2
                                         + (pos[1] - stop_pos[1])**2)
                dist_to_blue = math.sqrt((pos[0] - BLUE_ZONE_CENTER[0])**2
                                         + (pos[1] - BLUE_ZONE_CENTER[1])**2)
                if drift <= STOP_DRIFT_CM and dist_to_blue <= BLUE_ZONE_RADIUS:
                    td["data"]["stopped_confirmed"] = True

    pos    = robot.position
    pos_px = robot.position_px
    if pos is not None and pos_px is not None and pos[0] != 0:
        px_per_cm = pos_px[0] / pos[0]

        gx0 = GREEN_ZONE_CENTER[0] - GREEN_ZONE_SIZE
        gy0 = GREEN_ZONE_CENTER[1] - GREEN_ZONE_SIZE
        gx1 = GREEN_ZONE_CENTER[0] + GREEN_ZONE_SIZE
        gy1 = GREEN_ZONE_CENTER[1] + GREEN_ZONE_SIZE
        zone_color = (0, 200, 0) if td["data"]["led_on_received"] else (0, 200, 255)
        cv2.rectangle(image,
                      (int(gx0 * px_per_cm), int(gy0 * px_per_cm)),
                      (int(gx1 * px_per_cm), int(gy1 * px_per_cm)),
                      zone_color, 2)
        cv2.putText(image, "GREEN ZONE",
                    (int(gx0 * px_per_cm), int(gy0 * px_per_cm) - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, zone_color, 1, cv2.LINE_AA)

        bz_px        = (int(BLUE_ZONE_CENTER[0] * px_per_cm),
                        int(BLUE_ZONE_CENTER[1] * px_per_cm))
        bz_radius_px = int(BLUE_ZONE_RADIUS * px_per_cm)
        blue_color   = (255, 180, 0) if td["data"]["stopped_confirmed"] else (255, 200, 100)
        cv2.circle(image, bz_px, bz_radius_px, blue_color, 2)
        cv2.putText(image, "BLUE ZONE",
                    (bz_px[0] - 30, bz_px[1] - bz_radius_px - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, blue_color, 1, cv2.LINE_AA)

    led_label = "LED ON" if td["data"]["mqtt_led_state"] else "LED OFF"
    led_color = (0, 255, 0) if td["data"]["mqtt_led_state"] else (0, 100, 100)
    cv2.putText(image, led_label,
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, led_color, 1)

    color_count = len(td["data"]["color_msgs"])
    last = td["data"]["last_msg"]
    if last:
        text = f"Classifications: {color_count} | Last: {last[:40]}"

    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        color_count = len(td["data"]["color_msgs"])
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif color_count == 0:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = "No color classification messages received | Score: 0"
            text = "No color data received."
        elif not td["data"]["led_on_received"]:
            result["success"]     = False
            result["score"]       = 50
            result["description"] = (
                f"Color data received ({color_count} msgs) but "
                f"'Green: led on' message not received | Score: 50"
            )
            text = "LED-on message not received."
        elif not td["data"]["stop_received"]:
            result["success"]     = False
            result["score"]       = 50
            result["description"] = (
                f"LED confirmed ON for green zone but "
                f"'Blue: Mission complete.' not received | Score: 50"
            )
            text = "Blue stop message not received."
        elif not td["data"]["stopped_confirmed"]:
            result["success"]     = False
            result["score"]       = 75
            result["description"] = (
                f"Blue stop message received but robot did not confirm stationary "
                f"near blue zone (radius {BLUE_ZONE_RADIUS}cm from {BLUE_ZONE_CENTER}) "
                f"| Score: 75"
            )
            text = "Robot did not stop near blue zone."
        else:
            result["success"]     = True
            result["score"]       = 100
            result["description"] = (
                f"Mission complete! LED on green, stopped on blue "
                f"({color_count} classifications) | Score: 100"
            )
            text = "Mission complete!"

    return image, td, text, result


# ──────────────────────────────────────────────────────────────────────────────
# 4.6 Data Logging
# ──────────────────────────────────────────────────────────────────────────────

def data_logging(robot, image, td, user_code=None):
    """
    Verification for lesson: Data Logging — 4.6
    Start: x=45, y=29, direction x=30, y=0 (any position on track accepted)
    All checks MQTT-based. Student code silent during 30s mission;
    "Found: ..." lines arrive in burst after break, before "End of transmission".
    Verification window 60s covers mission + report burst.
    """

    TASK_DURATION  = 60
    VALID_COLORS   = {"Red", "Green", "Blue", "Floor", "Unknown"}
    START_MSG      = "Mission Start!"
    REPORT_END_MSG = "End of transmission"

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for mission start..."

    image = robot.draw_info(image)

    if td is None:
        lines        = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code  = '\n'.join(active_lines)

        has_i2c           = "machine.I2C" in active_code
        has_tcs3472       = "tcs3472" in active_code
        has_octoliner     = "Octoliner" in active_code
        has_detect_func   = "def detect_color_name" in active_code
        has_normalization = ("r_ratio" in active_code
                             and "g_ratio" in active_code
                             and "b_ratio" in active_code)
        has_empty_list    = "= []" in active_code
        has_mission_dur   = "mission_duration" in active_code
        has_start_time    = "start_time" in active_code
        has_timer         = active_code.count("time.time()") >= 2
        has_while         = "while True" in active_code
        has_elapsed       = "elapsed_time" in active_code
        has_break         = "break" in active_code
        has_append        = ".append(" in active_code
        has_read_all      = "analog_read_all()" in active_code
        has_elif          = "elif" in active_code
        has_for_report    = "for " in active_code
        has_end_msg       = "End of transmission" in active_code

        code_valid = (
            has_i2c and has_tcs3472 and has_octoliner
            and has_detect_func and has_normalization
            and has_empty_list and has_mission_dur and has_start_time and has_timer
            and has_while and has_elapsed and has_break
            and has_append and has_read_all and has_elif
            and has_for_report and has_end_msg
        )

        missing = []
        if not has_i2c:           missing.append("machine.I2C")
        if not has_tcs3472:       missing.append("tcs3472 sensor")
        if not has_octoliner:     missing.append("Octoliner")
        if not has_detect_func:   missing.append("detect_color_name() function")
        if not has_normalization: missing.append("r_ratio / g_ratio / b_ratio normalization")
        if not has_empty_list:    missing.append("empty list (= [])")
        if not has_mission_dur:   missing.append("mission_duration variable")
        if not has_start_time:    missing.append("start_time variable")
        if not has_timer:         missing.append("time.time() timer (used at least twice)")
        if not has_while:         missing.append("while True loop")
        if not has_elapsed:       missing.append("elapsed_time check")
        if not has_break:         missing.append("break statement")
        if not has_append:        missing.append(".append() call")
        if not has_read_all:      missing.append("analog_read_all()")
        if not has_elif:          missing.append("elif statement")
        if not has_for_report:    missing.append("for loop for report")
        if not has_end_msg:       missing.append('"End of transmission" print')

        td = {
            "start_time": time.time(),
            "end_time":   time.time() + TASK_DURATION,
            "data": {
                "code_valid":        code_valid,
                "missing":           missing,
                "completed_verdict": False,
                "start_received":    False,
                "anomaly_msgs":      [],
                "report_end":        False,
                "last_msg":          None,
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["last_msg"] = msg
        if START_MSG in msg:
            td["data"]["start_received"] = True
        match = re.search(r'Found: (\w+) \| Raw Data: R:(\d+) G:(\d+) B:(\d+)', msg)
        if match and match.group(1) in VALID_COLORS:
            td["data"]["anomaly_msgs"].append(msg)
        if REPORT_END_MSG in msg:
            td["data"]["report_end"] = True

    anomaly_count = len(td["data"]["anomaly_msgs"])
    last = td["data"]["last_msg"]
    if last:
        text = f"Anomalies logged: {anomaly_count} | Last: {last[:50]}"
    if td["data"]["report_end"]:
        text = f"Report received! {anomaly_count} anomalies logged."

    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        anomaly_count = len(td["data"]["anomaly_msgs"])
        if not td["data"]["code_valid"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif not td["data"]["start_received"]:
            result["success"]     = False
            result["score"]       = 0
            result["description"] = "'Mission Start!' not received — robot did not run | Score: 0"
            text = "Mission Start not received."
        elif anomaly_count == 0:
            result["success"]     = False
            result["score"]       = 50
            result["description"] = (
                "Robot ran but no anomaly log entries received — "
                "check .append() and print format | Score: 50"
            )
            text = "No anomaly data received."
        elif not td["data"]["report_end"]:
            result["success"]     = False
            result["score"]       = 75
            result["description"] = (
                f"Anomalies logged ({anomaly_count}) but 'End of transmission' "
                f"not received — report may not have printed | Score: 75"
            )
            text = "Report end message not received."
        else:
            result["success"]     = True
            result["score"]       = 100
            result["description"] = (
                f"Mission complete! {anomaly_count} anomalies logged and "
                f"report transmitted | Score: 100"
            )
            text = "Mission complete!"

    return image, td, text, result

#OLD

'''
# ──────────────────────────────────────────────────────────────────────────────
# Legacy / Module 4 intro
# ──────────────────────────────────────────────────────────────────────────────

def encoders(robot, image, td, user_code=None):
    """Verification function for Lesson 1: Encoder"""
    result = {
        "success": True,
        "description": "Test in progress...",
        "score": 100
    }
    text = "Reading encoder data..."

    image = robot.draw_info(image)

    if not td:
        td = {
            "end_time": time.time() + 5,
            "data": {
                'messages':     [],
                'encoder_pairs':[],
                'current_pair': {},
                'stage':        'start'
            }
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]['messages'].append(msg)
        text = f"Received: {msg}"

        if msg.startswith("LEFT:"):
            td["data"]['current_pair']['left_next'] = True
        elif msg.startswith("RIGHT:"):
            td["data"]['current_pair']['right_next'] = True
        elif td["data"]['current_pair'].get('left_next'):
            try:
                td["data"]['current_pair']['left'] = float(msg)
                td["data"]['current_pair']['left_next'] = False
            except ValueError:
                pass
        elif td["data"]['current_pair'].get('right_next'):
            try:
                td["data"]['current_pair']['right'] = float(msg)
                td["data"]['current_pair']['right_next'] = False
                if 'left' in td["data"]['current_pair']:
                    td["data"]['encoder_pairs'].append(
                        (td["data"]['current_pair']['left'],
                         td["data"]['current_pair']['right'])
                    )
                    td["data"]['current_pair'] = {}
            except ValueError:
                pass

    if td["end_time"] - time.time() < 1:
        if len(td["data"]['encoder_pairs']) < 2:
            pairs_str = ", ".join([f"({l}, {r})" for l, r in td["data"]['encoder_pairs']])
            result["success"]     = False
            result["description"] = f"Not enough encoders data: {pairs_str}"
            result["score"]       = 0
        else:
            start_pair   = td["data"]['encoder_pairs'][0]
            end_pair     = td["data"]['encoder_pairs'][-1]
            left_change  = abs(end_pair[0] - start_pair[0])
            right_change = abs(end_pair[1] - start_pair[1])
            tolerance    = 40
            expected     = 360
            if not (330 <= left_change <= 400 and 330 <= right_change <= 400):
                result["success"]     = False
                result["description"] = (
                    f"Incorrect rotation. Left changed: {left_change:.1f}°, "
                    f"Right changed: {right_change:.1f}°. "
                    f"Expected: {expected}° ±{tolerance}°"
                )
                result["score"] = 0
            else:
                result["success"]     = True
                result["description"] = (
                    f"Success! Left wheel: {left_change:.1f}°, "
                    f"Right wheel: {right_change:.1f}°"
                )
                result["score"] = 100

    return image, td, text, result

'''
