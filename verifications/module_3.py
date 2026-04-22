import cv2
import math
import time
import os
import numpy as np
import re
import ast


target_points = {
    'intro_to_octoliner': [(100,60),(30,0)],
    'conditional_logic' : [(80,60), (30,0)],
    'processing_sensor_data': [(85,63),(30,0)],
    'arrays_and_elif': [(70, 50),(30,0)],
    'led_feedback': [(70,50),(30,0)],
    'simple_line_follower': [(75,30),(30,0)],
    'logical_operators': [(75,30),(30,0)]

    #'differential_drive': [(30, 50), (30, 0)],
    #'move_function':[(50, 50), (30, 0)],
    #'electric_motor': [(50, 50), (30, 0)],


}

block_library_functions = {
    'intro_to_octoliner': True,
    'conditional_logic' : True,
    'processing_sensor_data': True,
    'arrays_and_elif': True,
    'led_feedback': True,
    'simple_line_follower': True,
    'logical_operators': True



    #'differential_drive': True,
    #"move_function": True,
    #'electric_motor': True,
    #'intro_to_octoliner': True,
    #'processing_sensor_data': True
}

def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])


def delta_points(point_0, point_1):
    return math.sqrt(((point_0[0] - point_1[0]) ** 2) +
                     ((point_0[1] - point_1[1]) ** 2))


##NEW

