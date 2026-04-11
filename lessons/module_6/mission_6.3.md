---
index: 34
module: module_6
task: code_clinic
previous: hardware_safety_net
next: module_7_intro
---

# Mission 6.3 Code Clinic (Refactoring)

## Objective
Learn the principles of "Clean Code" by refactoring a messy, unreadable script into a modular, professional program.

## Introduction
In the previous missions, you learned how to find bugs and handle errors. But did you notice that finding a bug in a messy program is much harder than in a clean one?

In professional robotics, code is read by humans far more often than it is run by computers. If your code is a "spaghetti mess" of cryptic variables and repeated lines, you will eventually make a mistake that costs millions. Today, you will learn how to perform **Refactoring** — the process of improving your code's structure without changing what it does.

## Theory

### 1. The Power of Naming
In professional Python, we use specific styles to distinguish between different types of data at a glance:

* **Constants (ALL_CAPS):** These are the "Configuration Settings" of your robot. We place them at the very top. Even though Python technically allows you to change them, the CAPS tell other engineers: *"This is a fixed rule for the mission."*
* **Variables (snake_case):** These represent live, changing data (sensor values, current speed). 

### 2. Eliminating "Magic Numbers"
A **Magic Number** is a hardcoded value (like `500` or `240`) that appears in your code without explanation. 
* **The Problem:** If you need to change the sensitivity in several different places, you will eventually miss one.
* **The Solution:** Use Constants. By defining `SENSITIVITY = 240` at the top, you create a "Control Panel" for your robot. You tune the robot at the top; the logic stays at the bottom.

### 3. Modularity: The Manager and the Workers
If your `while True` loop is a long list of math and sensor reads, it's hard to follow. Instead, use **Functions** to delegate tasks. 
* **The Functions (Workers):** Each should do **one thing** (e.g., *only* calculate steering or *only* identify a color).
* **The Main Loop (Manager):** It should read like a "Table of Contents," calling the workers in the right order. This follows the **DRY (Don't Repeat Yourself)** principle.

## Assignment
You have been handed a "Spaghetti Script" that successfully follows the line and identifies minerals. Your task is to perform a full architectural upgrade.

**Requirements:**
1.  **Configuration Panel:** Create a section at the top for **Constants**. Move the `SENSITIVITY` (240), `LINE_THRESHOLD` (500), `BASE_SPEED`, and `KP` there.
2.  **Standardize Naming:** Replace all cryptic names (like `sa`, `rr`, `v`) with descriptive names.
3.  **Modularize:** Wrap the logic into three distinct functions:
    * `get_mineral_color()` — Must include your `try-except` safety net.
    * `calculate_steering()` — For the P-controller math.
    * `apply_movement()` — To handle the motor commands.
4.  **The Clean Loop:** Simplify the `while True` loop so it only manages the high-level mission logic.

## Conclusion
Excellent work, Architect! The robot still drives exactly the same, but the code is now "Space-Grade." By separating the **Settings** (Constants) from the **Logic** (Functions), you've made your rover significantly more stable and much easier to upgrade for future missions.