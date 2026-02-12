# `task_test` Developer Guide

This document explains how to implement and use a custom verification function named `task_test` for **DevSubmit** checks.

---

## 1) Where `task_test` is used

In the developer verification flow (`DevSubmit`):

1. Verification code is loaded dynamically.
2. The function (default name: `task_test`) is called on each new camera frame.
3. The function returns updated runtime state and pass/fail status.

The worker executes the function in a loop inside `dev_verification`.

---

## 2) Required function signature

Use this signature:

```python
def task_test(robot, frame, td, code):
    ...
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `robot` | Robot object (`RobotBasic` implementation) | Yes | Current robot interface + telemetry/position fields. |
| `frame` | OpenCV image (`numpy.ndarray`, BGR) | Yes | Current frame from input video stream. |
| `td` | `dict` or `None` | Yes | Persistent test state between calls (first call receives `None`). |
| `code` | `str` | Yes | User code text passed to verification context. |

---

## 3) Required return contract

Your function must return **exactly 4 values**:

```python
return frame, td, text_for_output, result
```

### Return fields

| Return value | Type | Required | Description |
|---|---|---:|---|
| `frame` | `numpy.ndarray` | Yes | Frame (original or annotated) pushed to output stream. |
| `td` | `dict` | Yes | Updated test state. **Must include `end_time`.** |
| `text_for_output` | `str` | Yes | Status text sent to frontend during verification. |
| `result` | `dict` | Yes | Test result dictionary. **Must include `success` and `description`.** |

### `result` dictionary

Minimum required keys:

```python
result = {
    "success": True or False,
    "description": "human-readable status"
}
```

Recommended key:

```python
"score": 0..100
```

If `score` is missing, worker fallback is:
- `100` when `success=True`
- `0` when `success=False`

---

## 4) Runtime rules you must follow

### 4.1 Initialize `td` on first call

`td` is `None` on first invocation. Initialize it once:

```python
if td is None:
    td = {
        "start_time": time.time(),
        "end_time": time.time() + 20.0,
    }
```

### 4.2 Always keep `td["end_time"]`

Worker logic relies on `td["end_time"]` to stop verification.

### 4.3 Pass/fail behavior

- Verification is considered failed immediately when `result["success"]` is `False`.
- Verification can also end when current time exceeds `td["end_time"]`.

### 4.4 Keep function frame-safe

The function is called frequently; avoid long blocking operations inside `task_test`.

---

## 5) Robot coordinates and orientation

The worker updates robot position from camera frames before calling your function.

### 5.1 Position fields

Typical fields (depending on robot implementation):

- `robot.position`: `(x_cm, y_cm)` in centimeters.
- `robot.position_px`: `(x_px, y_px)` in pixels.

### 5.2 Units

- **Pixels**: image-space units.
- **Centimeters**: converted from pixels via DPI in robot implementation.

### 5.3 Axis directions (camera/image coordinates)

The coordinate system follows image conventions:

- Origin `(0, 0)` is **top-left** of the frame.
- `x` increases to the **right**.
- `y` increases **downward**.

ASCII diagram:

```text
(0,0)  +----------------------> +X
       |
       |
       |
       v
      +Y
```

### 5.4 Orientation / heading

For `RobotESP32MicroPython`, heading is computed as angle vs +X axis:

- `robot.compute_angle_x()` -> degrees in range `[0, 360)`.
- Angle depends on detected robot marker orientation in the current frame.

---

## 6) Example 1 — minimal valid function

```python
import time

def task_test(robot, frame, td, code):
    if td is None:
        td = {
            "start_time": time.time(),
            "end_time": time.time() + 5.0,
        }

    done = time.time() >= td["end_time"]

    result = {
        "success": done,
        "description": "Timer completed" if done else "Waiting...",
        "score": 100 if done else 0,
    }

    text_for_output = result["description"]
    return frame, td, text_for_output, result
```

Behavior: waits 5 seconds, then passes.

---

## 7) Example 2 — position-based success

```python
import time
import math

def task_test(robot, frame, td, code):
    if td is None:
        td = {
            "end_time": time.time() + 20.0,
            "target": (35.0, 50.0),
            "tolerance_cm": 3.0,
        }

    pos = getattr(robot, "position", None)
    if pos is None:
        result = {
            "success": False,
            "description": "Robot marker not detected",
            "score": 0,
        }
        return frame, td, result["description"], result

    dx = pos[0] - td["target"][0]
    dy = pos[1] - td["target"][1]
    dist = math.hypot(dx, dy)

    reached = dist <= td["tolerance_cm"]

    result = {
        "success": reached,
        "description": f"Distance to target: {dist:.2f} cm",
        "score": 100 if reached else max(0, int(100 - dist * 10)),
    }

    return frame, td, result["description"], result
```

Behavior: passes when robot center enters tolerance radius around target point.

---

## 8) Example 3 — defensive failure handling

```python
import time

def task_test(robot, frame, td, code):
    if td is None:
        td = {
            "end_time": time.time() + 10.0,
        }

    angle = None
    if hasattr(robot, "compute_angle_x"):
        angle = robot.compute_angle_x()

    if angle is None:
        result = {
            "success": False,
            "description": "Cannot compute robot orientation",
            "score": 0,
        }
        return frame, td, result["description"], result

    ok = 0 <= angle < 360
    result = {
        "success": ok,
        "description": f"Heading: {angle:.1f} deg",
        "score": 100 if ok else 0,
    }
    return frame, td, result["description"], result
```

Behavior: fails gracefully if orientation is not available.

---

## 9) Common mistakes checklist

Before running DevSubmit, verify:

- [ ] Function name matches `function_name` (default `task_test`).
- [ ] Function returns exactly 4 values.
- [ ] `td` is initialized when `None`.
- [ ] `td` always has `end_time`.
- [ ] `result` always has `success` and `description`.
- [ ] You do not confuse `position` (cm) and `position_px` (pixels).
- [ ] You use image coordinates (`y` grows downward), not math Cartesian Y-up.
- [ ] Per-frame logic is lightweight and non-blocking.

---

## 10) Quick mapping to worker behavior

- Validation step checks your function can run and verifies required keys in `td` and `result`.
- Runtime loop calls your function repeatedly and pushes your `text_for_output` to frontend.
- Final message/status are derived from `result` (`success`, `description`, `score`).