def intro_to_octoliner(robot, image, td, user_code=None):
    """
    Verification for lesson: Introduction to Octoliner
    Students must read sensor 3 or 4 using analog_read() and print the value.
    """

    # ===== CONFIGURATION =====
    TASK_DURATION = 10      # seconds before timeout
    # =========================

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for sensor readings..."

    image = robot.draw_info(image)

    if td is None:
        # Check for analog_read(3) or analog_read(4) — filter commented lines
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)
        code_valid = "analog_read(3)" in active_code or "analog_read(4)" in active_code

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,
            "data": {
                "code_valid": code_valid,
                "sensor_3": None,
                "sensor_4": None,
            }
        }

    if not td["data"]["code_valid"]:
        text = "Code missing: analog_read(3) or analog_read(4)"

    # draw sensor values on overlay
    if td["data"]["sensor_3"] is not None:
        cv2.putText(image, f"Sensor 3: {td['data']['sensor_3']}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
    if td["data"]["sensor_4"] is not None:
        cv2.putText(image, f"Sensor 4: {td['data']['sensor_4']}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

    # parse MQTT messages — only if code is valid
    msg = robot.get_msg()
    if td["data"]["code_valid"] and msg is not None:
        text = f"Message received: {msg}"
        numbers = [int(n) for n in re.findall(r'\d+', msg)]
        if numbers:
            if td["data"]["sensor_3"] is None:
                td["data"]["sensor_3"] = numbers[0]
            elif td["data"]["sensor_4"] is None:
                td["data"]["sensor_4"] = numbers[0]

    got_sensor_data = (td["data"]["sensor_3"] is not None or
                       td["data"]["sensor_4"] is not None)

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Code missing: analog_read(3) or analog_read(4) | Score: 0"
            text = "Code validation failed."
        elif not got_sensor_data:
            result["success"] = False
            result["score"] = 0
            result["description"] = "Timeout: No sensor readings received | Score: 0"
            text = "No readings received."
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = (
                f"You are amazing! Sensor readings received: "
                f"S3={td['data']['sensor_3']}, S4={td['data']['sensor_4']} | Score: 100"
            )
            text = "Assignment complete!"

    return image, td, text, result




def conditional_logic(robot, image, td, user_code=None):
    """
    Verification for lesson: Conditional Logic / Stop on Line
    Students must:
    - Drive forward using run_motors_speed()
    - Continuously read sensor 3 or 4 in a while loop
    - Use an if statement to stop motors when threshold is exceeded
    - Print "Target found. Rover stopped." after stopping
    """

    # ===== CONFIGURATION =====
    TASK_DURATION      = 20     # seconds before timeout
    STOP_SETTLE_TIME   = 3.0    # seconds to observe robot after stop message
    MOVEMENT_MIN       = 1.0    # cm — robot must have moved at least this before stop
    STOP_MAX_DRIFT     = 3.0    # cm — max point-to-point drift allowed after stop
    # =========================

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for robot to move..."

    image = robot.draw_info(image)

    if td is None:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        has_sensor = "analog_read(3)" in active_code or "analog_read(4)" in active_code
        has_if     = "if " in active_code
        code_valid = has_sensor and has_if

        missing = []
        if not has_sensor:
            missing.append("analog_read(3) or analog_read(4)")
        if not has_if:
            missing.append("if statement")

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 20,
            "data": {
                "code_valid": code_valid,
                "missing": missing,
                "prev_position": None,
                "peak_displacement": 0.0,   # total movement seen before stop msg
                "stop_msg_received": False,
                "stop_msg_time": None,
                "stop_position": None,      # position snapshot when stop msg arrives
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

    # track robot position every frame
    pos = robot.position
    if pos is not None:
        prev = td["data"]["prev_position"]

        if prev is not None and not td["data"]["stop_msg_received"]:
            dx = pos[0] - prev[0]
            dy = pos[1] - prev[1]
            td["data"]["peak_displacement"] += math.sqrt(dx**2 + dy**2)
            text = f"Robot moving... displacement: {td['data']['peak_displacement']:.1f}cm"

        td["data"]["prev_position"] = pos

    # parse MQTT messages
    msg = robot.get_msg()
    if msg is not None:
        text = f"Message: {msg}"
        if not td["data"]["stop_msg_received"] and "Target found" in msg:
            td["data"]["stop_msg_received"] = True
            td["data"]["stop_msg_time"] = time.time()
            td["data"]["stop_position"] = pos  # snapshot position at stop moment
            text = "Stop message received! Checking robot..."

    # extend end_time once to allow post-stop observation
    if (td["data"]["stop_msg_received"] and
            td["data"]["stop_msg_time"] is not None and
            td["end_time"] < td["data"]["stop_msg_time"] + STOP_SETTLE_TIME):
        td["end_time"] = td["data"]["stop_msg_time"] + STOP_SETTLE_TIME

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif not td["data"]["stop_msg_received"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "No stop message received. Did the robot find the line? | Score: 0"
            text = "No stop message received."
        elif td["data"]["peak_displacement"] < MOVEMENT_MIN:
            result["success"] = False
            result["score"] = 0
            result["description"] = (
                f"Robot did not appear to move before stopping "
                f"(displacement: {td['data']['peak_displacement']:.1f}cm) | Score: 0"
            )
            text = "Robot was not moving."
        else:
            # point-to-point drift check: stop position vs current position
            drift = 0.0
            if td["data"]["stop_position"] is not None and pos is not None:
                dx = pos[0] - td["data"]["stop_position"][0]
                dy = pos[1] - td["data"]["stop_position"][1]
                drift = math.sqrt(dx**2 + dy**2)

            if drift > STOP_MAX_DRIFT:
                result["success"] = False
                result["score"] = 0
                result["description"] = (
                    f"Robot did not stop after line detected "
                    f"(drifted {drift:.1f}cm from stop position) | Score: 0"
                )
                text = "Robot did not stop."
            else:
                result["success"] = True
                result["score"] = 100
                result["description"] = (
                    f"You are amazing! Robot moved {td['data']['peak_displacement']:.1f}cm, "
                    f"detected the line and stopped (drift: {drift:.1f}cm) | Score: 100"
                )
                text = "Assignment complete!"

    return image, td, text, result


def processing_sensor_data(robot, image, td, user_code=None):
    """
    Verification for lesson: Processing Sensor Data / Geological Layers
    Students must move forward 15 times (1cm each), scan with sensors 3 and 4,
    detect when values exceed threshold (900), and send a message containing
    "Found geological layers!" with the sensor values.
    """

    # ===== CONFIGURATION =====
    TASK_DURATION        = 20           # seconds before timeout
    SENSOR_THRESHOLD     = 800          # minimum sensor value for a valid detection
    MIN_DETECTIONS       = 2            # valid above-threshold detections needed to pass
    MINERAL_POS          = (860, 500)   # (x, y) pixel position of mineral icon on screen
    POSITION_TOLERANCE   = 70           # detection radius in pixels
    ROBOT_SENSOR_OFFSET  = (100, 0)     # (x, y) offset from robot center to sensor position
    MINERAL_FLASH_SECS   = 5.0          # seconds to show mineral icon after detection
    # =========================

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Verifying..."

    image = robot.draw_info(image)

    if td is None:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 20,
            "data": {
                "total_readings": 0,
                "detections_above_threshold": 0,
                "valid_position_detections": 0,
                "mineral_display_until": 0,
                "mineral_target_x": MINERAL_POS[0] + 32,   # center of 64x64 icon
                "mineral_target_y": MINERAL_POS[1] + 32,
                "mineral_icon_x": MINERAL_POS[0],
                "mineral_icon_y": MINERAL_POS[1],
            }
        }

        # load mineral icon once at initialization
        basepath = os.path.abspath(os.path.dirname(__file__))
        try:
            mineral_img = cv2.imread(
                os.path.join(basepath, "images", "mineral.png"), cv2.IMREAD_UNCHANGED
            )
            if mineral_img is None:
                raise FileNotFoundError("mineral.png not found")

            mineral_img = cv2.resize(mineral_img, (64, 64))

            if mineral_img.shape[2] == 4:
                bgr = mineral_img[:, :, :3]
                _, mask = cv2.threshold(mineral_img[:, :, 3], 1, 255, cv2.THRESH_BINARY)
            else:
                bgr = mineral_img
                gray = cv2.cvtColor(mineral_img, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

            td["data"]["mineral"] = bgr
            td["data"]["mineral_mask"] = mask

        except Exception as e:
            print(f"Warning: Could not load mineral icon ({e}), using placeholder")
            placeholder = np.zeros((64, 64, 3), dtype=np.uint8)
            cv2.circle(placeholder, (32, 32), 28, (0, 200, 100), -1)
            td["data"]["mineral"] = placeholder
            td["data"]["mineral_mask"] = np.ones((64, 64), dtype=np.uint8) * 255

    # parse MQTT messages
    msg = robot.get_msg()
    if msg and "Found geological layers" in msg:
        for num_str in re.findall(r"\d+", msg):
            try:
                value = int(num_str)
            except ValueError:
                continue

            if not (0 <= value <= 1023):
                continue

            td["data"]["total_readings"] += 1

            if value > SENSOR_THRESHOLD:
                td["data"]["detections_above_threshold"] += 1

                robot_position = robot.get_info().get("position_px")
                if robot_position is not None:
                    sensor_x = robot_position[0] + ROBOT_SENSOR_OFFSET[0]
                    sensor_y = robot_position[1] + ROBOT_SENSOR_OFFSET[1]
                    distance = np.sqrt(
                        (sensor_x - td["data"]["mineral_target_x"]) ** 2 +
                        (sensor_y - td["data"]["mineral_target_y"]) ** 2
                    )
                    if distance <= POSITION_TOLERANCE:
                        td["data"]["valid_position_detections"] += 1
                        td["data"]["mineral_display_until"] = time.time() + MINERAL_FLASH_SECS
                        text = "MINERAL COLLECTED!"
                    else:
                        text = f"Sensor triggered, not at mineral ({distance:.0f}px away)"
                else:
                    # position unavailable — count it and flash icon
                    td["data"]["valid_position_detections"] += 1
                    td["data"]["mineral_display_until"] = time.time() + MINERAL_FLASH_SECS
                    text = "MINERAL DETECTED! (position not verified)"

    # draw mineral icon when recently triggered
    if time.time() < td["data"]["mineral_display_until"]:
        text = "MINERAL COLLECTED!"
        ix = td["data"]["mineral_icon_x"]
        iy = td["data"]["mineral_icon_y"]
        icon = td["data"]["mineral"]
        mask = td["data"]["mineral_mask"]
        ih, iw = icon.shape[:2]
        if iy + ih <= image.shape[0] and ix + iw <= image.shape[1]:
            cv2.copyTo(icon, mask, image[iy:iy + ih, ix:ix + iw])

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        valid = td["data"]["valid_position_detections"]
        total = td["data"]["detections_above_threshold"]

        if valid >= MIN_DETECTIONS:
            result["success"] = True
            result["score"] = 100
            result["description"] = (
                f"You are amazing! Found {valid} valid mineral detections "
                f"at correct location (out of {total} total triggers) | Score: 100"
            )
            text = "Verification complete!"
        else:
            result["success"] = False
            result["score"] = 0
            result["description"] = (
                f"Only {valid} detections at correct position "
                f"(need {MIN_DETECTIONS}). Total triggers: {total} | Score: 0"
            )
            text = "Verification complete!"

    return image, td, text, result


def arrays_and_elif(robot, image, td, user_code=None):
    """
    Verification for lesson: Arrays and Spatial Logic
    Students must:
    - Use analog_read_all() to read all 8 sensors
    - Extract indices 1, 3, and 6
    - Use if/elif/else to classify vein position
    - Print one of four expected strings per step
    - Print "Survey complete." after the loop
    """

    # ===== CONFIGURATION =====
    TASK_DURATION  = 20     # enough for 5 moves + settle delays
    EXPECTED_MSGS  = ["Vein: Center", "Vein: Left", "Vein: Right", "No minerals"]
    COMPLETE_MSG   = "Survey complete."
    # =========================

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for survey to begin..."

    image = robot.draw_info(image)

    if td is None:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        has_read_all  = "analog_read_all()" in active_code
        has_elif      = "elif" in active_code
        has_index_1   = "[1]" in active_code
        has_index_3   = "[3]" in active_code
        has_index_6   = "[6]" in active_code
        code_valid    = has_read_all and has_elif and has_index_1 and has_index_3 and has_index_6

        missing = []
        if not has_read_all:
            missing.append("analog_read_all()")
        if not has_elif:
            missing.append("elif statement")
        if not (has_index_1 and has_index_3 and has_index_6):
            missing.append("sensor indices [1], [3], [6]")

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 20,
            "data": {
                "code_valid": code_valid,
                "missing": missing,
                "scan_msgs": [],        # valid scan result messages received
                "complete_received": False,
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

    # parse MQTT messages
    msg = robot.get_msg()
    if msg is not None:
        text = f"Message: {msg}"
        if any(m in msg for m in EXPECTED_MSGS):
            td["data"]["scan_msgs"].append(msg)
            text = f"Scan result received ({len(td['data']['scan_msgs'])}/5): {msg}"
        if COMPLETE_MSG in msg:
            td["data"]["complete_received"] = True
            text = "Survey complete message received!"

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif not td["data"]["complete_received"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "'Survey complete.' message not received | Score: 0"
            text = "Survey complete message missing."
        elif len(td["data"]["scan_msgs"]) < 5:
            result["success"] = False
            result["score"] = 0
            result["description"] = (
                f"Only {len(td['data']['scan_msgs'])}/5 scan results received | Score: 0"
            )
            text = "Not enough scan results."
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = (
                f"You are amazing! Survey complete with {len(td['data']['scan_msgs'])} readings | Score: 100"
            )
            text = "Survey complete!"

    return image, td, text, result

def led_feedback(robot, image, td, user_code=None):
    """
    Verification for lesson: Visual Telemetry (LEDs)
    Students must:
    - Define a function that contains both .on() and .off() LED calls
    - Use machine.Pin(15) for the LED
    - Call the blink function when a vein is detected
    - Still print scan results and "Survey complete."
    """

    # ===== CONFIGURATION =====
    TASK_DURATION      = 30
    EXPECTED_MSGS      = ["Vein: Center", "Vein: Left", "Vein: Right", "No minerals"]
    COMPLETE_MSG       = "Survey complete."
    NUMBER_OF_SCANS    = 15
    # =========================

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Surveying..."

    image = robot.draw_info(image)

    if td is None:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        has_pin15    = "Pin(15" in active_code
        has_elif     = "elif" in active_code
        has_read_all = "analog_read_all()" in active_code

        # AST check: a defined function must contain both .on() and .off() calls
        has_led_fn = False
        try:
            tree = ast.parse(active_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    fn_src = ast.unparse(node)
                    if ".on()" in fn_src and ".off()" in fn_src:
                        has_led_fn = True
                        break
        except SyntaxError:
            pass

        code_valid = has_pin15 and has_led_fn and has_elif and has_read_all

        missing = []
        if not has_pin15:
            missing.append("machine.Pin(15)")
        if not has_led_fn:
            missing.append("LED blink function with .on() and .off()")
        if not has_elif:
            missing.append("elif statement")
        if not has_read_all:
            missing.append("analog_read_all()")

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 30,
            "data": {
                "code_valid":    code_valid,
                "missing":       missing,
                "scan_msgs":     [],
                "complete_received": False,
            }
        }

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

    # parse MQTT messages
    msg = robot.get_msg()
    if msg is not None:
        text = f"Message: {msg}"
        if any(m in msg for m in EXPECTED_MSGS):
            td["data"]["scan_msgs"].append(msg)
            text = f"Scan result ({len(td['data']['scan_msgs'])}/{NUMBER_OF_SCANS}): {msg}"
        if COMPLETE_MSG in msg:
            td["data"]["complete_received"] = True
            text = "Survey complete message received!"

    if td["end_time"] - time.time() < 1:
        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif not td["data"]["complete_received"]:
            result["success"] = False
            result["score"] = 0
            result["description"] = "'Survey complete.' not received | Score: 0"
            text = "Survey complete message missing."
        elif len(td["data"]["scan_msgs"]) < 5:
            result["success"] = False
            result["score"] = 0
            result["description"] = (
                f"Only {len(td['data']['scan_msgs'])}/5 scan results received | Score: 0"
            )
            text = "Not enough scan results."
        else:
            result["success"] = True
            result["score"] = 100
            result["description"] = (
                "You are amazing! Survey with LED feedback complete | Score: 100"
            )
            text = "Survey complete!"

    return image, td, text, result


def simple_line_follower(robot, image, td, user_code=None):
    """
    Verification for lesson: Simple Line Follower
    Students must:
    - Use analog_read_all() and extract scouts at indices 1 and 6
    - Use if/elif/else steering logic
    - Drive continuously through checkpoints in a while True loop
    Checkpoint detection via robot position (OpenCV).
    Flag overlays drawn at each checkpoint, turning green when hit.
    """

    # ===== CONFIGURATION =====
    TASK_DURATION     = 90
    CHECKPOINT_RADIUS = 10.0   # cm
    CHECKPOINTS       = [(103, 45), (98, 80)]
    # =========================

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for robot to start..."

    image = robot.draw_info(image)

    if td is None:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        has_read_all = "analog_read_all()" in active_code
        has_elif     = "elif" in active_code
        has_index_1  = "[1]" in active_code
        has_index_6  = "[6]" in active_code
        has_while    = "while True" in active_code
        code_valid   = has_read_all and has_elif and has_index_1 and has_index_6 and has_while

        missing = []
        if not has_read_all:
            missing.append("analog_read_all()")
        if not has_elif:
            missing.append("elif statement")
        if not (has_index_1 and has_index_6):
            missing.append("scout indices [1] and [6]")
        if not has_while:
            missing.append("while True loop")

        td = {
            "start_time": time.time(),
            "end_time":   time.time() + 90,
            "data": {
                "code_valid":            code_valid,
                "missing":               missing,
                "completed":             False,
                "completed_verdict":    False,
                "checkpoints_hit":       [],
                "checkpoints_remaining": list(CHECKPOINTS),
                "flag":                  None,
                "flag_mask":             None,
                "flag_green":            None,
                "flag_green_mask":       None,
                "image_error":           False,
            }
        }

        # Load flag images
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "flag_finish.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "flag_finish.jpg")

            flag = cv2.imread(filepath)
            if flag is None:
                raise FileNotFoundError(f"flag_finish.jpg not found at {filepath}")

            flag = cv2.resize(flag, (int(flag.shape[1] / 3), int(flag.shape[0] / 3)))
            lower_green = np.array([0, 240, 0])
            upper_green = np.array([50, 255, 50])
            mask = cv2.bitwise_not(cv2.inRange(flag, lower_green, upper_green))
            td["data"]["flag"]      = flag
            td["data"]["flag_mask"] = mask

            # Green "hit" version of the flag
            flag_green = flag.copy()
            flag_green[mask > 0] = (0, 200, 0)
            td["data"]["flag_green"]      = flag_green
            td["data"]["flag_green_mask"] = mask

        except Exception as e:
            print(f"Flag load error: {e} — falling back to circle markers")
            td["data"]["image_error"] = True

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

    # checkpoint detection
    pos = robot.position
    if pos is not None and td["data"]["checkpoints_remaining"]:
        next_cp = td["data"]["checkpoints_remaining"][0]
        dx   = pos[0] - next_cp[0]
        dy   = pos[1] - next_cp[1]
        dist = math.sqrt(dx**2 + dy**2)
        text = f"Distance to next checkpoint: {dist:.1f}cm"

        if dist < CHECKPOINT_RADIUS:
            td["data"]["checkpoints_hit"].append(next_cp)
            td["data"]["checkpoints_remaining"].pop(0)
            text = f"Checkpoint {len(td['data']['checkpoints_hit'])}/{len(CHECKPOINTS)} reached!"

            # early finish — shorten timer only, verdict handled by timeout block
            if not td["data"]["checkpoints_remaining"]:
                elapsed = time.time() - td["start_time"]
                if elapsed >= 10.0 and not td["data"]["completed"]:
                    td["data"]["completed"] = True
                    td["end_time"] = time.time() + 10.0
                text = "All checkpoints reached! Finishing..."

    msg = robot.get_msg()
    if msg is not None:
        text = f"Message: {msg}"

    # draw flag overlays
    pos_px = robot.position_px
    if pos is not None and pos_px is not None and pos[0] != 0:
        px_per_cm     = pos_px[0] / pos[0]
        radius_px     = int(CHECKPOINT_RADIUS * px_per_cm)
        flag          = td["data"]["flag"]
        flag_mask     = td["data"]["flag_mask"]
        flag_green    = td["data"]["flag_green"]
        use_flag      = not td["data"]["image_error"] and flag is not None

        hits = td["data"]["checkpoints_hit"]

        for cp_cm in CHECKPOINTS:
            cp_px_x = int(cp_cm[0] * px_per_cm)   # col (x)
            cp_px_y = int(cp_cm[1] * px_per_cm)   # row (y)
            cp_px   = (cp_px_x, cp_px_y)
            hit     = cp_cm in hits

            # Detection radius ring — green if hit, orange if not
            ring_color = (0, 200, 0) if hit else (0, 200, 255)
            cv2.circle(image, cp_px, radius_px, ring_color, 1)

            if use_flag:
                # flag.shape = (height, width, channels)
                # height → rows → y axis
                # width  → cols → x axis
                draw_flag = flag_green if hit else flag
                half_w = int(draw_flag.shape[1] / 2)
                half_h = int(draw_flag.shape[0] / 2)

                r0 = cp_px_y - half_h
                r1 = cp_px_y + (draw_flag.shape[0] - half_h)
                c0 = cp_px_x - half_w
                c1 = cp_px_x + (draw_flag.shape[1] - half_w)

                if 0 <= r0 and r1 < image.shape[0] and 0 <= c0 and c1 < image.shape[1]:
                    cv2.copyTo(draw_flag, flag_mask, image[r0:r1, c0:c1])
            else:
                color = (0, 200, 0) if hit else (0, 200, 255)
                cv2.circle(image, cp_px, 5, color, -1)

    # timeout / final verdict
    if td["end_time"] - time.time() < 1 and not td["data"].get("completed_verdict"):
        td["data"]["completed_verdict"] = True
        hit   = len(td["data"]["checkpoints_hit"])
        total = len(CHECKPOINTS)

        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"]   = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif hit < total:
            result["success"] = False
            result["score"]   = int((hit / total) * 100)
            result["description"] = (
                f"Only {hit}/{total} checkpoints reached | Score: {result['score']}"
            )
            text = f"Only {hit}/{total} checkpoints reached."
        else:
            result["success"] = True
            result["score"]   = 100
            result["description"] = f"You are amazing! All {total} checkpoints reached | Score: 100"
            text = "Line following complete!"

    return image, td, text, result

def logical_operators(robot, image, td, user_code=None):
    """
    Verification for lesson: Simple Line Follower
    Students must:
    - Use analog_read_all() and extract scouts at indices 1 and 6
    - Use if/elif/else steering logic
    - Drive continuously through checkpoints in a while True loop
    Checkpoint detection via robot position (OpenCV).
    Flag overlays drawn at each checkpoint, turning green when hit.
    """

    # ===== CONFIGURATION =====
    TASK_DURATION     = 90
    CHECKPOINT_RADIUS = 10.0   # cm
    CHECKPOINTS       = [(60, 90), (105, 60), (80, 30)]
    # =========================

    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Waiting for robot to start..."

    image = robot.draw_info(image)

    if td is None:
        lines = user_code.split('\n') if user_code else []
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        has_read_all = "analog_read_all()" in active_code
        has_elif     = "elif" in active_code
        has_while    = "while True" in active_code
        has_or       = " or " in active_code
        code_valid   = has_read_all and has_elif and has_while and has_or

        missing = []
        if not has_read_all:
            missing.append("analog_read_all()")
        if not has_elif:
            missing.append("elif statement")
        if not has_while:
            missing.append("while True loop")
        if not has_or:
            missing.append("or operator")

        td = {
            "start_time": time.time(),
            "end_time":   time.time() + 90,
            "data": {
                "code_valid":            code_valid,
                "missing":               missing,
                "checkpoints_hit":       [],
                "checkpoints_remaining": list(CHECKPOINTS),
                "flag":                  None,
                "flag_mask":             None,
                "flag_green":            None,
                "flag_green_mask":       None,
                "image_error":           False,
            }
        }

        # Load flag images
        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "flag_finish.jpg")
            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "flag_finish.jpg")

            flag = cv2.imread(filepath)
            if flag is None:
                raise FileNotFoundError(f"flag_finish.jpg not found at {filepath}")

            flag = cv2.resize(flag, (int(flag.shape[1] / 3), int(flag.shape[0] / 3)))
            lower_green = np.array([0, 240, 0])
            upper_green = np.array([50, 255, 50])
            mask = cv2.bitwise_not(cv2.inRange(flag, lower_green, upper_green))
            td["data"]["flag"]      = flag
            td["data"]["flag_mask"] = mask

            # Green "hit" version of the flag
            flag_green = flag.copy()
            flag_green[mask > 0] = (0, 200, 0)
            td["data"]["flag_green"]      = flag_green
            td["data"]["flag_green_mask"] = mask

        except Exception as e:
            print(f"Flag load error: {e} — falling back to circle markers")
            td["data"]["image_error"] = True

    if not td["data"]["code_valid"]:
        text = f"Code missing: {', '.join(td['data']['missing'])}"

    # checkpoint detection
    pos = robot.position
    if pos is not None and td["data"]["checkpoints_remaining"]:
        next_cp = td["data"]["checkpoints_remaining"][0]
        dx   = pos[0] - next_cp[0]
        dy   = pos[1] - next_cp[1]
        dist = math.sqrt(dx**2 + dy**2)
        text = f"Distance to next checkpoint: {dist:.1f}cm"

        if dist < CHECKPOINT_RADIUS:
            td["data"]["checkpoints_hit"].append(next_cp)
            td["data"]["checkpoints_remaining"].pop(0)
            text = f"Checkpoint {len(td['data']['checkpoints_hit'])}/{len(CHECKPOINTS)} reached!"

    msg = robot.get_msg()
    if msg is not None:
        text = f"Message: {msg}"

    # draw flag overlays
    pos_px = robot.position_px
    if pos is not None and pos_px is not None and pos[0] != 0:
        px_per_cm     = pos_px[0] / pos[0]
        radius_px     = int(CHECKPOINT_RADIUS * px_per_cm)
        flag          = td["data"]["flag"]
        flag_mask     = td["data"]["flag_mask"]
        flag_green    = td["data"]["flag_green"]
        use_flag      = not td["data"]["image_error"] and flag is not None

        hits = td["data"]["checkpoints_hit"]

        for cp_cm in CHECKPOINTS:
            cp_px_x = int(cp_cm[0] * px_per_cm)   # col (x)
            cp_px_y = int(cp_cm[1] * px_per_cm)   # row (y)
            cp_px   = (cp_px_x, cp_px_y)
            hit     = cp_cm in hits

            # Detection radius ring — green if hit, orange if not
            ring_color = (0, 200, 0) if hit else (0, 200, 255)
            cv2.circle(image, cp_px, radius_px, ring_color, 1)

            if use_flag:
                # flag.shape = (height, width, channels)
                # height → rows → y axis
                # width  → cols → x axis
                draw_flag = flag_green if hit else flag
                half_w = int(draw_flag.shape[1] / 2)
                half_h = int(draw_flag.shape[0] / 2)

                r0 = cp_px_y - half_h
                r1 = cp_px_y + (draw_flag.shape[0] - half_h)
                c0 = cp_px_x - half_w
                c1 = cp_px_x + (draw_flag.shape[1] - half_w)

                if 0 <= r0 and r1 < image.shape[0] and 0 <= c0 and c1 < image.shape[1]:
                    cv2.copyTo(draw_flag, flag_mask, image[r0:r1, c0:c1])
            else:
                color = (0, 200, 0) if hit else (0, 200, 255)
                cv2.circle(image, cp_px, 5, color, -1)

    # timeout / final verdict
    if td["end_time"] - time.time() < 1:
        hit   = len(td["data"]["checkpoints_hit"])
        total = len(CHECKPOINTS)

        if not td["data"]["code_valid"]:
            result["success"] = False
            result["score"]   = 0
            result["description"] = f"Code missing: {', '.join(td['data']['missing'])} | Score: 0"
            text = "Code validation failed."
        elif hit < total:
            result["success"] = False
            result["score"]   = int((hit / total) * 100)
            result["description"] = (
                f"Only {hit}/{total} checkpoints reached | Score: {result['score']}"
            )
            text = f"Only {hit}/{total} checkpoints reached."
        else:
            result["success"] = True
            result["score"]   = 100
            result["description"] = f"You are amazing! All {total} checkpoints reached | Score: 100"
            text = "Line following complete!"

    return image, td, text, result


##OLD

'''

def move_function(robot, image, td: dict, user_code=None):
    """Test: Robot must turn 180 degrees."""
    # overlay robot info on image
    image = robot.draw_info(image)

    # initialize task data
    if not td:
        current_ang = robot.compute_angle_x()
        target_ang = current_ang + 180 if current_ang < 180 else current_ang - 180
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 7,
            "target_ang": target_ang,
            "completed": False,
        }

    # default text/result
    ang = robot.compute_angle_x()
    delta_ang = abs(ang - td["target_ang"])
    text = f"Robot must turn to: {delta_ang:0.0f}"
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100,
    }

    # if within 10° of target, give 2 more seconds to settle
    if delta_ang < 10 and not td["completed"]:
        td["end_time"] = time.time() + 2
        td["completed"] = True

    # failure: ran out of time without reaching within 10°
    if (td["end_time"] - time.time()) < 1 and delta_ang > 10:
        result["success"] = False
        result["score"] = 0
        result["description"] = (
            f"Robot did not turn 180 degrees. "
            f"Final error: {delta_ang:0.0f} degrees"
        )

    # append score to description
    result["description"] += f" | Score: {result['score']}"

    return image, td, text, result



def electric_motor(robot, image, td: dict, user_code=None):
    """Test for lesson 8: Electric motor"""
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"

    image = robot.draw_info(image)

    if not td:
        td = {
            "end_time": time.time() + 7,
            "data": {}
        }

        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, 'images', 'flag_finish.jpg')

            flag = cv2.imread(filepath)

            flag = cv2.resize(flag, (int(flag.shape[1]/3), int(flag.shape[0]/3)))
            lower_green = np.array([0, 240, 0])
            upper_green = np.array([50, 255, 50])
            td["data"]["flag-mask"] = cv2.bitwise_not(cv2.inRange(flag, lower_green, upper_green))
            td["data"]["flag"] = flag
            td["data"]["reached"] = False
        except Exception as e:
            print(f"Error loading or processing image: {e}")
            td["data"]["image_error"] = True
            return image, td, f"Error processing image: {str(e)}", result

    # Only proceed with flag-related operations if we have a flag
    if not td["data"].get("image_error", False):
        # First, set the flag coordinates if they don't exist yet
        if "flag-coords" not in td["data"] and robot:
            robot_info = robot.get_info()
            position_px = robot_info["position_px"]

            if position_px is None:
                return image, td, "Robot position not detected", result

            angle = robot.compute_angle_x()

            x = position_px[0] + 150 if 90 < angle < 270 else position_px[0] - 120
            y = position_px[1] - 180 if 90 < angle < 270 else position_px[1] + 200
            td["data"]["flag-coords"] = (x, y)
            td["data"]["flag-coords-cm"] = (robot.pixels_to_cm(x), robot.pixels_to_cm(y))

        # Then, in a separate condition, draw the flag using those coordinates
        if "flag-coords" in td["data"]:
            flag = td["data"]["flag"]
            x_left = int(flag.shape[0]/2)
            x_right = flag.shape[0] - x_left
            y_bottom = int(flag.shape[1]/2)
            y_up = flag.shape[1] - y_bottom

            # Check if coordinates are within image bounds
            coords = td["data"]["flag-coords"]
            if (0 <= coords[0] - x_left < image.shape[0] and
                coords[0] + x_right < image.shape[0] and
                0 <= coords[1] - y_bottom < image.shape[1] and
                coords[1] + y_up < image.shape[1]):

                if td["data"]["reached"]:
                    # Increased rotation angle from 25 to 45 degrees
                    result_img = rotate_image(flag, 45)
                    mask = cv2.inRange(result_img, (0, 0, 0), (205, 205, 205))
                    result_img[mask > 0] = (0, 255, 0)
                    cv2.copyTo(result_img, rotate_image(td["data"]["flag-mask"], 45),
                              image[coords[0] - x_left:x_right + coords[0],
                                    coords[1] - y_bottom:y_up + coords[1]])
                else:
                    cv2.copyTo(flag, td["data"]["flag-mask"],
                              image[coords[0] - x_left:x_right + coords[0],
                                    coords[1] - y_bottom:y_up + coords[1]])

    position = robot.get_info()["position"]
    if position and "flag-coords-cm" in td["data"]:
        delta = robot.delta_points((position[1], position[0]), td["data"]["flag-coords-cm"])

        # Increased threshold from 5.1 to 7.0 cm for better detection
        if delta < 7.0:
            td["data"]["reached"] = True
            text = "The robot has reached target point!"
        else:
            text = f'Distance to target point {delta:0.1f} cm'

    if td["end_time"] - time.time() < 1 and td["data"].get("reached", False) == False:
        result["success"] = False
        result["score"] = 0
        result["description"] = "Robot did not reach the target point"

    return image, td, text, result

def closest_node(node, nodes):
    """Find the index of the closest node in a set of nodes"""
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.argmin(dist_2)

def rotate_image(image, angle):
    """Rotate an image by the given angle"""
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def differential_drive(robot, image, td, user_code=None):
    """Verification function for driving straight assignment"""
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Drive the robot in a straight line for 3 seconds"

    # Draw robot info on image
    image = robot.draw_info(image)

    # Initialize td if it's the first call
    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 10,  # Verification lasts for 10 seconds
            "data": {
                "task-failed": "",
                "failed-cone": {},
                "direction_0": None,
                "prev_robot_position": None,
                "robot_start_move_time": None,
                "robot_end_move_time": None,
                "max_angle_deviation": 0,
                "straight_driving_start": None,
                "straight_driving_duration": 0
            }
        }

        try:
            basepath = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basepath, "auto_tests", "images", "traffic-sign.jpg")

            if not os.path.exists(filepath):
                filepath = os.path.join(basepath, "images", "traffic-sign.jpg")

            if not os.path.exists(filepath):
                # Create a simple colored cone as fallback
                cone = np.zeros((100, 100, 3), dtype=np.uint8)
                cone[:, :] = (0, 0, 255)  # Red rectangle
            else:
                cone = cv2.imread(filepath)
                cone = cv2.resize(cone, (int(cone.shape[1]), int(cone.shape[0])))

            # Define green color range
            lower_green = np.array([0, 240, 0])
            upper_green = np.array([35, 255, 35])

            td["data"]["cone-mask"] = cv2.bitwise_not(cv2.inRange(cone, lower_green, upper_green))
            td["data"]["cone"] = cone
            td["data"]["cones-coords"] = []
        except Exception as e:
            print(f"Error initializing drive straight test: {e}")
            td["data"]["image_error"] = True

    # Set up cone coordinates if robot detected and coordinates not set
    if robot and robot.position_px and len(td["data"].get("cones-coords", [])) == 0:
        # Define cone positions to create a corridor
        y_u = robot.position_px[1] - 150  # Upper row of cones
        y_d = robot.position_px[1] + 150  # Lower row of cones
        for i in range(10):
            x = robot.position_px[0] + (i % 5) * 200
            if i < 5:
                td["data"]["cones-coords"].append((y_u, x))
            else:
                td["data"]["cones-coords"].append((y_d, x))

        # Save initial direction when robot is first detected
        if td["data"]["direction_0"] is None:
            td["data"]["direction_0"] = robot.compute_angle_x()
            if td["data"]["direction_0"] > 180:
                td["data"]["direction_0"] -= 360

    # Draw cones if we have coordinates and cone image
    if "cones-coords" in td["data"] and "cone" in td["data"] and len(td["data"]["cones-coords"]) > 0:
        try:
            cone = td["data"]["cone"]
            x_left = int(cone.shape[0] / 2)
            x_right = cone.shape[0] - x_left
            y_bottom = int(cone.shape[1] / 2)
            y_up = cone.shape[1] - y_bottom

            for i in range(min(10, len(td["data"]["cones-coords"]))):
                coords = td["data"]["cones-coords"][i]

                # Check if coordinates are within image bounds
                if (0 <= coords[0] - x_left < image.shape[0] and
                    coords[0] + x_right < image.shape[0] and
                    0 <= coords[1] - y_bottom < image.shape[1] and
                    coords[1] + y_up < image.shape[1]):

                    if i in td["data"]["failed-cone"]:
                        result_img = rotate_image(cone, td["data"]["failed-cone"][i])
                        cv2.copyTo(
                            result_img,
                            rotate_image(td["data"]["cone-mask"], td["data"]["failed-cone"][i]),
                            image[coords[0] - x_left:x_right + coords[0],
                                 coords[1] - y_bottom:y_up + coords[1]]
                        )
                        if td["data"]["failed-cone"][i] > -89:
                            td["data"]["failed-cone"][i] -= 45
                    else:
                        cv2.copyTo(
                            cone,
                            td["data"]["cone-mask"],
                            image[coords[0] - x_left:x_right + coords[0],
                                 coords[1] - y_bottom:y_up + coords[1]]
                        )
        except Exception as e:
            print(f"Error drawing cones: {e}")

    # Process robot movement
    if robot and robot.position is not None:
        # Get current angle
        angle_x = robot.compute_angle_x()
        angle_x_disp = angle_x

        if angle_x > 180:
            angle_x -= 360

        # Calculate angle difference (account for wrap-around at 360°)
        if td["data"]["direction_0"] is not None:
            angle_diff = abs(td["data"]["direction_0"] - angle_x)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            # Track maximum deviation
            td["data"]["max_angle_deviation"] = max(td["data"]["max_angle_deviation"], angle_diff)

            text = f'Robot angle with x: {angle_x_disp:0.0f}°, Deviation: {angle_diff:.1f}°'

            # Check robot movement
            if td["data"]["prev_robot_position"] is not None:
                delta_pos = robot.delta_points(robot.position, td["data"]["prev_robot_position"])

                # Detect when robot starts moving
                if td["data"]["robot_start_move_time"] is None and delta_pos > 1:
                    td["data"]["robot_start_move_time"] = time.time()
                    td["data"]["straight_driving_start"] = time.time()
                    text = f"Robot started moving at angle {angle_x_disp:0.0f}°"

                # While robot is moving, check if it's staying within deviation limits
                if td["data"]["robot_start_move_time"] is not None and delta_pos > 0.5:
                    # If deviation is within limits and we're tracking straight driving
                    if angle_diff <= 10 and td["data"]["straight_driving_start"] is not None:
                        # Calculate current straight driving duration
                        current_time = time.time()
                        td["data"]["straight_driving_duration"] = current_time - td["data"]["straight_driving_start"]

                        # Update text to show progress
                        if td["data"]["straight_driving_duration"] >= 3.0:
                            text = f"Success! Robot drove straight for {td['data']['straight_driving_duration']:.1f}s"
                            td["data"]["task-failed"] = ""  # Clear any failure state
                        else:
                            text = f"Straight: {td['data']['straight_driving_duration']:.1f}/3.0s, Deviation: {angle_diff:.1f}°"

                    # If deviation exceeds limits
                    elif angle_diff > 10:
                        # Reset straight driving timer
                        td["data"]["straight_driving_start"] = None
                        td["data"]["straight_driving_duration"] = 0

                        # Set task as failed if not already
                        if not td["data"]["task-failed"]:
                            td["data"]["task-failed"] = f"Robot deviated {angle_diff:.1f}° (max allowed: 10°)"

                            # Find closest cone to knock down
                            if robot.position_px is not None and len(td["data"]["cones-coords"]) > 0:
                                min_index = closest_node((robot.position_px[1], robot.position_px[0]),
                                                       td["data"]["cones-coords"])
                                if min_index not in td["data"]["failed-cone"]:
                                    td["data"]["failed-cone"][min_index] = -20

                # Detect when robot stops moving
                if td["data"]["robot_start_move_time"] is not None and delta_pos < 0.5:
                    if td["data"]["robot_end_move_time"] is None:
                        td["data"]["robot_end_move_time"] = time.time()

                        # If it didn't drive straight for 3 seconds before stopping
                        if td["data"]["straight_driving_duration"] < 3.0 and not td["data"]["task-failed"]:
                            td["data"]["task-failed"] = f"Robot only drove straight for {td['data']['straight_driving_duration']:.1f}s (need 3.0s)"

        # Store current position for next frame
        td["data"]["prev_robot_position"] = robot.position

    # Check for task completion or failure
    if td["end_time"] - time.time() < 1:
        if td["data"]["task-failed"]:
            result["success"] = False
            result["description"] = td["data"]["task-failed"]
            result["score"] = 0
        elif td["data"].get("robot_start_move_time") is None:
            result["success"] = False
            result["description"] = "Robot didn't start moving"
            result["score"] = 0
        elif td["data"]["straight_driving_duration"] >= 3.0:
            result["success"] = True
            result["description"] = f"Success! Robot drove straight for {td['data']['straight_driving_duration']:.1f} seconds with max deviation of {td['data']['max_angle_deviation']:.1f}°"
            result["score"] = 100
        else:
            result["success"] = False
            result["description"] = f"Robot only drove straight for {td['data']['straight_driving_duration']:.1f}s (need 3.0s)"
            result["score"] = 0

    return image, td, text, result

#NEW

def intro_to_octoliner(robot, image, td, code):
    """
    Octoliner Introduction Task - Verify student reads sensor 3 or 4
    Uses state-lock pattern to prevent result overwriting by platform
    """

    # ===== 0. INITIAL RESULT TEMPLATE =====
    # CRITICAL: Always start with success=True (platform requirement)
    result = {
        "success": True,
        "description": "You are amazing! The Robot has completed the assignment",
        "score": 100
    }
    text = "Not recognized"

    # ===== 1. FIRST-RUN INITIALIZATION =====
    if td is None:
        # Code validation - check for analog_read(3) or analog_read(4)
        # Filter out commented lines to avoid false positives
        lines = code.split('\n')
        active_lines = [line.split('#')[0] for line in lines]
        active_code = '\n'.join(active_lines)

        has_sensor_3 = "analog_read(3)" in active_code
        has_sensor_4 = "analog_read(4)" in active_code

        code_valid = has_sensor_3 or has_sensor_4
        missing = [] if code_valid else ["analog_read(3) or analog_read(4)"]

        td = {
            "start_time": time.time(),
            "end_time": time.time() + 20,
            "data": {
                "sensor_3": None,
                "sensor_4": None,
                "completed": False,
                "code_valid": code_valid,
                "missing_functions": missing
            }
        }

    # ===== 2. STATE LOCK - Early Return if Already Completed =====
    # If task already completed, return saved result immediately
    # This prevents platform from overwriting our result
    if td["data"].get("completed", False):
        final_result = td["data"].get("final_result", result)
        final_text = td["data"].get("final_text", text)

        # Still draw sensor values on video
        image = robot.draw_info(image)
        if td["data"]["sensor_3"] is not None:
            cv2.putText(image, f"Sensor 3: {td['data']['sensor_3']}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        if td["data"]["sensor_4"] is not None:
            cv2.putText(image, f"Sensor 4: {td['data']['sensor_4']}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

        return image, td, final_text, final_result

    # ===== 3. DRAWING & TELEMETRY =====
    image = robot.draw_info(image)

    info = robot.get_info()
    robot_position = info.get('position')
    if robot_position is not None:
        text = f'Robot position: x: {robot_position[0]:0.1f} y: {robot_position[1]:0.1f}'

    # Display sensor values on video overlay
    if td["data"]["sensor_3"] is not None:
        cv2.putText(image, f"Sensor 3: {td['data']['sensor_3']}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
    if td["data"]["sensor_4"] is not None:
        cv2.putText(image, f"Sensor 4: {td['data']['sensor_4']}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

    # ===== 4. MESSAGE PROCESSING =====
    msg = robot.get_msg()

    if td["data"]["code_valid"] and msg is not None:
        # Extract numbers from message (e.g., "Sensor 3: 450")
        numbers = [int(num) for num in re.findall(r'\d+', msg)]
        if numbers:
            # Store first number in empty sensor slot
            if td["data"]["sensor_3"] is None:
                td["data"]["sensor_3"] = numbers[0]
            elif td["data"]["sensor_4"] is None:
                td["data"]["sensor_4"] = numbers[0]

        # Update text to show message received
        text = f"Message received: {msg}"

    # ===== 5. EVALUATION LOGIC =====
    elapsed = time.time() - td["start_time"]
    timeout_reached = time.time() >= td["end_time"]
    got_sensor_data = (td["data"]["sensor_3"] is not None or
                       td["data"]["sensor_4"] is not None)

    if td["data"]["code_valid"]:
        # Code is valid - check if we got data or timed out
        if got_sensor_data or timeout_reached:
            td["data"]["completed"] = True  # Set completion flag FIRST

            if got_sensor_data:
                # SUCCESS: Got sensor reading
                result = {
                    "success": True,
                    "score": 100,
                    "description": f"Perfect! Sensor reading received: S3={td['data']['sensor_3']}, S4={td['data']['sensor_4']}"
                }
                text = "Assignment complete!"
            else:
                # FAIL: Timeout without data
                result = {
                    "success": False,  # Safe because completed=True is set
                    "score": 0,
                    "description": "Timeout: No sensor readings received"
                }
                text = "No readings received."
    else:
        # Code validation failed - wait 3 seconds before failing
        # This gives MQTT time to stabilize
        if elapsed > 3.0:
            td["data"]["completed"] = True  # Set completion flag FIRST
            result = {
                "success": False,  # Safe because completed=True is set
                "score": 0,
                "description": f"Code missing required functions: {', '.join(td['data']['missing_functions'])}"
            }
            text = "Code validation failed."

    # ===== 6. SAVE FINAL STATE =====
    # Store result in td so state lock can return it on subsequent frames
    if td["data"]["completed"]:
        td["data"]["final_result"] = result
        td["data"]["final_text"] = text

    return image, td, text, result


def processing_sensor_data(robot, image, td, user_code=None):
    """
    Verification function for geological layers detection assignment.

    Students must:
    - Move forward 15 times (1cm each)
    - Scan with sensors 3 and 4
    - Detect when sensor values exceed threshold (900)
    - Send message containing "Found geological layers!" with sensor values
    """

    # ========== CONFIGURATION - EDIT THESE VALUES ==========
    mineral_pos = (670, 500)          # (x, y) position of mineral icon on screen
    position_tolerance = 50           # Detection radius in pixels
    sensor_threshold = 900            # Minimum sensor value for detection
    detection_time = 20               # Time limit in seconds
    min_detections = 2                # Minimum valid detections required to pass
    robot_position_offset = (100, 0)  # (x, y) offset from robot center to sensor position
    # ========================================================

    result = {
        "success": True,
        "description": "Scanning for geological layers...",
        "score": 100
    }
    text = "Verifying..."

    # Initialize task data on first frame
    if not td:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + detection_time,
            "data": {
                "detections_above_threshold": 0,
                "total_readings": 0,
                "last_detection_time": None,
                "mineral_display_until": 0,
                "mineral_icon_x": mineral_pos[0],
                "mineral_icon_y": mineral_pos[1],
                "mineral_target_x": mineral_pos[0] + 32,  # Center of icon
                "mineral_target_y": mineral_pos[1] + 32,
                "position_tolerance": position_tolerance,
                "sensor_threshold": sensor_threshold,
                "robot_offset_x": robot_position_offset[0],
                "robot_offset_y": robot_position_offset[1],
                "valid_position_detections": 0,
            }
        }

        # Load mineral icon (one-time setup)
        basepath = os.path.abspath(os.path.dirname(__file__))

        try:
            mineral_img = cv2.imread(os.path.join(basepath, "images", "mineral.png"), cv2.IMREAD_UNCHANGED)

            if mineral_img is None:
                print("Warning: mineral.png not found, using placeholder")
                mineral_img = np.zeros((64, 64, 4), dtype=np.uint8)
                cv2.circle(mineral_img, (32, 32), 28, (0, 255, 0, 255), -1)

            if mineral_img.shape[0] != 64 or mineral_img.shape[1] != 64:
                mineral_img = cv2.resize(mineral_img, (64, 64))

            if mineral_img.shape[2] == 4:  # PNG with alpha channel
                bgr = mineral_img[:, :, :3]
                alpha = mineral_img[:, :, 3]
                _, mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)
                td["data"]["mineral"] = bgr
                td["data"]["mineral-mask"] = mask
            else:
                gray = cv2.cvtColor(mineral_img, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
                td["data"]["mineral"] = mineral_img
                td["data"]["mineral-mask"] = mask

        except Exception as e:
            print(f"Error loading mineral icon: {e}")
            mineral_img = np.zeros((64, 64, 3), dtype=np.uint8)
            mineral_img[:, :] = (0, 200, 100)
            mask = np.ones((64, 64), dtype=np.uint8) * 255
            td["data"]["mineral"] = mineral_img
            td["data"]["mineral-mask"] = mask

    # Draw robot info overlay
    image = robot.draw_info(image)

    # Parse incoming MQTT messages
    msg = robot.get_msg()
    if msg and "Found geological layers" in msg:
        numbers = re.findall(r"\d+", msg)

        for num_str in numbers:
            try:
                value = int(num_str)
            except ValueError:
                continue

            if 0 <= value <= 1023:
                td["data"]["total_readings"] += 1

                if value > td["data"]["sensor_threshold"]:
                    td["data"]["detections_above_threshold"] += 1
                    td["data"]["last_detection_time"] = time.time()

                    robot_position = robot.get_info().get("position_px")

                    if robot_position is not None:
                        sensor_x = robot_position[0] + td["data"]["robot_offset_x"]
                        sensor_y = robot_position[1] + td["data"]["robot_offset_y"]
                        target_x = td["data"]["mineral_target_x"]
                        target_y = td["data"]["mineral_target_y"]

                        distance = np.sqrt((sensor_x - target_x)**2 + (sensor_y - target_y)**2)

                        if distance <= td["data"]["position_tolerance"]:
                            td["data"]["valid_position_detections"] += 1
                            td["data"]["mineral_display_until"] = time.time() + 2.0
                            text = "MINERAL COLLECTED!"
                        else:
                            text = f"Sensor triggered, not at mineral ({distance:.0f}px away)"
                    else:
                        td["data"]["mineral_display_until"] = time.time() + 2.0
                        text = "MINERAL DETECTED! (position not verified)"

    # Show mineral icon when recently detected
    if time.time() < td["data"]["mineral_display_until"]:
        text = "MINERAL COLLECTED!"
        icon_x = td["data"]["mineral_icon_x"]
        icon_y = td["data"]["mineral_icon_y"]
        icon_height = td["data"]["mineral"].shape[0]
        icon_width = td["data"]["mineral"].shape[1]

        if (icon_y + icon_height <= image.shape[0] and
                icon_x + icon_width <= image.shape[1]):
            cv2.copyTo(
                td["data"]["mineral"],
                td["data"]["mineral-mask"],
                image[icon_y:icon_y + icon_height,
                      icon_x:icon_x + icon_width]
            )

    # Check if time is up
    if time.time() > td["end_time"]:
        if td["data"]["valid_position_detections"] >= min_detections:
            text = "Verification complete!"
            result["description"] = (
                f"Assignment passed! Found {td['data']['valid_position_detections']} "
                f"valid mineral detections at correct location "
                f"(out of {td['data']['detections_above_threshold']} total sensor triggers)."
            )
        else:
            result["success"] = False
            result["description"] = (
                f"Assignment Failed! Only {td['data']['valid_position_detections']} "
                f"detections at correct position (need at least {min_detections}). "
                f"Total sensor triggers: {td['data']['detections_above_threshold']}"
            )
            result["score"] = 0
            text = "Verification complete!"

    return image, td, text, result

'''
