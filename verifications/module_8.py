import ast
import cv2
import time

LINE_SENSOR_THRESHOLD = 120
MAX_FADE_STEP = 64
HEALTH_LEVELS = {"ok", "warn", "low"}
HEALTH_WARN_VOLTAGE = 9.0
HEALTH_LOW_VOLTAGE = 7.0
HEALTH_WARN_SPEED = 10


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
    """Verify that the LED fade publishes a PWM step list."""
    result = {
        "success": True,
        "description": "Awaiting LED_FADE profile...",
        "score": 0,
    }
    text = "Listening for LED_FADE message..."
    image = robot.draw_info(image)

    if not td:
        td = _initial_td("No LED_FADE message received yet.")
        td["data"]["steps"] = []

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        if msg.startswith("LED_FADE:"):
            payload = msg[len("LED_FADE:") :]
            parts = payload.split(";") if payload else []
            values = {}
            try:
                for part in parts:
                    if "=" not in part:
                        raise ValueError("Each LED_FADE field must contain an '=' sign.")
                    key, value = part.split("=", 1)
                    values[key.strip()] = value.strip()
                steps_raw = values["steps"]
                steps = ast.literal_eval(steps_raw)
                if not isinstance(steps, list) or len(steps) < 5:
                    raise ValueError("Steps must be a list with at least five values.")
                numbers = [int(v) for v in steps]
                if numbers[0] != 0 or numbers[-1] != 0:
                    raise ValueError("Fade must start and end at 0.")
                if max(numbers) < 200:
                    raise ValueError("Fade must reach at least 200 to demonstrate full brightness.")
                if max(numbers) > 255 or min(numbers) < 0:
                    raise ValueError("Steps must be between 0 and 255.")
                for a, b in zip(numbers, numbers[1:]):
                    if abs(a - b) > MAX_FADE_STEP:
                        raise ValueError("Adjacent steps must change by 64 or less for a smooth fade.")
                increasing = any(b > a for a, b in zip(numbers, numbers[1:]))
                decreasing = any(b < a for a, b in zip(numbers, numbers[1:]))
                if not (increasing and decreasing):
                    raise ValueError("Fade must include both increasing and decreasing sections.")
            except KeyError as missing:
                td["data"]["error"] = f"Missing field: {missing.args[0]}"
            except (ValueError, SyntaxError) as exc:
                td["data"]["error"] = str(exc)
            else:
                td["data"]["validated"] = True
                td["data"]["error"] = ""
                td["data"]["steps"] = numbers
        else:
            td["data"]["error"] = "Message must start with 'LED_FADE:'."

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

    steps = td["data"].get("steps")
    if steps:
        preview = ", ".join(map(str, steps[:6]))
        if len(steps) > 6:
            preview += ", ..."
        cv2.putText(
            image,
            f"Steps: [{preview}]",
            (20, 150),
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
                    "description": "LED_FADE profile validated successfully!",
                    "score": 100,
                }
            )
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get("error", "No valid LED_FADE message received.")
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


def _classify_health(speed: int, battery: float, ready: bool) -> str:
    """Return the expected health classification for the provided telemetry."""
    if battery < HEALTH_LOW_VOLTAGE or speed <= 0:
        return "low"
    if battery < HEALTH_WARN_VOLTAGE or speed < HEALTH_WARN_SPEED or not ready:
        return "warn"
    return "ok"


def _validate_status_payload(payload: str, *, require_health: bool, allow_optional_health: bool):
    """Validate a STATUS payload and return parsed values or an error message."""

    parts = payload.split(";") if payload else []

    min_fields = 5 if require_health else 4
    max_fields = 5 if (require_health or allow_optional_health) else 4
    if len(parts) < min_fields or len(parts) > max_fields:
        if require_health:
            return None, "STATUS message must contain five fields separated by semicolons."
        if allow_optional_health:
            return None, "STATUS message must contain four or five fields separated by semicolons."
        return None, "STATUS message must contain four fields separated by semicolons."

    values = {}
    for part in parts:
        if "=" not in part:
            return None, "Each STATUS field must contain an '=' sign."
        key, value = part.split("=", 1)
        values[key.strip()] = value.strip()

    required_fields = {"name", "speed", "battery", "ready"}
    missing = [field for field in required_fields if field not in values]
    if missing:
        return None, f"Missing field: {missing[0]}"

    allowed_fields = set(required_fields)
    if require_health or (allow_optional_health and "health" in values):
        allowed_fields.add("health")

    unexpected = set(values) - allowed_fields
    if unexpected:
        field = unexpected.pop()
        return None, f"Unexpected field: {field}"

    try:
        name = values["name"]
        speed = int(values["speed"])
        battery = float(values["battery"])
        ready_value = values["ready"]
        if ready_value not in {"True", "False"}:
            raise ValueError("Ready must be True or False.")
    except ValueError as exc:
        return None, str(exc)

    if not name:
        return None, "Robot name must not be empty."
    if not (1 <= speed <= 200):
        return None, "Speed must be an integer between 1 and 200 cm/s."
    if not (0.0 < battery < 20.0):
        return None, "Battery voltage must be between 0 and 20 volts."

    ready = ready_value == "True"
    expected_health = _classify_health(speed, battery, ready)

    reported_health = values.get("health")
    if require_health or (allow_optional_health and reported_health is not None):
        if reported_health is None:
            return None, "Missing field: health"
        reported_health = reported_health.lower()
        if reported_health not in HEALTH_LEVELS:
            return None, "Health must be one of ok, warn, or low."
        if reported_health != expected_health:
            return None, f"Health flag should be '{expected_health}' for the provided telemetry."

    return {
        "name": name,
        "speed": speed,
        "battery": battery,
        "ready": ready,
        "ready_raw": ready_value,
        "reported_health": values.get("health"),
        "expected_health": expected_health,
    }, None


def _verify_status_message(robot, image, td, *, require_health: bool, allow_optional_health: bool):
    result = {
        "success": True,
        "description": "Awaiting STATUS message...",
        "score": 0,
    }
    text = "Listening for STATUS message..."
    image = robot.draw_info(image)

    if not td:
        td = {
            "end_time": time.time() + 10,
            "data": {
                "validated": False,
                "error": "No STATUS message received yet.",
                "messages": [],
                "expected_health": None,
                "reported_health": None,
            },
            "finished": False,
            "finish_time": None,
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        if msg.startswith("STATUS:"):
            payload = msg[len("STATUS:") :]
            parsed, error = _validate_status_payload(
                payload,
                require_health=require_health,
                allow_optional_health=allow_optional_health,
            )
            if error:
                td["data"]["error"] = error
            else:
                td["data"]["validated"] = True
                td["data"]["error"] = ""
                td["data"]["expected_health"] = parsed["expected_health"]
                td["data"]["reported_health"] = parsed["reported_health"]
        else:
            td["data"]["error"] = "Message must start with 'STATUS:'."

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

    if td["data"].get("expected_health") is not None:
        expected = td["data"]["expected_health"]
        reported = td["data"].get("reported_health")
        display = reported if reported is not None else "(not reported)"
        cv2.putText(
            image,
            f"Expected health: {expected}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        cv2.putText(
            image,
            f"Reported health: {display}",
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
                    "description": "STATUS message validated successfully!",
                    "score": 100,
                }
            )
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get("error", "No valid STATUS message received.")
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


def telemetry_heartbeat_health(robot, image, td):
    """Validate STATUS heartbeat that includes a derived health flag."""
    return _verify_status_message(
        robot,
        image,
        td,
        require_health=True,
        allow_optional_health=False,
    )
