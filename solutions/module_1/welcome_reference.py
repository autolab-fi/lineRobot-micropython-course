from lineRobot import Robot

print("ARTEMIS LTV SYSTEM DIAGNOSTIC")
print("Initializing hardware...")
ltv_unit = Robot()
print("[TEST 1] Checking Main Drive...")
ltv_unit.move_forward_distance(15)
ltv_unit.move_backward_distance(15)
print("[TEST 2] Checking Steering Mechanism...")
ltv_unit.turn_left()
ltv_unit.turn_right()
print("DIAGNOSTIC COMPLETE. SYSTEMS NOMINAL.")
print("Welcome to the team!")
