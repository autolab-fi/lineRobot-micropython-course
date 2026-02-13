# Verification Documentation Assignment Standard

## 1. Purpose and audience

This document is for **lesson authors and reviewers** who create, update, or approve lesson verification behavior.

Its purpose is to define a **single repository-wide standard** for how verification is implemented, documented, and reviewed across all lessons.

---

## 2. Verification flow (how verifications work)

### Lifecycle overview

1. A learner opens a lesson and writes/runs code in the editor.
2. The platform triggers a verification run for the current lesson task (typically when the learner presses **Verify**).
3. The platform loads the matching verification logic from `verifications/module_<n>.py`.
4. The selected task function (for example, `welcome(...)`) is called repeatedly with current runtime context.
5. Each call returns updated runtime state and a pass/fail payload.
6. Verification ends when either:
   - success criteria are met, or
   - timeout / rule violation causes failure.
7. The learner receives a final result (`success`, `description`, optional `score`) plus status text.

### Trigger, inputs, and outputs

- **Trigger:** Verification is initiated by platform runtime for the active lesson task.
- **Inputs expected by verification logic:**
  - robot state (position, heading, telemetry),
  - current frame/image,
  - test state dictionary (`td`) persisted between calls,
  - learner code text (when code-style/content checks are required).
- **Outputs expected from verification logic:**
  - current frame (possibly annotated),
  - updated `td`,
  - learner-facing status text,
  - final result object containing at minimum `success` and `description` (and usually `score`).

### Happy path example

- Lesson `module_1 / welcome` initializes a short timer in `td`.
- No rule violations occur.
- On timeout completion, verification returns:
  - `success: true`,
  - a completion description,
  - score `100`.

### Failure example

- Lesson expects movement distance in a limited time window.
- Robot moves too little or too far compared with the target.
- Verification returns:
  - `success: false`,
  - description explaining movement mismatch,
  - score `0`.

---

## 3. Where verification assets/config must be stored

Use only these canonical locations:

- **Verification definitions/config:** in module verification files under `verifications/` (for example constants/dictionaries like `target_points`).
- **Verification scripts/logic:** `verifications/module_<module_number>.py`.
- **Test media (images):** `verifications/images/`.
- **Lesson metadata:**
  - repository lesson index: `lessons-list.json`,
  - lesson manifest/front matter: at top of each `lessons/module_*/<lesson>.md`.

### Naming conventions

- Verification file: `module_<n>.py` (for example `module_1.py`).
- Task function name should match lesson task identifier (for example task `welcome` -> function `welcome`).
- Verification image names must be lowercase, hyphen-separated, and stable for lookup (for example `headlight-on.jpg`, `flag_finish.jpg`).

### Concrete directory example

```text
verifications/
  module_1.py
  images/
    headlight-on.jpg
lessons/
  module_1/
    mission_1.1.md
lessons-list.json
```

### Prohibited placement

Do **not** place verification scripts, verification configs, or verification media in ad-hoc folders outside approved paths (for example root-level random files, lesson folders, or temporary directories committed to git).

---

## 4. How to link images in docs and lesson data

### Allowed formats and path rules

- Allowed formats: `.png`, `.jpg`, `.jpeg`, `.gif`.
- Use **relative paths** in Markdown lesson/docs files.
- Use canonical repository URLs in `lessons-list.json` lesson URLs (as already done), not local absolute filesystem paths.

### Markdown examples

```md
![Mission Control interface](../../images/module-1/Interface1.png)
![Upload animation](../../images/module-1/upload.gif)
```

### Lesson manifest/list example

`lessons-list.json` lesson URL should point to the lesson markdown (not image files):

```json
{
  "str_id": "welcome",
  "url": "https://raw.githubusercontent.com/autolab-fi/lineRobot-micropython-course/main/lessons/module_1/mission_1.1.md"
}
```

### Alt text, captions, and file naming

- Alt text must describe purpose, not just type (`"Mission Control interface"`, not `"image1"`).
- If instructional context matters, add a one-line caption below the image.
- File names must support predictable lookup:
  - lowercase,
  - words separated by `-`,
  - include lesson/task cue where helpful (for example `module-1-upload.gif`).

---

## 5. Lesson list consistency rules (what must match)

For every lesson, the following must align between `lessons-list.json`, lesson markdown manifest, and verification code:

