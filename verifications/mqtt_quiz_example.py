import cv2
import time
import re

target_points = {
    "mqtt_quiz_example": [(30, 50), (0, -200)],
}

block_library_functions = {
    "mqtt_quiz_example": False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])


def mqtt_quiz_example(robot, image, td):
    result = {
        "success": True,
        "description": "Awaiting ANSWER message...",
        "score": 0,
    }
    text = "Listening for ANSWER message..."
    image = robot.draw_info(image)

    if not td:
        td = {
            "end_time": time.time() + 10,
            "data": {
                "validated": False,
                "error": "No ANSWER message received yet.",
                "messages": [],
                "last_answer": None,
            },
            "finished": False,
            "finish_time": None,
        }

    msg = robot.get_msg()
    if msg is not None:
        td["data"]["last_answer"] = msg.strip()
        td["data"]["messages"].append(msg)
        text = f"Received: {msg}"
        match = re.match(r"^ANSWER:([+-]?\d+)$", msg.strip())
        if match:
            try:
                value = int(match.group(1))
            except ValueError:
                td["data"]["error"] = "Answer must be an integer."
            else:
                if value == 42:
                    td["data"]["validated"] = True
                    td["data"]["error"] = ""
                else:
                    td["data"]["error"] = "Answer must be 42."
        else:
            td["data"]["error"] = "Message must match 'ANSWER:<number>'."

    last_answer = td["data"].get("last_answer") or "ANSWER:..."
    answer_color = (0, 255, 0) if td["data"]["validated"] else (0, 0, 255)
    cv2.putText(
        image,
        f"Received: {last_answer}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        answer_color,
        2,
    )

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

    if td["data"]["error"]:
        cv2.putText(
            image,
            f"Error: {td['data']['error']}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )

    if not td.get("finished", False):
        if td["data"]["validated"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result.update(
                {
                    "success": True,
                    "description": "ANSWER message validated successfully!",
                    "score": 100,
                }
            )
            text = "Verification successful!"
        elif time.time() > td["end_time"]:
            td["finished"] = True
            td["finish_time"] = time.time()
            result["success"] = False
            result["description"] = td["data"].get(
                "error", "No valid ANSWER message received."
            )
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
