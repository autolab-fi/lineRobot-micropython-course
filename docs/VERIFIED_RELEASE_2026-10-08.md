# HAMK verified subset — 2026-10-08

This main-branch update intentionally promotes only the hardware-confirmed task fixes and the requested removal of Tuning and Kick. Remaining candidates are preserved on `validation/hamk-course-20261008` (course tip `e9bc0b2`, simulator tip `03cbb1b`). It does not claim that every HAMK task has been physically validated.

## Included

- Defining Functions: validate a defined and called function using manual motor control, handle heading wraparound, require a stable 180-degree turn, and retain the final verdict. Hardware reference uses a 0.63 s pulse; simulator reference retains 0.7 s. Lesson and AI guidance explain separate tuning.
- Encoder Theory: collect split/merged telemetry, require both encoder values, validate the distance formula with the HAMK lesson radius 3.21 cm and actual movement. Hardware reference uses a 0.6 s pulse and 0.3 s settling; simulator reference uses its verified 0.8 s pulse. The lesson explicitly requests both counters.
- Remove Tuning and Kick from lessons, next/previous links, grader lookup and function, and simulator manifest. Adjust the Adaptive Speed conclusion to remove the obsolete kick instructions.
- Canonical references and AI context: the nine hardware-passed references are selected by their exact submission hashes. Other active task references are preserved from the pre-audit tutor snapshot, with pending physical-validation status; their candidate modifications are excluded. The generated context uses the selected main-branch lessons and graders, not the unverified candidate versions.
- Simulation metadata is regenerated, also reflecting the valid Hardware Safety direction already present in baseline commit `ca88ac2`.

## Hardware evidence

| Task | Successful submission |
| --- | --- |
| welcome | 21992 |
| test_drive | 21993 |
| license_to_drive | 21997 |
| directional_movement | 21994 |
| python_variables_commands | 21995 |
| maneuvering | 21996 |
| defining_functions | 22000 |
| for_loops | 22001 |
| encoder_theory | 22003 |

All nine completed with successful verification and a video. Exact reference hashes are stored in `tutor/task-notes.json`. These tests were performed before the charging pause; this promotion did not move the robot.

## Validation of the selected main version

- Six grader regression tests passed (positive, negative, split telemetry, stable heading and no-movement cases).
- Simulator curriculum: 34 tasks / 136 reference, renamed, empty and output-only cases passed.
- Simulator unit tests: 56 passed.
- Generated AI manifest freshness check passed.
- AST comparison confirms all retained grader functions except Defining Functions and Encoder Theory are unchanged from baseline.
- All retained student templates and simulator task contracts are unchanged. The generated simulator bundle differs from the published baseline only by the removed Kick task.

## Excluded until further physical tests

Sequential Navigation tolerance/geometry, compact Python Lists route, redesigned Simple Line Follower, Octoliner parsing changes, Electric Motors/Differential Drive checker changes, Concept/controller changes, debugging/final-verdict changes in other modules, Navigation geometry, and all other candidate changes remain on the validation branches. Two failed physical tasks need retesting; 23 tasks have not been physically tested in this audit.

## Deployment boundary

This operation updates Git main only. It does not invoke the backend course update, download graders to the worker, or deploy the public simulator. The worker was left on published grader revision `ca88ac2` at the pause. During a later coordinated rollout, refresh course 9 and its AI profiles, soft-invalidate removed task 240 without deleting student history, download the main graders, and publish the matching simulator bundle.

HAMK automatic docking was restored before this promotion. No manual movement, firmware change, calibration change or automatic-docking change is part of this release. Fresh charging state must be checked before resuming physical validation.
