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
| simple_line_follower | 22046, 22053 |
| color_sensor_basics | 22057 |
| color_classification | 22058 |
| concept_of_error | 22059 |

## Checks

- 56 verifier/replay tests passed.
- All 34 simulator task references passed, including renamed programs and negative empty/output-only cases (136 cases; Sandbox intentionally permits free programs).
- All 17 simulator UI scenarios passed earlier in this audit; the targeted line/waypoint/telemetry/RGB UI check also passed with the final color reference.
- Sequential Navigation uses 20/15/20/15 cm, with the original 6 cm checkpoint tolerance, after the long route accumulated about 8 cm of drift.
- Lists uses [35, 30, 35] and a smaller safe route.
- Electric Motors timed reference uses left 30 / right 64 for 2.1 seconds on HAMK (22038 and 22039 passed). Simulator keeps its own 30/50, 2.5 s reference. The lesson explains tuning balance and time independently.

## Remaining physical checks

The live matrix and submission records are in `artifacts/hamk-course-audit-20261009/` in the workspace. Remaining tasks at this checkpoint:
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

User cutoff: below **23.0 V battery voltage**, stop the current test and return to dock. The audit guard requires at least **23.3 V** before a new submission and polls during the run; the runner requests docking after a low-voltage cutoff and stops the series. The firmware may defer ADC sampling until student Python returns, so cached readings during long-running code are labelled explicitly and are not a guarantee of continuous fresh voltage monitoring. Low-voltage stopping was tested offline without discharging the physical battery. Live battery telemetry has been confirmed during actual tests.

The new magnetic dock target is **(27.5, 63.0)**; direction (30, 0). Previous (27.5, 57.7) is obsolete. AutoCharge is temporarily suspended during controlled course submissions and must be restored on cleanup.

## Publication

Only previously promoted verified changes are in main (course 6ad7103, simulator 8cc6dd6). This audit remains on `validation/hamk-course-20261008`; pending tasks are not declared validated. Worker candidate checkers currently come from course revision 7d895f8; subsequent Concept/controller/race changes are not deployed or physically validated. Backend lesson/reference updates and public simulator deployment still require coordinated release after verification. No firmware or robot calibration changes were made during this audit.

## Latest candidate changes (physical tests pending)

- Concept start moved to (104, 76), facing up, away from the left frame; physical submission 22059 passed, with first-attempt reset and about 29 cm displacement.
- Adaptive Speed and Adaptive Racing use maximum speed 40, braking 20, gain 25, sensitivity 245 and raw line-loss threshold 700.
- Adaptive Racing requires all three ordered route checkpoints; five replay tests cover full/partial/skipped routes, invalid code and immutable final results.
- Simulator Relay, P, Adaptive Speed and Racing now check the full three-checkpoint route. All 34 canonical and renamed references passed alongside empty/output-only cases (136 cases).
- Color references physically demonstrated Green → Floor → Red using six readings, five 13 cm steps at 40%, and 1.1 s settling. Lessons, starter code and tutor guidance agree.
- Latest physical total: **23/34**, with **11 pending**. These candidate changes stay on the validation branch until physical verification.

## Controller experiments after 9e9b481

- Concept 22059 passed on the new start (104, 76), with ten error readings and about 29 cm displacement. Reset succeeded on its first attempt.
- Relay 22060 stopped on line loss at the lower right bend, tag approximately (99.7, 79.7), heading 107.6 degrees; 1/3 checkpoints. The canonical 5/25 turning command is not yet validated for a full HAMK lap.
- P-controller 22061 passed the right bend and lower straight, then stopped on line loss at the lower left bend, approximately (22.6, 75), heading -116.6 degrees; 2/3 checkpoints. Its current base_speed=30, kp=20 reference is not yet validated for a full HAMK lap.
- Both controller resets succeeded on their first attempt. No boundary stop or reset retry occurred in these three submissions.
- Proposed experimental values (not canonical yet): Relay -5/20 turns and 15/15 straight; P-controller base speed 20 and gain 30. This reduces forward motion on a bend and permits a tighter turn. Physical and simulator comparison are still required.
- Battery reached about 23.29 V after P-controller; further launches paused for docking before the 23.0 V user cutoff.
