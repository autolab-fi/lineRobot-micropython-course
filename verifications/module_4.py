import cv2
import math
import time
import os
import numpy as np

target_points = {
    'encoders': [(30, 50), (30, 0)],
}

block_library_functions = {
    'encoders': False,
}


def get_block_library_functions(task):
    """Retrieve block library status for a given task."""
    return block_library_functions.get(task, False)


def get_target_points(task):
    """Retrieve target points for a given task."""
    return target_points.get(task, [])

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
                'messages': [],         
                'encoder_pairs': [],    
                'current_pair': {},     
                'stage': 'start'        
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
            pairs_str = ", ".join([f"({l}, {r})" for l,r in td["data"]['encoder_pairs']])
            result["success"] = False
            result["description"] = f"Not enough encoders data: {pairs_str}"
            result["score"] = 0
        else:
            start_pair = td["data"]['encoder_pairs'][0]    
            end_pair = td["data"]['encoder_pairs'][-1]     
            

            left_change = abs(end_pair[0] - start_pair[0])   
            right_change = abs(end_pair[1] - start_pair[1])  
            
           
            tolerance = 40   
            expected = 360    
            

            if not (330 <= left_change <= 400 and 330 <= right_change <= 400):
                result["success"] = False
                result["description"] = (f"Incorrect rotation. Left changed: {left_change:.1f}°, "
                                      f"Right changed: {right_change:.1f}°. "
                                      f"Expected: {expected}° ±{tolerance}°")
                result["score"] = 0
            else:
                result["success"] = True
                result["description"] = f"Success! Left wheel: {left_change:.1f}°, Right wheel: {right_change:.1f}°"
                result["score"] = 100
    
    return image, td, text, result
