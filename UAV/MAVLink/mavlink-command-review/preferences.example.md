# Reviewer preferences

Copy this file to `~/.config/mavlink-command-review/preferences.md` and edit it there.
The skill loads only that exact path, so a copy that keeps `.example` in its name is never read.

The `mavlink-command-review` skill loads it if it exists and skips it silently if it doesn't, so an empty or absent file is a valid setup: you get the skill's defaults.

It lives outside the skill directory on purpose, so sharing the skill can't carry your preferences to anyone else.

Delete any section you don't want to change.

## What you can set

**Output shape.** Tables or lists, which columns, what to group by, and whether to include the triage summary at all.

**Where the report goes.** Chat by default, or a path to write it to instead.

**Emphasis.** Checks to weight more heavily than the defaults — e.g. always double-checking a param's units column even when the description text looks unremarkable.

**Suppression.** Severities to drop. `minor` is the usual candidate.

**Orientation.** Questions to answer before reviewing, for a command you don't know well — e.g. "which flight stacks actually implement this command at all?"

**Tone.** Collegial, blunt, how much hedging.

## What you can't set

Preferences cannot override the sources of truth or their precedence, the read-only rule, or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

---

## Output

<!-- e.g. Drop the per-file summary table when there's only one changed file. -->

## Emphasis

<!-- e.g. Always flag a new Autopilot Support subsection for evidence, even if it reads plausibly. -->

## Suppression

<!-- e.g. Don't report `minor` findings. -->

## Orient before reviewing

<!-- e.g. For a PR adding a new command page, establish first:
     - Does a local ArduPilot and/or PX4 clone exist to check implementation claims against?
     - Is there a linked issue or discussion explaining why the command needed a dedicated page? -->

## Tone

<!-- e.g. Collegial, not apologetic. No hedging. Same standard for everyone. -->
