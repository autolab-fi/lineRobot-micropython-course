# HAMK course verification — 2026-10-09

The current continuous Moodle course has **29 core tasks plus Sandbox**. All **30 active tasks** have a successful physical submission with the current canonical reference hash, finished status and recorded video. HAMK's lunar/Artemis story and the independently updated Moodle wording from main a1638fa are preserved. Tuning and Kick remains excluded. The four former final-block tasks remain excluded from the active lesson list; their additional audit results are recorded separately.

## Active physical results

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
| simple_line_follower | 22053 |
| python_lists | 22032 |
| telemetry | 22035 |
| color_sensor_basics | 22057 |
| color_classification | 22058 |
| concept_of_error | 22059 |
| upgraded_relay_controller | 22070 |
| proportional_control | 22067 |
| adaptive_speed | 22080 |
| art_of_debugging | 22085 |
| hardware_safety_net | 22082 |
| code_clinic | 22086 |
| sandbox | 22078 |

Art of Debugging passed twice from the new upper-straight start: **22084 and 22085**. Hardware Safety Net **22082** and Code Clinic **22086** used the deployed stricter module 6 checker, rather than only replaying older event recordings.

## Archived final-block results

These are not active Moodle tasks and are not reintroduced by this release.

| Task | Physical submission |
| --- | --- |
| navigation | 22079 |
| perimeter | 22075 |
| visual_telemetry | 22076 |
| adaptive_racing | 22081 |

## Simulator and regression evidence

- Current active HAMK course: **30 tasks / 120 scenarios passed** (reference, renamed robot variable, empty and output-only). Sandbox intentionally permits free programs.
- Before integrating the current Moodle activity list, the original 34-task audit passed all **136 scenarios**, including archived final-block references.
- **81 local verifier/replay tests passed**, including recorded physical positions from the two new Debugging runs, strict module 6 completion requirements, malformed routes, missing camera data, late verdict immutability and the P-controller deadline regression.
- Two bundle-selection tests passed: excluded tasks stay excluded, physical-only tasks need no simulator entry, and missing active simulator tasks fail the build.
- All 17 HAMK UI scenarios passed earlier in the audit; targeted line/waypoint/telemetry/RGB checks passed after updating those references.
- Metropolia isolation checks passed **77 verifier tests**, **35 tasks / 140 simulator scenarios**, and **3 UI tests** (assets/3D, Python execution, Reset cancellation/fresh globals). Its two generated simulator configurations remained byte-identical to main. One UI assertion was updated to the already-existing title “Python Programming for Mobile Robotics @ Metropolia”; no Metropolia application behavior was changed.

## Corrections and why they were needed

- Sequential Navigation uses 20/15/20/15 cm with the original 6 cm tolerance; the longer route accumulated excessive physical turn drift. Lists uses [35, 30, 35] on its compact safe route.
- Electric Motors uses 30/64 for 2.1 seconds on HAMK; its simulator reference uses 30/50 for 2.5 seconds. The exercise explicitly teaches independent balance/time tuning. Encoder and function pulse references likewise retain separate measured physical/simulator values.
- Introductory line following uses a short straight route and three sensor groups. Concept starts at (104, 76), facing up, away from the left frame.
- Relay passed a complete route at 25/25 straight and 0/25 or 25/0 turns. P passed at base 20, gain 25. Both use sensitivity 245, loss threshold 700 and five consecutive weak readings before stopping. Reverse-wheel Relay turns and gain-30 P candidates failed and were not selected.
- P's checker deadline is 90 seconds; a second hard-coded 60-second deadline was found and corrected. The firmware's existing 70-second student-code watchdog is unchanged. The successful P run reached its required checkpoints before that watchdog stopped execution.
- Adaptive Speed and archived Racing passed at max speed 40, braking 20, gain 25, sensitivity 245 and the same five-reading filter. The Racing checker cannot let the filter's short sleep conceal an unfixed five-second control-loop sleep.
- Art of Debugging passed once from (60, 92), but repeat 22083 lost the line before its first checkpoint near (80, 96). The selected start is **(50, 30), east**, with checkpoints **(80, 30) then (105, 60)**. Both repeats 22084/22085 passed. The six intended starter bugs are preserved. Simulator start is (0.50, 0.84), placing the sensor on the upper line.
- Code Clinic keeps physical start (50, 30), east, and all three ordered checkpoints (80, 30), (105, 60), (60, 90). Its simulator start is corrected to (0.50, 0.84). A real Red/Green/Blue mineral message is required; “No minerals found” cannot pass as a detection.
- Partial Debugging and Clinic routes no longer count as success. Safety Net requires all ten unique scans, ten analyses, four Unknown cases and completion. Combined MQTT packets are read in order; duplicate sector messages cannot inflate scan counts.
- Color exercises physically demonstrated Green → Floor → Red with six readings, five 13 cm steps at 40%, and 1.1 seconds of sensor settling. Starters, lessons, reference solutions and tutor guidance agree.
- Archived Navigation now tolerates 12 cm of accumulated open-loop drift while separately checking its required command sequence; 22079 passed with about 8 cm final error. Missing camera data cannot pass at timeout. Archived Perimeter additionally checks four 30 cm/right-90 legs, so arbitrary travelled distance cannot count as a square.

## Battery, docking and deployment

User cutoff is **23.0 V**. New submissions require a **23.3 V** reserve. The guard polls battery telemetry and sends direct Robot Stop and submission cancellation on a low-voltage event; the runner then docks and pauses the series. Firmware can defer fresh ADC telemetry while student Python runs: cached readings are explicitly labelled and do not guarantee continuous fresh voltage monitoring. No firmware, calibration, motor-library or Wi-Fi changes were made in this audit.

Magnetic dock target is **(27.5, 63.0)**, direction (30, 0); the former y=57.7 target is obsolete. Several controlled docking cycles confirmed stable contact, including a three-minute observation. Before the final return, the latest fresh post-run battery was about 23.39 V. Final docking confirmation and publication revisions are appended below.

Only HAMK course **9**, device **13**, task queue `submit-python-line-HAMK` received candidate verifiers (latest physical module 6 runs: a3da6b1). Metropolia course 11/device 14 was not deployed to or moved. Shared simulator runtime and robot models were not changed; the bundle builder now respects each course's active lesson list and preserves lab-only tasks.

The current simulator bundle has 30 HAMK tasks, 35 full Metropolia tasks and 11 simulator-enabled tasks in the separate Metropolia 2 ECTS package. Active Moodle composition is taken from the course lesson list, rather than resurrecting archived manifest entries. Publication must keep the HAMK lessons, canonical references, tutor profiles, checker revision and simulator bundle synchronized.

Final docking update: two returns at the saved target detected contact but failed stable charging (battery about 23.38 V, input 22.1–22.8 V). Motion was stopped after each attempt. A bounded third trial uses temporary y=62.3, 7 mm toward the earlier successful contact position; the saved backend target is unchanged.
