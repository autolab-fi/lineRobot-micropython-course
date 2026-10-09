# HAMK course audit — 2026-10-09

Continuation of the 2026-10-08 audit. The lunar/Artemis story remains. Tuning and Kick is excluded; scope is 34 tasks including Sandbox.

## Latest physical results

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
| art_of_debugging | 22071 (old route; new start pending) |
| hardware_safety_net | 22072 |
| code_clinic | 22073 |
| navigation | 22079 |
| perimeter | 22075 |
| visual_telemetry | 22076 |
| adaptive_racing | 22081 |
| sandbox | 22078 |

## Checks

- 81 verifier/replay tests passed for the latest candidate, including actual module 6 event recordings and wrong-route negative cases.
- All 34 simulator task references passed, including renamed programs and negative empty/output-only cases (136 cases; Sandbox intentionally permits free programs).
- All 17 simulator UI scenarios passed earlier in this audit; the targeted line/waypoint/telemetry/RGB UI check also passed with the final color reference.
- Sequential Navigation uses 20/15/20/15 cm, with the original 6 cm checkpoint tolerance, after the long route accumulated about 8 cm of drift.
- Lists uses [35, 30, 35] and a smaller safe route.
- Electric Motors timed reference uses left 30 / right 64 for 2.1 seconds on HAMK (22038 and 22039 passed). Simulator keeps its own 30/50, 2.5 s reference. The lesson explains tuning balance and time independently.

## Active course coverage

At the preceding checkpoint all **30 current Moodle activities** (29 core tasks plus Sandbox) had successful physical references. The subsequent repeat below exposed an unstable Art of Debugging start; that updated candidate is pending. The four removed final-block tasks (Navigation, Perimeter, Visual Telemetry and Adaptive Racing) also passed, bringing the archived audit scope to **34/34**. Each success includes a finished submission and video. The candidate is being reconciled with current main a1638fa; the removed final block must stay excluded.

## Battery and docking

User cutoff: below **23.0 V battery voltage**, stop the current test and return to dock. The audit guard requires at least **23.3 V** before a new submission and polls during the run; the runner requests docking after a low-voltage cutoff and stops the series. The firmware may defer ADC sampling until student Python returns, so cached readings during long-running code are labelled explicitly and are not a guarantee of continuous fresh voltage monitoring. Low-voltage stopping was tested offline without discharging the physical battery. Live battery telemetry has been confirmed during actual tests.

The new magnetic dock target is **(27.5, 63.0)**; direction (30, 0). Previous (27.5, 57.7) is obsolete. AutoCharge is temporarily suspended during controlled course submissions and must be restored on cleanup.

## Publication

Only previously promoted verified changes are in main (course 6ad7103, simulator 8cc6dd6). This audit remains on `validation/hamk-course-20261008`; pending tasks are not declared validated. Worker candidate checkers at the start of this checkpoint came from 5fed9de. The stricter module 6 and module 11 candidates below still require deployment. Backend lesson/reference updates and public simulator deployment still require coordinated release after verification. No firmware or robot calibration changes were made during this audit.

## Historical checkpoints and experiments

The entries below record earlier candidate states and failures; the latest successful submissions are listed above.

## Latest candidate changes (physical tests pending)

- Concept start moved to (104, 76), facing up, away from the left frame; physical submission 22059 passed, with first-attempt reset and about 29 cm displacement.
- Adaptive Speed and Adaptive Racing use maximum speed 40, braking 20, gain 25, sensitivity 245 and raw line-loss threshold 700.
- Adaptive Racing requires all three ordered route checkpoints; five replay tests cover full/partial/skipped routes, invalid code and immutable final results.
- Simulator Relay, P, Adaptive Speed and Racing now check the full three-checkpoint route. All 34 canonical and renamed references passed alongside empty/output-only cases (136 cases).
- Color references physically demonstrated Green → Floor → Red using six readings, five 13 cm steps at 40%, and 1.1 s settling. Lessons, starter code and tutor guidance agree.
- Latest physical total: **26/34**, with **8 pending**. These candidate changes stay on the validation branch until physical verification.

## Controller experiments after 9e9b481

- Concept 22059 passed on the new start (104, 76), with ten error readings and about 29 cm displacement. Reset succeeded on its first attempt.
- Relay 22060 stopped on line loss at the lower right bend, tag approximately (99.7, 79.7), heading 107.6 degrees; 1/3 checkpoints. The canonical 5/25 turning command is not yet validated for a full HAMK lap.
- P-controller 22061 passed the right bend and lower straight, then stopped on line loss at the lower left bend, approximately (22.6, 75), heading -116.6 degrees; 2/3 checkpoints. Its current base_speed=30, kp=20 reference is not yet validated for a full HAMK lap.
- Both controller resets succeeded on their first attempt. No boundary stop or reset retry occurred in these three submissions.
- Proposed experimental values (not canonical yet): Relay -5/20 turns and 15/15 straight; P-controller base speed 20 and gain 30. This reduces forward motion on a bend and permits a tighter turn. Physical and simulator comparison are still required.
- Battery reached about 23.29 V after P-controller; further launches paused for docking before the 23.0 V user cutoff.

## Follow-up measurements

