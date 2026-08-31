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
