# Reviewer preferences

Copy this file to `~/.config/px4-board-doc-review/preferences.md` and edit it there.
The skill loads only that exact path, so a copy that keeps `.example` in its name is never read.

The `px4-board-doc-review` skill loads it if it exists and skips it silently if it doesn't, so an empty or absent file is a valid setup: you get the skill's defaults.

It lives outside the skill directory on purpose, so sharing the skill can't carry your preferences to anyone else.

Delete any section you don't want to change.

## What you can set

**Output shape.** Tables or lists, which columns, whether to include the submission checklist.

**Where the report goes.** Chat by default, or a path to write it to instead.

**Emphasis.** Checks to weight more heavily, such as always comparing the serial mapping table with every reference-design sibling rather than two.

**Suppression.** Severities to drop.

**Tone.** Collegial, blunt, how much hedging.

## What you can't set

Preferences cannot override the sources of truth or their precedence, the read-only rule, or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

---

## Output

<!-- e.g. Write the report to ~/reviews/PX4-Autopilot-<pr>-board.md as well as showing it in chat. -->

## Emphasis

<!-- e.g. Always compare against the px4/<design> reference board's pages, even when three closer siblings exist. -->

## Suppression

<!-- e.g. Don't report `minor` findings. -->

## Tone

<!-- e.g. Collegial, not apologetic. Manufacturers are often first-time contributors: explain why, briefly. -->
