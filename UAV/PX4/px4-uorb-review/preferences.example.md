# Reviewer preferences

Copy this file to `~/.config/px4-uorb-review/preferences.md` and edit it there.
The skill loads only that exact path, so a copy that keeps `.example` in its name is never read.

The `px4-uorb-review` skill loads it if it exists and skips it silently if it doesn't, so an empty or absent file is a valid setup: you get the skill's defaults.

It lives outside the skill directory on purpose, so sharing the skill can't carry your preferences to anyone else.

Delete any section you don't want to change.

## What you can set

**Output shape.** Tables or lists, which columns, what to group by, and whether to include the triage summary at all.

**Where the report goes.** Chat by default, or a path to write it to instead.

**Emphasis.** Checks to weight more heavily than the defaults — e.g. always double-checking a renamed field's new name against `community-conventions.md` even when it looks unremarkable.

**Suppression.** Severities to drop. `minor` and `hint` are the usual candidates — `hint` in particular is easy to suppress entirely if you don't want grammar suggestions on terse field comments at all.

**Orientation.** Questions to answer before reviewing, for a message you don't know well.

**Tone.** Collegial, blunt, how much hedging.

## What you can't set

Preferences cannot override the sources of truth or their precedence, the read-only rule, the new-or-changed gate (naming/comment findings only on fields this PR actually touches by name or comment), or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

---

## Output

<!-- e.g. Drop the Hints section entirely. Write the report to ~/reviews/PX4-Autopilot-<pr>.md as well as showing it in chat. -->

## Emphasis

<!-- e.g. Always flag a new enum whose prefix isn't referenced by any field's @enum tag, even if tool-check didn't already catch it. -->

## Suppression

<!-- e.g. Don't report `hint` or `minor` findings. -->

## Orient before reviewing

<!-- e.g. For a PR adding a new message, establish first:
     - What publishes it, and what subscribes to it?
     - Is this message versioned (msg/versioned/) or not, and does that match similar existing messages?
     Mine the PR description and diff for these answers before looking anywhere else. -->

## Tone

<!-- e.g. Collegial, not apologetic. No hedging. Same standard for everyone. -->
