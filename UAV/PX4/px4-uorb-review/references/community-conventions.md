# Community conventions: @MaEtUgR on uORB naming and comments

@MaEtUgR is a PX4 maintainer who reviews most PRs touching `.msg` files.
These are conventions he's argued for repeatedly across real PR review threads — not the written standard (`style-guide.md`), but the maintainer-level norms a PR is likely to get pushback on if it ignores them.

Apply these at `style` or `minor` severity, never `bug` — they supplement the written standard, they don't override it, and `style-guide.md` wins if the two ever conflict.
Every check below cites the source thread; when you apply one, cite it back in the finding the same way `style-guide.md` rules are cited.

Compiled from a review of his PR comment history (2026-09-03); if a finding doesn't clearly match one of these patterns, don't stretch a bullet to cover it — fall back to `style-guide.md` and general clarity instead of inventing a rule in his name.

## Naming

Only applies to a field/constant this PR introduces or renames/retypes — see "New-or-changed determination" in `shared.md`. Never raise a naming finding against a field this PR leaves untouched by name/type.

- **Enum prefixes shouldn't repeat context the field/message name already gives.** On an `airspeed` message's `source` field, he preferred `SOURCE_` over the more verbose `AIRSPEED_SOURCE_`, calling the longer form redundant.
  A prefix change must keep the field's `[@enum PREFIX]` tag in sync — `tool-check.md` will independently flag a mismatch as `constant_not_in_assigned_enum`, so don't duplicate that finding, just check the two are consistent before suggesting a shorter prefix.
  https://github.com/PX4/PX4-Autopilot/pull/25878#discussion_r2494226892
- **Prefer established industry terminology over PX4-internal phrasing**, even where it reads slightly redundant with context — e.g. `state_of_charge` (matching the widely-used "SoC") over a PX4-only `capacity`/`remaining`.
  https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2128301559 , https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2142810254
- **Name a field for what it actually represents today, not how it originated.** He objected to a `priority` field that in practice is only ever used as a unique device instance identifier, proposing `id`.
  https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2073408190
- **Don't conflate two concepts in one field or enum.** He flagged a `warning` field whose documented values are actually device *states*: "Either it's a state or a warning but this is just confusing."
  https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2128645897
- Note, not a rule to enforce: he's on record that some existing, seemingly-clunky names (the old manual-control `x, y, z, r` axes) have a defensible rationale once you know the history — don't treat "this name looks odd" alone as grounds for a finding.
  https://github.com/PX4/PX4-Autopilot/pull/19310#issuecomment-1076077626

## When a comment is required, and what it should say

Applies to any field/constant this PR adds, or whose comment text this PR changes, and to the message-level short/long description whenever this PR adds or edits one — see `shared.md`.

- **State the field's real-world purpose when it isn't obvious from the name**, especially for a field that just passes through or logs an external protocol value. He explicitly praised "This is currently used only for logging cell status from MAVLink" as exactly the right kind of addition.
  https://github.com/PX4/PX4-Autopilot/pull/24662#discussion_r2073289792
- **Use terminology precise to the field's actual semantics, not generic copied phrasing.** He objected to describing a location field's sentinel values as "uncontrolled" — a word he reserves for setpoint fields — preferring "special values" for a sensor/measurement field.
  https://github.com/PX4/PX4-Autopilot/pull/24662#discussion_r2036703485
- **Pure metainformation (version numbers, max-instance-count constants) belongs at the very top of the message**, ahead of the fields it describes. Only actionable when this PR is adding such a constant or already relocating fields — don't ask a PR to reorder an untouched message.
  https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2128289509 , https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2128655885
- **Terminal periods on short field descriptions: unsettled, don't police it.** He raised this as an open question, not an asserted rule. Defer to `style-guide.md` (no period on a single-sentence description) and leave it at that — don't cite him for a period/no-period finding.
  https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2128301559
- **A field that no longer earns its keep should be removed, not just documented as unused.** If a new/changed comment describes a field as unused, dead, or vestigial, suggest removing it (`minor` — a suggestion, not a blocker) rather than treating the documentation as sufficient.
  https://github.com/PX4/PX4-Autopilot/pull/24789#issuecomment-2976557585

## Other conventions worth checking

- **Blank lines that group related fields (and their constants) must survive a reformat.** If this PR's diff touches the blank-line structure around a field group, check the grouping wasn't accidentally collapsed. Agreed by multiple maintainers, not just him.
  https://github.com/PX4/PX4-Autopilot/pull/25228#discussion_r2630202488 , https://github.com/PX4/PX4-Autopilot/pull/25878#discussion_r2630291299
- **Comment alignment: contested, report at `minor` only.** He's argued repeatedly for a single space before `#` and against column-padded/aligned comments (padding means a single field-name-length change rewrites every line in the block, polluting `git blame`). As of the last comment found this was still being actively discussed with other maintainers, not settled project style — so a padded/aligned block in a diff is worth a `minor` note citing this thread, never a `style` or `bug` finding.
  https://github.com/PX4/PX4-Autopilot/pull/25878#discussion_r2493929851 , https://github.com/PX4/PX4-Autopilot/pull/25878#discussion_r2606477864 , https://github.com/PX4/PX4-Autopilot/pull/25878#discussion_r2630291299
- Not a checkable rule, background only: he tends to treat "document this message" and "clean up this message's fields" as one job, not two — worth keeping in mind when a PR's description frames itself as pure documentation but the fields underneath clearly need more than a comment.
  https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2128330015
