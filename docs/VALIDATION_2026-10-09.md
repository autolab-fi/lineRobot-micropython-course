# HAMK course audit — 2026-10-09

Continuation of the 2026-10-08 audit. The lunar/Artemis story remains. Tuning and Kick is excluded; scope is 34 tasks including Sandbox.

## Confirmed so far

| Task | Physical submission |
| --- | --- |
| welcome | 21992 |
| test_drive | 21993 |
| license_to_drive | 21997 |
| directional_movement | 21994 |
| python_variables_commands | 21995 |
| maneuvering | 21996 |
| sequential_navigation | 22031 |
| electric_motors | 22039 |
| differential_drive | 22034 |
| defining_functions | 22000 |
| for_loops | 22001 |
| encoder_theory | 22003 |
| intro_to_octoliner | 22040 |
| conditional_logic | 22041 |
| processing_sensor_data | 22042 |
| arrays_and_elif | 22043 |
| led_feedback | 22044 |
| python_lists | 22032 |
| telemetry | 22035 |

## Checks

- 45 verifier/replay tests passed.
- All 34 simulator task references passed, including renamed programs and negative empty/output-only cases (136 cases; Sandbox intentionally permits free programs).
- All 17 simulator UI scenarios passed.
- Sequential Navigation uses 20/15/20/15 cm, with the original 6 cm checkpoint tolerance, after the long route accumulated about 8 cm of drift.
- Lists uses [35, 30, 35] and a smaller safe route.
- Electric Motors timed reference uses left 30 / right 64 for 2.1 seconds on HAMK (22038 and 22039 passed). Simulator keeps its own 30/50, 2.5 s reference. The lesson explains tuning balance and time independently.

## Remaining physical checks

The live matrix and submission records are in `artifacts/hamk-course-audit-20261009/` in the workspace. Remaining tasks at this checkpoint:
- simple_line_follower
- color_sensor_basics
- color_classification
- concept_of_error
- upgraded_relay_controller
- proportional_control
- adaptive_speed
- art_of_debugging
- hardware_safety_net
- code_clinic
- navigation
- perimeter
- visual_telemetry
- adaptive_racing
- sandbox

## Battery and docking

User cutoff: below **23.0 V battery voltage**, stop the current test and return to dock. The audit guard checks before submission and polls during the run; the runner requests docking after a low-voltage cutoff and stops the series. Low-voltage stopping was tested offline without discharging the physical battery. Live battery telemetry has been confirmed during actual tests.

The new magnetic dock target is **(27.5, 63.0)**; direction (30, 0). Previous (27.5, 57.7) is obsolete. AutoCharge is temporarily suspended during controlled course submissions and must be restored on cleanup.

## Publication

Only previously promoted verified changes are in main (course 6ad7103, simulator 8cc6dd6). This audit remains on `validation/hamk-course-20261008`; pending tasks are not declared validated. Worker candidate checkers currently come from course revision 9091db1. Backend lesson/reference updates and public simulator deployment still require coordinated release after verification. No firmware or robot calibration changes were made during this audit.
