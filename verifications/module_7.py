import cv2
import math
import time
import os
import numpy as np

target_points = {
    'introduction_to_variables_and_conditional_statements': [(35, 50), (0,-200)],
    'loops_and_conditional_logic': [(35, 50), (30, 0)],
    'array_and_processing_data': [(30, 50), (30, 0)],
}

block_library_functions = {
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

def introduction_to_variables_and_conditional_statements(robot, image, td):
    """
    Verification function that checks if at least one sensor (0-7) is detected as ON THE LINE.
    """
    result = {
        "success": True,  # Start with success assumption
        "description": "Waiting for sensor messages...",
        "score": 100
    }
    
    # Use a consistent verification message until the end
    text = "Verifying..."
    
    # Draw robot info on image
    image = robot.draw_info(image)
    
    # Initialize test data if not already set
    if not td:
        td = {
            "end_time": time.time() + 10,  # 10 seconds verification time
            "data": {
                "sensors_on_line": set(),  # Track which sensors are detected as on the line
                "messages": [],
                "start_time": time.time(),
                "result_displayed": False  # Flag to track if final result is displayed
            }
        }
    
    # Get message from robot
    msg = robot.get_msg()
    if msg is not None:
        # Store all messages
        td["data"]["messages"].append(msg)
        
        # Check for any sensor ON LINE messages (0-7)
        for sensor_num in range(8):
            if f"SENSOR {sensor_num} ON LINE" in msg.upper():
                td["data"]["sensors_on_line"].add(sensor_num)
    
    # Check if time has expired
    if time.time() > td["end_time"]:
        # Set the final result text only once when time expires
        if not td["data"]["result_displayed"]:
            td["data"]["result_displayed"] = True
            
            if td["data"]["sensors_on_line"]:  # If any sensor is on the line
                result["success"] = True
                detected_sensors = ", ".join(str(s) for s in sorted(td["data"]["sensors_on_line"]))
                result["description"] = f"Assignment passed! Detected sensors on line: {detected_sensors}"
                text = "Verification successful!"
            else:
                result["success"] = False
                
                if not td["data"]["messages"]:
                    result["description"] = "No messages received from robot."
                else:
                    result["description"] = "No sensor was detected as ON LINE."
                
                text = "Verification failed."
                result["score"] = 0
    
    return image, td, text, result

def loops_and_conditional_logic(robot, image, td):
    """
    Robust verification function that waits for the full time period
    before making any pass/fail decision.
    """
    result = {
        "success": True,  # Start with success assumption
        "description": "Collecting sensor data...",
        "score": 100
    }
    text = "Verifying sensor values..."
    
    # Draw robot info on image
    image = robot.draw_info(image)
    
    # Initialize test data if not already set
    if not td:
        td = {
            "end_time": time.time() + 15,  # 15 seconds verification time
            "data": {
                "sensor_values": {},  # Store sensor values as they come in
                "sensors_above_threshold": set(),  # Track which sensors are above threshold
                "messages": [],
                "start_time": time.time(),
                "verification_complete": False  # Flag to ensure we only complete once
            }
        }
    
    # Get message from robot
    msg = robot.get_msg()
    if msg is not None:
        # Store message
        td["data"]["messages"].append(msg)
        
        # Parse sensor messages in format "Sensor X: Y"
        if "Sensor" in msg and ":" in msg:
            try:
                # Split by colon and extract parts
                parts = msg.split(":")
                if len(parts) == 2:
                    sensor_part = parts[0].strip()
                    value_part = parts[1].strip()
                    
                    # Extract sensor number
                    sensor_num = int(sensor_part.replace("Sensor", "").strip())
                    
                    # Extract sensor value
                    sensor_val = int(value_part)
                    
                    # Store the sensor value
                    td["data"]["sensor_values"][sensor_num] = sensor_val
                    
                    # Check if value is above threshold
                    if sensor_val > 200:
                        td["data"]["sensors_above_threshold"].add(sensor_num)
            except:
                # If parsing fails, just continue
                pass
    
    # CRITICAL: Do not change success/score until time expires
    # This prevents immediate failure
    
    # Check if time has expired - ONLY place we set success/failure
    if time.time() > td["end_time"] and not td["data"]["verification_complete"]:
        td["data"]["verification_complete"] = True
        sensors_above_threshold = len(td["data"]["sensors_above_threshold"])
        
        if sensors_above_threshold >= 2:
            result["success"] = True
            above_threshold_list = ", ".join(str(s) for s in sorted(td["data"]["sensors_above_threshold"]))
            result["description"] = f"Assignment passed! Found {sensors_above_threshold} sensors > 200: {above_threshold_list}"
            result["score"] = 100
        else:
            result["success"] = False
            if sensors_above_threshold == 0:
                result["description"] = "No sensors detected with values > 200."
            else:
                result["description"] = "Assignment Failed"
            result["score"] = 0
        
        text = "Verification complete!"
    
    return image, td, text, result
def array_and_processing_data(robot, image, td):
    """
    Verification function that passes if at least 2 sensor values are above 200.
    """
    result = {
        "success": True,
        "description": "Checking for values above 200...",
        "score": 100
    }
    text = "Verifying..."
    
    # Draw robot info on image
    image = robot.draw_info(image)
    
    # Initialize test data if not already set
    if not td:
        td = {
            "end_time": time.time() + 15,
            "data": {
                "values_above_200": 0,
                "total_values": 0,  # Added for debugging
                "start_time": time.time()
            }
        }
    
    # Get message from robot
    msg = robot.get_msg()
    if msg is not None:
        # Extract any number from the message
        import re
        numbers = re.findall(r'\d+', msg)
        
        for num_str in numbers:
            try:
                value = int(num_str)
                # Check if it's a reasonable sensor value (0-1023 range)
                if 0 <= value <= 1023:
                    td["data"]["total_values"] += 1  # Count all valid values
                    if value > 200:
                        td["data"]["values_above_200"] += 1
            except:
                pass
    
    # Display debugging info on image
    cv2.putText(image, f"Total values received: {td['data']['total_values']}", 
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.putText(image, f"Values above 200: {td['data']['values_above_200']}", 
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Check if time has expired
    if time.time() > td["end_time"]:
        if td["data"]["values_above_200"] >= 2:
            result["success"] = True
            result["description"] = f"Assignment passed! Found {td['data']['values_above_200']} values > 200 out of {td['data']['total_values']} total values"
            result["score"] = 100
        else:
            result["success"] = False
            result["description"] = "Assignment Failed!"
            result["score"] = 0
        
        text = "Verification complete!"
    
    return image, td, text, result