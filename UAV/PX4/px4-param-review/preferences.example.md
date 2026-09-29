# Reviewer preferences

Copy this file to `~/.config/px4-param-review/preferences.md` and edit it there.
The skill loads only that exact path, so a copy that keeps `.example` in its name is never read.

The `px4-param-review` skill loads it if it exists and skips it silently if it doesn't, so an empty or absent file is a valid setup: you get the skill's defaults.

It lives outside the skill directory on purpose, so sharing the skill can't carry your preferences to anyone else.

Delete any section you don't want to change.

## What you can set

**Output shape.** Tables or lists, which columns, what to group by, whether to include the triage summary or the dropped-content note.

**Where the report goes.** Chat by default, or a path to write it to instead.

**Emphasis.** Checks to weight more heavily, such as always reading the code for every rewritten parameter, not only where a condition was merged.

**Suppression.** Severities to drop; `minor` is the usual candidate.

**Orientation.** Questions to answer before reviewing.

**Tone.** Collegial, blunt, how much hedging.

## What you can't set

Preferences cannot override the sources of truth or their precedence, the read-only rule, the classification of parameters, or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

---

## Output

<!-- e.g. Always write the report to ~/reviews/PX4-Autopilot-params-<pr>.md as well as showing it in chat. -->

## Emphasis

<!-- e.g. Flag every O3 label compression at `bug` rather than `style` until the batch rewrites settle. -->

## Suppression

<!-- e.g. Don't report `minor` findings. -->

## Orient before reviewing

<!-- e.g. For a split-off of #27758, establish first which parameters it takes from the tracking PR, and whether the tracking PR was updated to drop them. -->

## Tone

<!-- e.g. Collegial, not apologetic. No hedging. -->
