---
index: 1
module: module_1
task: welcome
previous:
next: test_drive
---

# Mission 1.1 Welcome to Artemis Support Program

## Objective

Join the Artemis Support Program, familiarize yourself with the Mission Control Interface, and establish a connection with the Lunar Terrain Vehicle (LTV).

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction

Welcome, Recruit!

You have been selected for the **Artemis Support Program**. Your goal is to develop and test software for the next generation of lunar rovers. We are returning to the Moon, and this time, we are staying.

To assist the astronauts, we are deploying autonomous **Lunar Terrain Vehicles (LTV)**. Before we send them to the lunar South Pole, they must be tested in our simulation facility.


## The HAMK remote laboratory

Your code controls a real rover in HAMK’s robotics laboratory at **Riihimäki campus**. The lunar setting belongs to this HAMK course; it is separate from the Metropolia Mars laboratory.

![The HAMK lunar rover and its physical track](https://raw.githubusercontent.com/autolab-fi/lineRobot-micropython-course/main/images/course-info/hamk-image.jpg)

## Open activities through Moodle

Open each activity from your HAMK Moodle course. Remote Lab opens in a new window or tab and signs you in automatically through LTI. You do not need a separate registration, group membership or group key. Allow pop-ups for Moodle if your browser blocks the launch. If your session expires, return to Moodle and open the activity again.

## Mission Control Interface

![Current Remote Lab workspace opened from the HAMK Moodle course](https://raw.githubusercontent.com/autolab-fi/lineRobot-micropython-course/main/images/module-1/hamk-workspace-20261009.png)

* **Lesson:** your task objective and instructions.
* **Editor:** your Python program and activity files.
* **Output:** printed values, errors and verification feedback.
* **Run:** the browser simulator or physical-lab view.

The header **Reset** restores the workspace layout. The separate Editor reset restores starter code.

## Assignment

Run the supplied system diagnostic to check your connection to the rover. Read the code first: it initializes the robot, moves forward and backward, then checks steering.

1. Use **Test in simulator**, when available, to practise in the browser.
2. Use **Verify on robot** to submit the diagnostic to the physical HAMK rover. Wait if your submission is queued.
3. Review the recorded camera feedback, Output and verification result.
4. Successful physical verification returns **100/100** to this activity in Moodle. Unsuccessful verification returns **0**; review the feedback and retry. A simulator pass alone does not complete the graded Moodle activity.

![HAMK simulator view for practising robot movement](https://raw.githubusercontent.com/autolab-fi/lineRobot-micropython-course/main/images/module-1/hamk-simulator-20261009.png)

## Review a physical verification

![Camera frame from a physical HAMK robot verification on the lunar track](https://raw.githubusercontent.com/autolab-fi/lineRobot-micropython-course/main/images/module-1/hamk-physical-verification-20261009.png)

This frame comes from a successful physical **Simple Line Follower** verification on 9 October 2026. It shows the real HAMK rover and track, with on-screen markers from the recording. The technical side panel has been omitted. It is an example of recorded physical feedback, not a simulator view or a required result for this introductory diagnostic.

After your own submission, use the **Physical lab** view in **Run** to review the recording. Read **Output** for printed values, errors and verification feedback. A program can finish without passing every task requirement: check the verification result as well as the video. Return to Moodle and refresh the activity to see the returned grade and completion state. If a result appears delayed, check the submission status before submitting again.

## Proceed to the next mission

Return to Moodle and open **Test drive**. Always launch the next activity from Moodle so its grade is returned to the correct activity.

The course is continuously available and self-paced. Work through the six modules in order; the Sandbox is optional. The Remote Lab uses a **70% participation-certificate threshold**; check your progress and certificate status there.

Use the Moodle questions forum for course questions and Remote Lab **Helpdesk** for technical issues.

## Conclusion

System check complete!

You have successfully connected to the platform and verified the communication link. In the next mission, we will introduce you to the rover hardware and analyze how this code actually works.

Now proceed to next Mission!
