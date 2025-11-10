import ast
import cv2
import numpy as np
import time

LINE_SENSOR_THRESHOLD = 120

EXPECTED_ROBOT_STATUSES = {
    "robot1": {"battery": 3, "status": "critical"},
    "robot2": {"battery": 8, "status": "warn"},
    "robot3": {"battery": 10, "status": "ok"},
}

ALLOWED_STATUS_VALUES = {info["status"] for info in EXPECTED_ROBOT_STATUSES.values()}


target_points = {
    'line_sensor_leds': [(30, 50), (0, -200)],
    'analog_led_fade': [(30, 50), (0, -200)],
    'telemetry_heartbeat_health': [(30, 50), (0, -200)],
}

block_library_functions = {
    'line_sensor_leds': False,
    'analog_led_fade': False,
    'telemetry_heartbeat_health': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])


def _initial_td(message):
    return {
        "end_time": time.time() + 10,
        "data": {
            "validated": False,
            "error": message,
            "messages": [],
        },
        "finished": False,
        "finish_time": None,
    }


def line_sensor_leds(robot, image, td):
    """Verify that LED state reflects the middle line sensor readings."""
    result = {
        "success": True,
        "description": "Awaiting LINE_LED summary...",
        "score": 0,
    }
    text = "Listening for LINE_LED message..."
    image = robot.draw_info(image)

    if not td:
        td = _initial_td("No LINE_LED message received yet.")
        td["data"]["state"] = None
        td["data"]["line_seen"] = None

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        if msg.startswith("LINE_LED:"):
            payload = msg[len("LINE_LED:") :]
            parts = payload.split(";") if payload else []
            values = {}
            try:
                for part in parts:
                    if "=" not in part:
                        raise ValueError("Each LINE_LED field must contain an '=' sign.")
                    key, value = part.split("=", 1)
                    values[key.strip()] = value.strip()
                state = values["state"].lower()
                if state not in {"on", "off"}:
                    raise ValueError("State must be 'on' or 'off'.")
                readings_raw = values["readings"]
                readings = ast.literal_eval(readings_raw)
                if not isinstance(readings, list) or len(readings) < 5:
                    raise ValueError("Readings must be a list containing at least five values.")
                numbers = [int(v) for v in readings]
            except KeyError as missing:
                td["data"]["error"] = f"Missing field: {missing.args[0]}"
            except (ValueError, SyntaxError) as exc:
                td["data"]["error"] = str(exc)
            else:
                centre = numbers[2:6] if len(numbers) >= 6 else numbers
                line_seen = any(value < LINE_SENSOR_THRESHOLD for value in centre)
                if state == "on" and not line_seen:
                    td["data"]["error"] = "State is 'on' but centre readings are above the threshold."
                elif state == "off" and line_seen:
                    td["data"]["error"] = "State is 'off' but centre readings indicate the line is present."
                else:
                    td["data"]["validated"] = True
                    td["data"]["error"] = ""
                td["data"]["state"] = state
                td["data"]["line_seen"] = "yes" if line_seen else "no"
        else:
            td["data"]["error"] = "Message must start with 'LINE_LED:'."

    cv2.putText(
        image,
        f"Messages received: {len(td['data']['messages'])}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        image,
        f"Time remaining: {td['end_time'] - time.time():.1f}s",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    if td["data"].get("error"):
        cv2.putText(
            image,
            f"Error: {td['data']['error']}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )

    state = td["data"].get("state")
    if state:
        cv2.putText(
            image,
            f"Reported state: {state}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
    seen = td["data"].get("line_seen")
    if seen:
        cv2.putText(
            image,
            f"Line detected: {seen}",
            (20, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

    if not td.get("finished", False):
        if td["data"]["validated"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result.update(
                {
                    "success": True,
                    "description": "LINE_LED message validated successfully!",
                    "score": 100,
                }
            )
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get("error", "No valid LINE_LED message received.")
            text = "Verification failed."
        else:
            result["success"] = True
            result["description"] = td["data"].get("error", result["description"])
    else:
        if time.time() - td["finish_time"] >= 3:
            if td["data"]["validated"]:
                result["success"] = True
                result["score"] = 100
            else:
                result["success"] = False
                result["score"] = 0

    return image, td, text, result


def analog_led_fade(robot, image, td):
    """Verify that the LEDs flash six times with roughly two-second spacing."""

    result = {
        "success": True,
        "description": "Watching for timed LED flashes...",
        "score": 0,
    }
    text = "Detecting LED state..."
    image = robot.draw_info(image)

    if not td:
        td = _initial_td("LED flash pattern not detected yet.")
        td["end_time"] = time.time() + 40
        td["data"].update(
            {
                "state_buffer": [],
                "last_state": None,
                "state_started": None,
                "last_change": None,
                "flashes": 0,
                "last_on_time": None,
                "intervals": [],
                "durations_on": [],
                "durations_off": [],
            }
        )
        td["data"]["error"] = ""

    now = time.time()

    robot_info = robot.get_info()
    position = robot_info.get("position_px") if robot_info else None

    led_on = False
    if position is not None:
        crop_x = int(position[0] + 80)
        crop_y = int(position[1] - 90)
        crop_w, crop_h = 80, 180

        height, width, _ = image.shape
        crop_x = max(0, min(crop_x, width - crop_w))
        crop_y = max(0, min(crop_y, height - crop_h))

        region = image[crop_y : crop_y + crop_h, crop_x : crop_x + crop_w]
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([180, 60, 255]))
        white_pixels = cv2.countNonZero(mask)
        total_pixels = mask.size
        led_on = (white_pixels / max(total_pixels, 1)) > 0.02

        cv2.rectangle(image, (crop_x, crop_y), (crop_x + crop_w, crop_y + crop_h), (0, 255, 0), 1)

    buffer = td["data"]["state_buffer"]
    buffer.append(led_on)
    if len(buffer) > 5:
        buffer.pop(0)
    smoothed_state = sum(buffer) > len(buffer) / 2 if buffer else False

    last_state = td["data"].get("last_state")
    if last_state is None:
        td["data"]["last_state"] = smoothed_state
        td["data"]["state_started"] = now
        td["data"]["last_change"] = now
        if smoothed_state:
            td["data"]["flashes"] = 1
            td["data"]["last_on_time"] = now
    elif smoothed_state != last_state:
        last_change = td["data"].get("last_change")
        if last_change is None or now - last_change >= 0.3:
            duration = now - td["data"]["state_started"]
            if last_state:
                td["data"]["durations_on"].append(duration)
            else:
                td["data"]["durations_off"].append(duration)

            td["data"]["last_state"] = smoothed_state
            td["data"]["state_started"] = now
            td["data"]["last_change"] = now

            if smoothed_state:
                td["data"]["flashes"] += 1
                last_on = td["data"].get("last_on_time")
                if last_on is not None:
                    td["data"]["intervals"].append(now - last_on)
                td["data"]["last_on_time"] = now

    flashes = td["data"].get("flashes", 0)
    intervals = td["data"].get("intervals", [])

    if flashes >= 6 and len(intervals) >= 5:
        recent_intervals = intervals[-5:]
        if all(1.7 <= interval <= 2.3 for interval in recent_intervals):
            td["data"]["validated"] = True
            td["data"]["error"] = ""
        else:
            td["data"]["error"] = "Intervals between flashes must be about two seconds."

    cv2.putText(
        image,
        f"Flashes counted: {flashes}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )
    if intervals:
        last_interval = intervals[-1]
        cv2.putText(
            image,
            f"Last interval: {last_interval:.2f}s",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

    remaining = td["end_time"] - now
    cv2.putText(
        image,
        f"Time remaining: {remaining:.1f}s",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    if td["data"].get("error"):
        cv2.putText(
            image,
            f"Error: {td['data']['error']}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )

    if not td.get("finished", False):
        if td["data"].get("validated"):
            td["finished"] = True
            td["finish_time"] = now
            result.update(
                {
                    "success": True,
                    "description": "Detected six LED flashes with two-second spacing!",
                    "score": 100,
                }
            )
            text = "Verification successful!"
        elif now > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = now
            result["success"] = False
            result["description"] = td["data"].get(
                "error", "Did not detect the required LED flash pattern."
            )
            text = "Verification failed."
        else:
            result["success"] = True
            result["description"] = td["data"].get("error", result["description"])
    else:
        if now - td["finish_time"] >= 3:
            if td["data"].get("validated"):
                result["success"] = True
                result["score"] = 100
            else:
                result["success"] = False
                result["score"] = 0

    return image, td, text, result


def _parse_robot_status_line(line: str):
    """Parse a status line of the form 'robotX status=... battery=...'."""

    cleaned = line.strip()
    if not cleaned:
        return None, "Received an empty status line."

    parts = cleaned.replace(",", " ").replace(";", " ").split()
    if not parts:
        return None, "Unable to parse the status line."

    name = parts[0]
    if name not in EXPECTED_ROBOT_STATUSES:
        return None, f"Unexpected robot name '{name}'."

    fields = {}
    for token in parts[1:]:
        if "=" not in token:
            return None, "Each status line must include key=value pairs after the name."
        key, value = token.split("=", 1)
        key = key.lower().strip()
        value = value.strip().lower()
        if key in fields:
            return None, f"Duplicate field '{key}' detected."
        fields[key] = value

    if "status" not in fields or "battery" not in fields:
        return None, "Include both status=... and battery=... after the robot name."

    try:
        battery_value = int(fields["battery"])
    except ValueError as exc:
        return None, f"Battery value must be an integer: {exc}"

    status_value = fields["status"]
    if status_value not in ALLOWED_STATUS_VALUES:
        return None, "Status must be one of ok, warn, or critical."

    return {
        "name": name,
        "status": status_value,
        "battery": battery_value,
    }, None


def telemetry_heartbeat_health(robot, image, td):
    """Validate three printed robot status summaries."""
    result = {
        "success": True,
        "description": "Waiting for robot status lines...",
        "score": 0,
    }
    text = "Listening for status lines..."
    image = robot.draw_info(image)

    if not td:
        td = _initial_td("No robot status lines received yet.")
        td["end_time"] = time.time() + 20
        td["data"]["reports"] = {}

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        parsed, error = _parse_robot_status_line(msg)
        if error:
            td["data"]["error"] = error
        else:
            expected = EXPECTED_ROBOT_STATUSES[parsed["name"]]
            if parsed["status"] != expected["status"]:
                td["data"]["error"] = (
                    f"{parsed['name']} status must be {expected['status']}."
                )
            elif parsed["battery"] != expected["battery"]:
                td["data"]["error"] = (
                    f"{parsed['name']} battery must be {expected['battery']}."
                )
            else:
                td["data"]["error"] = ""
                td["data"]["reports"][parsed["name"]] = parsed
                if len(td["data"]["reports"]) == len(EXPECTED_ROBOT_STATUSES):
                    td["data"]["validated"] = True

    cv2.putText(
        image,
        f"Messages received: {len(td['data']['messages'])}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        image,
        f"Time remaining: {td['end_time'] - time.time():.1f}s",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    if td["data"].get("reports"):
        y = 120
        for name in sorted(td["data"]["reports"]):
            report = td["data"]["reports"][name]
            cv2.putText(
                image,
                f"{name}: status={report['status']} battery={report['battery']}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )
            y += 25

    if td["data"].get("error"):
        cv2.putText(
            image,
            f"Error: {td['data']['error']}",
            (20, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )

    if not td.get("finished", False):
        if td["data"].get("validated"):
            td["finished"] = True
            td["finish_time"] = time.time()
            result.update(
                {
                    "success": True,
                    "description": "All robot status lines validated successfully!",
                    "score": 100,
                }
            )
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get(
                "error", "Did not receive all robot status lines in time."
            )
            text = "Verification failed."
        else:
            result["success"] = True
            result["description"] = td["data"].get(
                "error", result["description"]
            )
    else:
        if time.time() - td["finish_time"] >= 3:
            if td["data"].get("validated"):
                result["success"] = True
                result["score"] = 100
            else:
                result["success"] = False
                result["score"] = 0

    return image, td, text, result
