import time
from lineRobot import Robot

robot = Robot()

def detect_color_name(r, g, b):
    total = r + g + b
    try:
        r_ratio = r / total
        g_ratio = g / total
    except ZeroDivisionError:
        print("CRITICAL: Sensor Blind!")
        return "Unknown"
    if r_ratio > 0.4:
        return "Red"
    elif g_ratio > 0.4:
        return "Green"
    return "Floor"

scans = [(140,30,30),(0,0,0),(50,150,50),(0,0,0),(0,0,0),(60,60,60),(150,40,40),(0,0,0),(40,140,40),(70,70,70)]
for scan_num, (r, g, b) in enumerate(scans, 1):
    robot.run_motors_speed(25, -25)
    time.sleep(0.2)
    robot.stop()
    print(f"Sector #{scan_num} | RGB: ({r},{g},{b})")
    color = detect_color_name(r, g, b)
    print(f"ANALYSIS: {color}")
    time.sleep(0.1)
print("Survey Complete")
