import ast
import cv2
import time
import re
import ast

target_points = {
    'hello_mqtt_variables': [(30, 50), (0, -200)],
    'mission_time_report': [(30, 50), (0, -200)],
    'sensor_log_summary': [(30, 50), (0, -200)],
    'list_operations_check': [(30, 50), (0, -200)],
    'introduction_to_variables_and_conditional_statements': [(30, 50), (0, -200)],
    'loops_and_conditional_logic': [(65, 50), (30, 0)],
    'array_and_processing_data': [(30, 50), (30, 0)],
}

block_library_functions = {
    'hello_mqtt_variables': False,
    'mission_time_report': False,
    'sensor_log_summary': False,
    'list_operations_check': False,
    'introduction_to_variables_and_conditional_statements': False,
    'loops_and_conditional_logic': False,
    'array_and_processing_data': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])


def hello_mqtt_variables(robot, image, td):
    result = {
        "success": True,  # Changed to True to keep running
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
            parts = payload.split(";")
            if len(parts) == 4:
                values = {}
                for part in parts:
                    if "=" not in part:
                        td["data"]["error"] = "Each STATUS field must contain an '=' sign."
                        break
                    key, value = part.split("=", 1)
                    values[key.strip()] = value.strip()
                else:
                    try:
                        name = values["name"]
                        speed = int(values["speed"])
                        battery = float(values["battery"])
                        ready_value = values["ready"]
                        if ready_value not in {"True", "False"}:
                            raise ValueError("Ready must be True or False.")
                    except KeyError as missing:
                        td["data"]["error"] = f"Missing field: {missing.args[0]}"
                    except ValueError as exc:
                        td["data"]["error"] = str(exc)
                    else:
                        if not name:
                            td["data"]["error"] = "Robot name must not be empty."
                        elif not (1 <= speed <= 200):
                            td["data"]["error"] = "Speed must be an integer between 1 and 200 cm/s."
                        elif not (0.0 < battery < 20.0):
                            td["data"]["error"] = "Battery voltage must be between 0 and 20 volts."
                        else:
                            td["data"]["validated"] = True
                            td["data"]["error"] = ""
            else:
                td["data"]["error"] = "STATUS message must contain four fields separated by semicolons."
        else:
            td["data"]["error"] = "Message must start with 'STATUS:'."

    # Display current status on screen
    cv2.putText(image, f"Messages received: {len(td['data']['messages'])}", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(image, f"Time remaining: {td['end_time'] - time.time():.1f}s", 
                (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    if td["data"]["error"]:
        cv2.putText(image, f"Error: {td['data']['error']}", 
                    (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Only mark as finished once
    if not td.get("finished", False):
        if td["data"]["validated"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result.update({
                "success": True,
                "description": "STATUS message validated successfully!",
                "score": 100,
            })
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get("error", "No valid STATUS message received.")
            text = "Verification failed."
        else:
            # Keep running
            result["success"] = True
            result["description"] = td["data"].get("error", result["description"])
    else:
        # Show result for 3 seconds before ending
        if time.time() - td["finish_time"] >= 3:
            # Actually end by setting success to final state
            if td["data"]["validated"]:
                result["success"] = True
                result["score"] = 100
            else:
                result["success"] = False
                result["score"] = 0

    return image, td, text, result


def mission_time_report(robot, image, td):
    result = {
        "success": True,  # Changed to True to keep running
        "description": "Awaiting mission report...",
        "score": 0,
    }
    text = "Listening for mission report..."
    image = robot.draw_info(image)

    if not td:
        td = {
            "end_time": time.time() + 10,
            "data": {
                "validated": False,
                "error": "No mission report received yet.",
                "messages": [],
            },
            "finished": False,
            "finish_time": None,
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        if msg.startswith("MISSION:"):
            payload = msg[len("MISSION:") :]
            parts = payload.split(";")
            expected_order = ["distance", "speed", "time"]
            if len(parts) == 3:
                values = {}
                for expected, part in zip(expected_order, parts):
                    if "=" not in part:
                        td["data"]["error"] = "Each mission field must contain an '=' sign."
                        break
                    key, value = part.split("=", 1)
                    key = key.strip()
                    if key != expected:
                        td["data"]["error"] = "Mission fields must appear as distance, speed, time."
                        break
                    values[key] = value.strip()
                else:
                    try:
                        if values["distance"] != "120cm":
                            raise ValueError("Distance must be 120cm.")
                        if values["speed"] != "18.0cm/s":
                            raise ValueError("Speed must be 18.0cm/s.")
                        if not values["time"].endswith("s"):
                            raise ValueError("Time field must end with 's'.")
                        time_value = float(values["time"][:-1])
                    except ValueError as exc:
                        td["data"]["error"] = str(exc)
                    else:
                        expected_time = 120 / 18.0
                        if abs(time_value - expected_time) <= 0.05:
                            td["data"]["validated"] = True
                            td["data"]["error"] = ""
                        else:
                            td["data"]["error"] = "Computed time is outside the allowed tolerance."
            else:
                td["data"]["error"] = "Mission report must contain three fields."
        else:
            td["data"]["error"] = "Message must start with 'MISSION:'."

    # Display current status on screen
    cv2.putText(image, f"Messages received: {len(td['data']['messages'])}", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(image, f"Time remaining: {td['end_time'] - time.time():.1f}s", 
                (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    if td["data"]["error"]:
        cv2.putText(image, f"Error: {td['data']['error']}", 
                    (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Only mark as finished once
    if not td.get("finished", False):
        if td["data"]["validated"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result.update({
                "success": True,
                "description": "Mission report validated successfully!",
                "score": 100,
            })
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get("error", "No valid mission report received.")
            text = "Verification failed."
        else:
            # Keep running
            result["success"] = True
            result["description"] = td["data"].get("error", result["description"])
    else:
        # Show result for 3 seconds before ending
        if time.time() - td["finish_time"] >= 3:
            # Actually end by setting success to final state
            if td["data"]["validated"]:
                result["success"] = True
                result["score"] = 100
            else:
                result["success"] = False
                result["score"] = 0

    return image, td, text, result


def sensor_log_summary(robot, image, td):
    result = {
        "success": True,  # Changed to True to keep running
        "description": "Awaiting LOG messages...",
        "score": 0,
    }
    text = "Listening for sensor log messages..."
    image = robot.draw_info(image)

    if not td:
        td = {
            "end_time": time.time() + 12,
            "data": {
                "count": None,
                "values": None,
                "average": None,
                "validated": False,
                "error": "Waiting for LOG:COUNT, LOG:VALUES, and LOG:AVERAGE messages.",
                "messages": [],
            },
            "finished": False,
            "finish_time": None,
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        if msg.startswith("LOG:COUNT="):
            try:
                td["data"]["count"] = int(msg.split("=", 1)[1])
            except ValueError:
                td["data"]["error"] = "LOG:COUNT must contain an integer."
        elif msg.startswith("LOG:VALUES="):
            values_part = msg.split("=", 1)[1]
            if values_part:
                try:
                    values = [int(v.strip()) for v in values_part.split(",")]
                except ValueError:
                    td["data"]["error"] = "LOG:VALUES must contain integers separated by commas."
                else:
                    td["data"]["values"] = values
            else:
                td["data"]["error"] = "LOG:VALUES must list at least one value."
        elif msg.startswith("LOG:AVERAGE="):
            try:
                td["data"]["average"] = float(msg.split("=", 1)[1])
            except ValueError:
                td["data"]["error"] = "LOG:AVERAGE must contain a number."

        if all(td["data"][key] is not None for key in ("count", "values", "average")):
            values = td["data"]["values"]
            if td["data"]["count"] != len(values):
                td["data"]["error"] = "Count does not match the number of values provided."
            elif len(values) == 0:
                td["data"]["error"] = "Provide at least one sensor value."
            else:
                average = sum(values) / len(values)
                if abs(average - td["data"]["average"]) <= 0.05:
                    td["data"]["validated"] = True
                    td["data"]["error"] = ""
                else:
                    td["data"]["error"] = "Reported average does not match the values provided."

    # Display current status on screen
    cv2.putText(image, f"Messages received: {len(td['data']['messages'])}", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(image, f"Time remaining: {td['end_time'] - time.time():.1f}s", 
                (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Show received data status
    status_y = 120
    if td["data"]["count"] is not None:
        cv2.putText(image, f"COUNT: {td['data']['count']}", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        status_y += 25
    if td["data"]["values"] is not None:
        cv2.putText(image, f"VALUES: {len(td['data']['values'])} received", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        status_y += 25
    if td["data"]["average"] is not None:
        cv2.putText(image, f"AVERAGE: {td['data']['average']}", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        status_y += 25
    
    if td["data"]["error"] and not td["data"]["validated"]:
        cv2.putText(image, f"Error: {td['data']['error']}", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Only mark as finished once
    if not td.get("finished", False):
        if td["data"]["validated"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result.update({
                "success": True,
                "description": "Sensor log summary validated successfully!",
                "score": 100,
            })
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get("error", "Sensor log messages were incomplete.")
            text = "Verification failed."
        else:
            # Keep running
            result["success"] = True
            result["description"] = td["data"].get("error", result["description"])
    else:
        # Show result for 3 seconds before ending
        if time.time() - td["finish_time"] >= 3:
            # Actually end by setting success to final state
            if td["data"]["validated"]:
                result["success"] = True
                result["score"] = 100
            else:
                result["success"] = False
                result["score"] = 0

    return image, td, text, result

def list_operations_check(robot, image, td):
    result = {
        "success": True,  # Changed to True to keep running
        "description": "Awaiting LIST messages...",
        "score": 0,
    }
    text = "Listening for list messages..."
    image = robot.draw_info(image)

    if not td:
        td = {
            "end_time": time.time() + 12,
            "data": {
                "items": None,
                "length": None,
                "validated": False,
                "error": "Waiting for LIST:items and LIST:length messages.",
                "messages": [],
            },
            "finished": False,
            "finish_time": None,
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        if msg.startswith("LIST:items="):
            payload = msg.split("=", 1)[1].strip()
            try:
                parsed_items = ast.literal_eval(payload)
            except (ValueError, SyntaxError):
                td["data"]["error"] = "Unable to parse LIST:items payload as a Python list."
            else:
                if not isinstance(parsed_items, list):
                    td["data"]["error"] = "LIST:items payload must represent a list."
                elif len(parsed_items) < 3:
                    td["data"]["error"] = "List must contain at least three items."
                elif len({type(item) for item in parsed_items}) < 2:
                    td["data"]["error"] = "List must contain at least two different data types."
                else:
                    td["data"]["items"] = parsed_items
                    td["data"]["error"] = ""
        elif msg.startswith("LIST:length="):
            try:
                td["data"]["length"] = int(msg.split("=", 1)[1])
            except ValueError:
                td["data"]["error"] = "LIST:length must contain an integer."

        if td["data"]["items"] is not None and td["data"]["length"] is not None:
            if len(td["data"]["items"]) == td["data"]["length"]:
                td["data"]["validated"] = True
                td["data"]["error"] = ""
            else:
                td["data"]["error"] = "LIST:length does not match the number of items provided."

    # Display current status on screen
    cv2.putText(image, f"Messages received: {len(td['data']['messages'])}", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(image, f"Time remaining: {td['end_time'] - time.time():.1f}s", 
                (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Show received data status
    status_y = 120
    if td["data"]["items"] is not None:
        item_preview = str(td["data"]["items"])[:50] + "..." if len(str(td["data"]["items"])) > 50 else str(td["data"]["items"])
        cv2.putText(image, f"ITEMS: {item_preview}", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        status_y += 25
        # Show item count and types
        types_in_list = {type(item).__name__ for item in td["data"]["items"]}
        cv2.putText(image, f"Types: {', '.join(types_in_list)}", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        status_y += 25
    
    if td["data"]["length"] is not None:
        cv2.putText(image, f"LENGTH: {td['data']['length']}", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        status_y += 25
    
    if td["data"]["error"] and not td["data"]["validated"]:
        # Word wrap error message if too long
        error_msg = td["data"]["error"]
        if len(error_msg) > 60:
            error_msg = error_msg[:60] + "..."
        cv2.putText(image, f"Error: {error_msg}", 
                    (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Only mark as finished once
    if not td.get("finished", False):
        if td["data"]["validated"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result.update({
                "success": True,
                "description": "List operations validated successfully!",
                "score": 100,
            })
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get("error", "List messages were incomplete.")
            text = "Verification failed."
        else:
            # Keep running
            result["success"] = True
            result["description"] = td["data"].get("error", result["description"])
    else:
        # Show result for 3 seconds before ending
        if time.time() - td["finish_time"] >= 3:
            # Actually end by setting success to final state
            if td["data"]["validated"]:
                result["success"] = True
                result["score"] = 100
            else:
                result["success"] = False
                result["score"] = 0

    return image, td, text, result


def introduction_to_variables_and_conditional_statements(robot, image, td):
    """Check that at least one sensor is reported as ON LINE within the allotted time."""
    result = {
        "success": True,
        "description": "Waiting for sensor messages...",
        "score": 100,
    }
    text = "Verifying..."
    image = robot.draw_info(image)
    if not td:
        td = {
            "end_time": time.time() + 10,
            "data": {
                "sensors_on_line": set(),
                "messages": [],
                "result_displayed": False,
            },
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        for sensor_num in range(8):
            if f"SENSOR {sensor_num} ON LINE" in msg.upper():
                td["data"]["sensors_on_line"].add(sensor_num)

    if time.time() > td["end_time"] and not td["data"]["result_displayed"]:
        td["data"]["result_displayed"] = True
        if td["data"]["sensors_on_line"]:
            detected = ", ".join(str(s) for s in sorted(td["data"]["sensors_on_line"]))
            result["description"] = f"Assignment passed!"
            text = "Verification successful!"
        else:
            result.update({
                "success": False,
                "description": "Assignment failed!",
                "score": 0,
            })
            text = "Verification failed."
    return image, td, text, result


def loops_and_conditional_logic(robot, image, td):
    result = {
        "success": True,
        "description": "Collecting sensor data...",
        "score": 100,
    }
    text = "Verifying sensor values..."
    image = robot.draw_info(image)
    if not td:
        td = {
            "end_time": time.time() + 15,
            "data": {
                "sensor_values": {},
                "sensors_above_threshold": set(),
                "messages": [],
                "verification_complete": False,
            },
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["messages"].append(msg)
        if "Sensor" in msg and ":" in msg:
            try:
                parts = msg.split(":")
                if len(parts) == 2:
                    sensor_part = parts[0].strip()
                    value_part = parts[1].strip()
                    sensor_num = int(sensor_part.replace("Sensor", "").strip())
                    sensor_val = int(value_part)
                    td["data"]["sensor_values"][sensor_num] = sensor_val
                    if sensor_val > 200:
                        td["data"]["sensors_above_threshold"].add(sensor_num)
            except Exception:
                pass

    if time.time() > td["end_time"] and not td["data"]["verification_complete"]:
        td["data"]["verification_complete"] = True
        sensors_above = len(td["data"]["sensors_above_threshold"])
        if sensors_above >= 2:
            text = "Verification complete!"
        else:
            result.update({
                "success": False,
                "description": "No sensors detected on Line." if sensors_above == 0 else "Assignment Failed",
                "score": 0,
            })
            text = "Verification complete!"
    return image, td, text, result


def array_and_processing_data(robot, image, td):
    result = {
        "success": True,
        "description": "Checking for values above 200...",
        "score": 100,
    }
    text = "Verifying..."
    image = robot.draw_info(image)
    if not td:
        td = {
            "end_time": time.time() + 15,
            "data": {
                "values_above_200": 0,
                "total_values": 0,
            },
        }

    msg = robot.get_msg()
    if msg is not None:
        numbers = re.findall(r"\d+", msg)
        for num_str in numbers:
            try:
                value = int(num_str)
            except ValueError:
                continue
            if 0 <= value <= 1023:
                td["data"]["total_values"] += 1
                if value > 200:
                    td["data"]["values_above_200"] += 1

    if time.time() > td["end_time"]:
        if td["data"]["values_above_200"] >= 2:
            text = "Verification complete!"
            result["description"] = (
                f"Assignment passed!"
                f"out of {td['data']['total_values']} total values"
            )
        else:
            result.update({
                "success": False,
                "description": "Assignment Failed!",
                "score": 0,
            })
            text = "Verification complete!"
    return image, td, text, result
