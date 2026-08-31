# Browser simulation configuration

`manifest.json` contains course-owned simulation modes and checks. Physical
verification remains in `verifications/` and is executed only by the lab worker.

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
