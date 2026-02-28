import time
from result import Result

def verify_sandbox(robot, image, dataTest):
    """ Basic sandbox verification:
    Checks whether robot was detected at least once in 3 seconds """

    #initialize verification window only once
    if dataTest.end_time is None:
        dataTest.end_time = time.time() + 3
        dataTest.data["robot_seen"] = False

    text = "Robot not detected yet"
    success = False
    desc = "Robot was not detected during verification"

    #if robot detected in current frame
    if robot:
        dataTest.data["robot_seen"] = True
        text = f"Robot detected at position {robot.center}"

    #when time window ends, decide result
    if time.time() > dataTest.end_time:
        if dataTest.data["robot_seen"]:
            success = True
            desc = "Robot was successfully detected during verification"
        else:
            success = False
            desc = "Robot was never detected"

    return dataTest, text, Result(success, desc)