- Relay experiment 22062 (15/15 straight, -5/20 turns, immediate threshold 700) stopped on a straight with samples [44, 54, 213, 512, 48, 46, 43, 46]. A single below-threshold sample does not prove all channels lost the line. A five-reading filter is now provided in the Relay and P candidate starter code.
- P experiment 22063 (base 20, gain 30, filter five) navigated both lower bends and the left side, but reached the third-checkpoint area after the 60-second verdict was already frozen. P's deadline was raised to 90 seconds; late checkpoints after the deadline still cannot change a verdict (two regression tests).
- Repeat 22064 at the same P settings lost the line on the lower left section after 2/3 checkpoints. Samples [44, 53, 44, 45, 48, 46, 43, 46] show a genuine loss; this reference remains pending and is not a reliable full-lap solution yet.
- Adaptive Speed 22065 (max 40, braking 20, gain 25, sensitivity 245, immediate loss threshold 700) passed all 3/3 checkpoints and followed approximately two laps during the 60-second run. Fresh post-run battery was about 23.33 V.
- Lessons and starters had stale sensitivity 240 / threshold 500 advice. Relay, P and Adaptive starter setup now agrees with the candidate references (245 / 700); obsolete Kick wording and P's removed-Tuning transition were corrected.
- All 58 local tests and all 136 simulator audit cases passed after the timing/filter candidate update. Physical validation remains separate from simulator validation.

- P experiment 22066 (base 20, gain 25, five-reading filter) followed both lower bends and the left side without line loss, but again received a 2/3 verdict at 60 seconds. Inspection found a duplicate hard-coded `end_time = time.time() + 60` despite the updated `TASK_DURATION = 90`. The deadline now uses the constant. The timing regression now includes a frame at 60.1 seconds before completing the third checkpoint at 70 seconds, so it detects premature verdict freezing. No worker restart or firmware change was needed.

- P 22067 passed 3/3 with base 20, gain 25, five-reading filter and the corrected 90-second deadline. The firmware's existing user-code watchdog is 70 seconds; it interrupted the loop after the third checkpoint. The checker continued to its deadline and preserved the completed route. This firmware limit was inspected, not changed.
- Relay 22068 (15/15 straight, -5/20 turns, five-reading filter) lost the line almost immediately on the first straight; reverse-wheel steering is too aggressive with this setup and remains unvalidated.

- Relay 22069 (20/20 straight, 0/20 turns, five-reading filter) followed the line around to approximately (43, 32), but the existing 70-second firmware stop occurred before the third checkpoint. The route was stable but too slow.
- Relay 22070 (25/25 straight, 0/25 turns, five-reading filter) passed all three checkpoints before the firmware stop. The canonical reference, lesson motor examples and tutor parameters now match this tested source.
- Pending Debugging and Clinic candidates reuse measured sensitivity 245 / threshold 700 / base 20 / gain 25 and the five-reading filter. Their simulator routes now use the same ordered checkpoints as the physical grader. Debugging's start is (60, 92), east, on the lower straight; its six intended bugs remain in the starter. Clinic keeps start (50, 30), east. Physical tests still required.

## Debugging and final-route checkpoint

- Art of Debugging 22071, Hardware Safety Net 22072 and Code Clinic 22073 passed. Their actual physical MQTT/position events are checked into test fixtures and pass the stricter checker requiring full completion. Partial routes/scans no longer pass. Combined MQTT deliveries are parsed in order and scan numbers prevent double counting; Code Clinic requires a real Red/Green/Blue detection rather than arbitrary text containing “mineral”.
- Perimeter 22075, Visual Telemetry 22076 and Sandbox 22078 passed. Perimeter additionally validates four 30 cm/right-90 legs, so total distance alone cannot count as a square.
- Navigation 22074 missed the third checkpoint after accumulated open-loop turn drift. Approximate observed displacement from expected points was 7–12 cm. Candidate tolerance is 12 cm instead of 4, together with static validation of the required distances and turn sequence. Missing camera position cannot pass at timeout, and final verdicts cannot flip on later frames. This candidate needs a physical run.
- Racing 22077 stopped after only about 10 cm on a weak sensor sample. Adaptive and Racing references/starters now preserve the same five-reading filter as P/Relay; both modified references need a fresh physical run. A regression check prevents the supplied short filter delay from concealing the unfixed five-second Racing delay.
- Clinic simulator start moved from (0.50, 0.79) to (0.50, 0.84), placing its sensor on the line. The full simulator regression after that correction passed 136 cases; the second run including the latest Adaptive/Racing filters also passed all 136 cases.
- Before this checkpoint, HAMK returned to its magnetic dock. Three stable charge samples confirmed contact, last battery 23.72 V and input 24.06 V. No new physical launch occurs below the 23.3 V audit reserve; the user cutoff remains 23.0 V.

## Final candidate confirmation

- Navigation 22079 passed all four ordered checkpoints with the candidate 12 cm tolerance and correct-command check. Final camera error was about 8 cm. It remains outside the current Moodle activity list.
- Adaptive Speed 22080 and Racing 22081 both passed 3/3 checkpoints with the five-reading filter. The exact reference hashes are stored in tutor task notes. Racing remains outside the current Moodle list.
- Candidate checker a90c855 was downloaded to HAMK and all 11 course modules imported successfully. The downloader's legacy bare-name import warnings for modules 1/4 did not prevent their qualified imports; final import checks passed.
- A further physical repeat of all three module 6 tasks with the stricter checker is in progress; recorded-event replays already pass.

## Repeat-test correction before release

Hardware Safety Net 22082 passed with the deployed strict parser: 10/10 scans, 4/4 Unknown events and completion. Art of Debugging repeat 22083 failed on line loss near (80, 96), before its first checkpoint. Its earlier success therefore does not establish a stable lower-straight start. Candidate start is now (50, 30), east, with ordered checkpoints (80, 30), (105, 60); simulator start is (0.50, 0.84) with matching order. The six debugging bugs and controller settings are unchanged. This changed task is pending two physical confirmations, and publication is postponed.

Isolation check: no Metropolia verifier, firmware or calibration was changed. Both generated Metropolia simulation configurations are byte-identical to their committed versions after rebuilding. The shared simulator's Metropolia curriculum regression passed all 35 tasks / 140 cases with the active-task bundle selection change.
