# HAMK simulator completion and survey stability — 2026-10-29

Course implementation: `c078d4e`. Public simulator bundle: `41cfdcf`.

20 of 29 core activities now accept a graded simulator check OR physical verification.
Nine retain required physical verification: License to drive, Electric Motors,
Differential Drive, Encoder Theory, Introduction to Octoliner Sensor, Telemetry
Report, Color Sensor Basics, Color Classification and Adaptive Speed. Sandbox
remains optional and has zero Moodle grade weight. Plain simulator runs are practice;
completion requires the graded Check in simulator action or successful robot verification.

The policy follows Metropolia's simulator-eligible matching activities, with HAMK's
three debugging exercises also accepting simulator completion. Hardware-specific
motion, sensor and integrated-control exercises retain their lab requirement.

Lessons 3.4/3.5 now classify zero, one or multiple active zones, report each zone's
Boolean state, and blink once per detected scan. Both use five 5 cm scans and 0.5 s
settling. The physical grader parses semantic records across MQTT packet boundaries.
HAMK start (70, 50), facing right, is retained; Metropolia's (75, 50) start was not copied.
The physical-validation entries explicitly mark this changed contract as awaiting
HAMK revalidation; old submission IDs are retained only as historical evidence.

Validation: 84 Python verifier/policy regression tests passed in a disposable Python
container with OpenCV; all 120 browser cases passed across 30 tasks (reference,
renamed variable, empty program, output-only). Build and generated tutor freshness
checks passed. No physical robot motion was initiated for this release.

Production: course 9 synced with stable task IDs and no deleted user progress;
all 30 task/tutor execution modes agree. The public HAMK configuration matches the
tested bundle. Metropolia configuration is unchanged. The course-scoped HAMK worker
loaded the revised module_3 (SHA256
`4da9920af77a88c31d5ef22b6fe266072d7b85b6aaa1257538226d3ed25de43f`).
Download workflow `hamk-survey-verifiers-20261029` reported two staging import warnings
for bare module_2/module_3 names; independent import of all 11 deployed course_9
modules through the production course-scoped loader passed, including the new parser.
No worker restart or robot motion was needed.

Deployment workflow: https://github.com/autolab-fi/autolab-fe/actions/runs/40912030392
It published the simulator and a separate frontend preview, not the production frontend.

The source Moodle course 4 was updated and exported as
`hamk-mobile-robotics-simulator-20261029-nu.mbz`, without users: 36 total LTI activities,
30 active with new completion guidance. The existing learn.hamk.fi course was not
edited remotely. Its administrator can use the prepared completion-guidance script
to update descriptions without changing LTI bindings, grades or student work.
