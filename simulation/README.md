# Browser simulation configuration

`manifest.json` contains course-owned simulation modes and checks. Physical
verification remains in `verifications/` and is executed only by the lab worker.
`course-info.json` publishes the generated browser configuration URL through
`simulationManifestUrl`; the course frontend can therefore discover simulation
support without embedding task IDs or checks in its own source.

`generated/task-metadata.json` is derived from verifier `target_points`. Generate
it from the sibling `browser-robot-sim` repository with `npm run course:extract`.
The coordinate conversion flips the physical arena Y axis and converts centimetres
to metres; direction vectors become simulator headings.

Reference solutions are not stored here or sent to students. They may be used by
trusted compatibility tests, identified only by task id and source hash.

The first module uses exact declarative command checks where the wording requires
a specific duration, distance, order, or turn angle. Signed values follow the
simulator convention: positive distance/angle means forward/left; negative means
backward/right. `non-literal-turn-angle` mirrors the physical verifier's code-style
rule and rejects a numeric literal passed directly to the precision-turn method.

Manual motor tasks additionally use source requirements to mirror the physical
verifiers' allowed APIs. Wheel-drive checks validate simulated duration and heading;
encoder checks use executed API events and stdout values, not source text alone.

The `electric_motors` finish target is derived from the physical verifier's
`(row=400, column=1000)` point using the 3000 x 2000 arena raster at 2 px/mm.
That maps to simulator `(x=0.50m, y=0.80m)` after flipping the camera Y axis.
Its current 18 cm simulation tolerance includes provisional motor-response error;
the physical verifier remains stricter at 10 cm.

`conditional_logic` is the first `simulation-and-lab` sensor task. Its browser
check requires a `while`/`if`/`break` structure, real Octoliner reads, forward
wheel motion, the assignment's success output, and a stop command issued while
the simulated sensor array is physically over the line. An immediate or
unconditional stop therefore does not pass.

`processing_sensor_data` accepts both the two-parameter `detect_line(distance,
threshold)` signature documented in the lesson and the three-parameter
`detect_line(sensitivity, distance, threshold)` signature used by the current
trusted reference solution. The reference uses threshold 900 while the physical
verifier accepts readings above 800; this discrepancy should be resolved in the
course content. The simulator currently emits 960 for line and 100 for floor so
that the published reference remains executable while preserving both thresholds.

The manifest currently enables 15 tasks. The September 2026 expansion adds
`sequential_navigation`, `for_loops`, `arrays_and_elif`, and `led_feedback`.
Their trusted references pass the browser checks. `defining_functions` remains
disabled: its lesson and physical verifier require a 180-degree manual turn, but
the trusted reference produces about 94 degrees in the calibrated simulator and
none of the 12 historically accepted submissions reaches the required 170–190
degree interval. Resolve the physical/simulator calibration and update the trusted
reference before enabling that task.