- **Module ID:** `lessons-list.json` module `str_id` must match lesson manifest `module`.
- **Lesson/verification ID:** `lessons-list.json` lesson `str_id` must match lesson manifest `task` and corresponding verification function name.
- **Title consistency:** `lessons-list.json` lesson `name` should semantically match markdown `#` heading.
- **Order consistency:** lesson `sn` and manifest `index` must follow intended sequence in module.
- **Verification binding:** lesson task id must exist in module verification definitions (`target_points`, rule maps, function implementation).

### Reviewer validation checklist

1. Open lesson entry in `lessons-list.json`.
2. Open referenced lesson markdown and verify front matter fields.
3. Open matching `verifications/module_<n>.py` and confirm function exists for lesson task id.
4. Confirm ordering fields (`sn`, `index`) are coherent within module.
5. Confirm URLs resolve to the same lesson file path intent.

### Mismatch example and fix

- **Mismatch:** lesson list uses `str_id: "line_sensor_intro"` but markdown front matter has `task: line_senosor_intro` (typo).
- **Fix:** rename one side so both use the same canonical id, then ensure verification function uses that same id.

---

## 6. Start coordinates definition

### Where start coordinates are declared

- Start coordinates for verification scenarios are declared in the module verification file (`verifications/module_<n>.py`) inside task configuration dictionaries (for example `target_points`).
- A coordinate set is interpreted per task according to verification logic.

### Format standard

- **Units:** centimeters unless explicitly documented otherwise by the verification function.
- **Axis order:** `(x, y)`.
- **Reference frame:** camera/image-aligned frame where origin is top-left, +x right, +y down.
- **Precision:** use numeric values with up to 1 decimal place unless higher precision is required by a specific task.

### Defaults and invalid behavior

- If start coordinates are missing for a task, verification must fail fast with a clear developer-facing message during review and a learner-safe message at runtime.
- If coordinates are invalid (wrong type/shape), verification must return `success: false` and a message indicating configuration error.

### Examples

- **Valid:** `"welcome": [(35.0, 50.0), (30.0, 0.0)]`
- **Invalid:** `"welcome": ["35,50"]` (wrong type and shape).

---

## 7. Additional critical topics to include

### Versioning / change policy

- Treat verification rule updates as versioned behavior changes.
- Record major rule intent changes in PR description and reference affected modules/tasks.
- Prefer additive changes; avoid silent behavioral drift.

### Backward compatibility

- Existing published lessons should keep previous pass criteria unless an explicit migration is approved.
- If behavior must change, document migration impact and update related lesson text/templates.

### Error messaging standards

- Failure messages must be:
  - specific (what failed),
  - actionable (what to change),
  - concise (one main reason per message).
- Avoid internal stack traces or ambiguous wording in learner-facing text.

### Localization considerations

- Learner-visible messages should be plain language and localization-ready.
- Avoid hard-coded idioms/slang and mixed-language fragments in the same message.

### Review/approval workflow and ownership

- Required approvers:
  1. lesson content owner (pedagogy/wording),
  2. verification owner (logic/criteria).
- No verification-rule PR merges without both approvals.

### Minimum QA before merge

- Static checks:
  - JSON validity (`lessons-list.json`, `course-info*.json`),
  - markdown/front matter sanity for changed lessons,
  - Python syntax for changed verification files.
- Manual checks:
  - run at least one happy-path verification,
  - run at least one known failure-path verification,
  - confirm learner-facing messages are understandable.

---

## 8. Deliverables and acceptance criteria

### Deliverables

- This assignment document.
- Linked examples/snippets (paths, markdown/image examples, config examples).
- Reviewer checklist (see Appendix A).

### Acceptance criteria

- Every required section exists and is complete.
- Examples are copy-paste usable.
- Paths/identifiers match this repository structure.
- A reviewer can validate a lesson end-to-end using only this document.

---

## 9. Cross-linking

- Add link in `README.md` under maintainer/developer documentation.
- Add link in contributor guide if/when `CONTRIBUTING.md` exists.

### Where to start (for new maintainers)

Start here:

1. Read this document.
2. Open `docs/task_test_documentation.md` for runtime return-contract details.
3. Validate one real lesson across:
   - `lessons-list.json`,
   - lesson markdown front matter,
   - `verifications/module_<n>.py`.

---

## 10. Suggested reviewer checklist (Appendix A)

Use this checklist in PR reviews:

- [ ] Can I locate verification files quickly?
- [ ] Can I confirm lesson list ↔ lesson metadata consistency?
- [ ] Can I verify image links without guessing paths?
- [ ] Can I validate start coordinates and error behavior?
- [ ] Do examples reflect real repo files?
