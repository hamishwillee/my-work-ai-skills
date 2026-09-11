# Naming lens

Applies only to a field or constant this PR **introduces, renames, or retypes** — classify every declaration first using "New-or-changed determination" in `shared.md`.
A declaration classified **Comment-only edit** or **Untouched** never gets a naming finding, no matter how the name reads: names are effectively part of a wire contract, and this PR isn't the place to relitigate one it isn't already changing.

**Single-message audit mode is the one exception** (`SKILL.md`): with no diff and no PR, every field/constant in the audited message is in scope, but every finding here is capped at `minor` and phrased as advisory rather than actionable — there's no PR here creating a reason to accept the compat break a rename implies, so the most this lens can do is flag it for awareness.

Work the diff systematically: every in-scope declaration gets checked against every rule below before you're done.

## Written-standard checks (`style-guide.md`)

- Field names: lower `snake_case`. Constant names: `UPPER_SNAKE_CASE`, and when part of a grouped enum, sharing the exact prefix named in the governing field's `[@enum PREFIX]` tag.
- A description that just restates the name is a naming/description mismatch worth flagging (`style`) — but note whether the fix is a better name or a real description; don't assume it's always the name that's wrong.

## Community-convention checks (`community-conventions.md`, "Naming" section, cite the link)

- Enum prefix repeating context already in the field/message name → suggest the shorter form, `style`, and confirm the field's `@enum` tag would still match it (if it wouldn't, say so — the fix needs both changed together, or `tool-check.md` will separately flag `constant_not_in_assigned_enum`).
- PX4-internal/ad-hoc phrasing where established industry terminology exists → suggest the industry term, `style`, only when you can name the term and its currency (don't invent a claim that a term is "standard" without being able to say where).
- A field named for its origin/history rather than its current use → `style`, name the mismatch and what the field is actually used for now (check publishers/subscribers in the same PR's diff if that's what shows current use).
- One field or enum conflating two distinct concepts → `style`, name both concepts and why one field/enum can't hold both cleanly.

## What this lens doesn't do

- Never propose a rename or retype for a declaration classified **Comment-only edit** or **Untouched** — see the gate above. If a name is genuinely bad but out of scope, it can go below the tables as a "pre-existing, not actionable" note (`SKILL.md`), at most once per file, not once per bad name.
- Don't duplicate `tool-check.md`'s mechanical `@enum`/unit checks — this lens covers whether a name is *well-chosen*, not whether it's syntactically valid.
- Don't second-guess a name with a defensible rationale just because it reads oddly to you — `community-conventions.md` has a worked example of this (the manual-control axis names) precisely to discourage it.
