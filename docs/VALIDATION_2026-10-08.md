# HAMK course validation — 2026-10-08 (in progress)

Scope: preserve the lunar / Artemis narrative and transfer applicable Metropolia technical fixes. Remove Tuning and Kick from the course while retaining student submission history. Target: 34 tasks including Sandbox.

The candidate branch is `validation/hamk-course-20261008`. Course main, backend lesson publication, and the production simulator have not yet been updated. Hardware currently uses candidate grader revision `19cbc83`; subsequent grader changes listed below await deployment and physical tests. Firmware and calibration are unchanged during this audit.

## Confirmed checks

- Simulator curriculum: all 34 tasks, 136 reference/renamed/empty/output-only cases passed after the compact Python Lists route update.
- Simulator unit tests: 56 passed.
- Physical grader unit/replay tests: 45 passed, including failures remaining failures on later frames.
- Nine task references passed ordinary hardware submissions, including completed processing and video availability. The reference hashes and submission IDs are recorded in `tutor/task-notes.json`.

## Hardware matrix

| Task | State | Submission |
| --- | --- | --- |
| welcome | passed | 21992 |
| test_drive | passed | 21993 |
| license_to_drive | passed | 21997 |
| directional_movement | passed | 21994 |
| python_variables_commands | passed | 21995 |
| maneuvering | passed | 21996 |
| sequential_navigation | needs-fix | 21998 |
| electric_motors | pending | — |
| differential_drive | pending | — |
| defining_functions | passed | 22000 |
| for_loops | passed | 22001 |
| encoder_theory | passed | 22003 |
| intro_to_octoliner | pending | — |
| conditional_logic | pending | — |
| processing_sensor_data | pending | — |
| arrays_and_elif | pending | — |
| led_feedback | pending | — |
| simple_line_follower | pending | — |
| python_lists | needs-fix | 22005 |
| telemetry | pending | — |
| color_sensor_basics | pending | — |
| color_classification | pending | — |
| concept_of_error | pending | — |
| upgraded_relay_controller | pending | — |
| proportional_control | pending | — |
| adaptive_speed | pending | — |
| art_of_debugging | pending | — |
| hardware_safety_net | pending | — |
| code_clinic | pending | — |
| navigation | pending | — |
| perimeter | pending | — |
| visual_telemetry | pending | — |
| adaptive_racing | pending | — |
| sandbox | pending | — |

## Findings and pending retests

- Sequential Navigation: original attempt 21998 missed the last two camera checkpoints. Fixed checkpoint radius is now 6 cm (rather than increasing tolerance during a run); the new grader still needs hardware confirmation.
- Defining Functions: original 0.7 s motor pulse overshot; 0.63 s passed hardware submission 22000. Simulator reference retains 0.7 s. Lesson and tutor explain independent timing adjustment.
- Encoder Theory: the old 0.8 s pulse overshot and did not print both counters. A 0.6 s pulse with 0.3 s settling and both counters passed 22003 (left 329 degrees, calculated distance 18.43 cm). Simulator uses its independently verified 0.8 s pulse.
- Python Lists: original [55, 60, 70] route passed only one of three checkpoints in 22005. Candidate uses [35, 30, 35], start (65,45), and checkpoints (100,45), (100,75), (65,75). The lesson, reference, grader, simulator and tutor agree. Simulator passes; hardware retest pending.
- Simple Line Follower: candidate uses three sensor zones and a short straight route, start (104,40) heading down, checkpoints (104,52) and (103,64). Simulator passes; physical sensor alignment and reference run are pending.
- Final verdict persistence fixed in Concept/Relay/P/Adaptive, debugging tasks, Lists/Telemetry/Color tasks and Perimeter/Adaptive Racing. Later frames must not overwrite a completed failure with default success.
- Sensor sensitivity, line-start alignment, both Concept sweeps, color thresholds and remaining debugging/final tasks need physical verification. Adaptive Racing currently has a weaker physical distance criterion than its intended route; align that before publication.

## Next steps

1. Restore sustained dock charging and recharge before more driving.
2. Deploy the latest candidate graders, retest Sequential Navigation and Python Lists.
3. Measure stationary Octoliner values at the proposed Simple, controller and Concept starts; test all remaining references with a camera boundary guard.
4. Correct lesson instructions, starters, references, graders, simulator and AI tutor together wherever physical tests require adjustments.
5. Repeat relevant positive and negative cases. Publish main, refresh course 9, verify Tuning and Kick is inactive with history preserved, and publish the matching simulator bundle.

Operational scripts, logs and submission evidence are in `/root/git-images/artifacts/hamk-course-audit-20261008/`. Charging and maintenance state must be checked there before resuming physical work.
