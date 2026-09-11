# Comment-necessity lens

Applies to:

- Any field or constant classified **New**, **Renamed or retyped**, or **Comment-only edit** in "New-or-changed determination" (`shared.md`) — i.e. anything whose comment text this PR actually introduces or changes. Never a declaration classified **Untouched**.
- The message-level short/long description block, whenever this PR adds a new message or edits that block.

Work the diff systematically: every in-scope comment gets checked against every rule below.

## Message-level short description

Applies to any message this PR adds, or whose short description this PR edits.

- **Missing entirely**: `tool-check.md` already catches this mechanically (`summary_missing`) — don't duplicate it here.
- **General clarity is out of scope, beyond the one exception below.** Don't judge whether a short description would mean something to a reader unfamiliar with the domain, and don't raise a finding purely because it "reads as unclear" — too subjective to check reliably, and the written standard gives no rule to check it against.
- **Length is in scope.** A short description is a label, not a sentence — in practice it's close to the de-camel-cased message name (`SensorUwb` → "UWB sensor" / "Sensor UWB"), one line, no terminal period. When it instead reads as a full sentence, runs to multiple clauses, or is noticeably longer than that (as a rough guide, much past 8-10 words, or containing its own internal comma/clause structure), flag it `minor` and suggest a tighter alternative in the Suggestion column.
  **Whatever this trims out is real content, not waste** — hand it forward rather than dropping it. Name, in this finding or a note attached to it, what substance the short description was carrying beyond a label (e.g. "measurement source, sensor make/model"), so the long-description check below can fold it into a drafted long description instead of losing it. Don't draft the long description here yourself — that's the other section's job, and it also has the publisher/subscriber search to add — just make sure the trimmed content is visibly handed off, not silently discarded.
- **Cheap acronym expansion is the one clarity check made, because it's mechanical rather than a judgement call.** When the short description contains an acronym that isn't spelled out anywhere in it, and expanding it parenthetically still fits comfortably within the length budget above (`UWB sensor` → `Ultra-wideband (UWB) sensor`), suggest the expanded form as a `minor` note. Don't force an expansion that would push the description past the length budget into full-sentence territory — in that case say so and point to the long description as the place for the fuller form instead, rather than bending the short description to fit both jobs.
  This is still not a general clarity check: an acronym is a mechanical thing to spot and a parenthetical expansion is a mechanical fix, which is why it's the one exception to the rule above. Don't extend it to rewording a description for tone, precision, or anything short of "this acronym is never expanded and expanding it is free."

## Message-level long description

Optional per the written standard, but should be provided whenever the message's role in the system genuinely isn't obvious from its short description and fields alone — which, in practice, is most messages, since "who publishes and subscribes this, and why" is rarely evident just from the field list.

Applies to any message this PR adds, or whose long description this PR edits.
For a PR that adds substantial new fields to an existing, undocumented message without touching its header at all, add one below-the-tables `minor` suggestion ("consider adding a long description while you're here") rather than a full finding — the gate above still governs whether this is a real finding or just a nudge.

**What a good long description covers**: which module(s) publish the topic(s) this message backs, which module(s) subscribe to them, and how the message fits into the data flow — "estimator output consumed by the position controller," not just a list of names. It doesn't need to enumerate every generic/ubiquitous consumer (logger, MAVLink bridge) individually; naming them collectively or omitting them is fine.

**This part runs in the main agent, not in this lens's subagent** — see `SKILL.md`, "Long-description verification," for why (timing and a possible reviewer check-in) and for what happens when the reviewer chooses to stop partway through. When you're running as the dispatched `comments` subagent and you find a message with no long description, your entire output for it is a bare flag — file, line, "long description missing" — with the Suggestion column left as the literal placeholder `(pending source search)`, never a drafted sentence, a guess, or a generic instruction like "add a long description." That placeholder exists precisely so the main agent can find and replace every one of them; if you write anything more specific there, the merge step in `SKILL.md` has no reliable way to tell your guess apart from the main agent's verified one, and a guess is what ends up in the report.

**Finding the actual publishers and subscribers.** Requires a local `PX4-Autopilot` clone (`shared.md`, "Reaching the sources") — if none is available, say so and skip this half of the lens rather than guessing at architecture from the message alone.
For each topic the message backs (`SKILL.md`, "Topics vs message names"):

1. `grep -rl "ORB_ID(<topic>)" <clone>/src` to find every file referencing the topic.
2. For each match, read enough surrounding context to classify it: a `uORB::Publication`/`uORB::PublicationMulti` declaration or an `orb_advertise`/`.publish(` call nearby means that file's module publishes it; a `uORB::Subscription`/`uORB::SubscriptionCallbackWorkItem` declaration or an `orb_subscribe`/`.copy(`/`.update(` call means it subscribes.
3. Map each match to its owning module by path (`src/modules/<name>/`, `src/drivers/<name>/`, `src/lib/<name>/`, ...), de-duplicated to one entry per module rather than one per file.

That publisher/subscriber list is the ground truth the long description is checked against — not a guess, and not the same thing as what the message's *fields* suggest it should be used for.

- **Missing.** No long description on an in-scope message: draft one, and offer the actual drafted paragraph as the suggestion (below the tables if more than a line, per `SKILL.md`) — never a generic instruction like "add a long description of how the topic is published/used." A finding that only tells the author *that* something's missing, without drafting it, isn't done. Draft it from two things together, not the publisher/subscriber search alone:
  1. The discovered publishers/subscribers (above) — who uses this and how it fits the data flow.
  2. Whatever the short-description check flagged as trimmed from an oversized short description for this same message — if that check found the short description carrying real content beyond a label, that content belongs in this draft, not nowhere.

  Severity `style` when the message's purpose or architectural fit genuinely isn't clear without one; `minor` when it would be a nice-to-have but the message is already small and self-explanatory (a handful of clearly-named diagnostic fields, say).
- **Present but wrong or incomplete.** An in-scope long description that misstates or omits a discovered publisher/subscriber, or that doesn't actually explain the message's role (restates the short description, or is boilerplate): `style`. Name the specific module it misses or misstates — never just "incomplete."
- **Don't overreach.** Only check what's mechanically discoverable by source search. Don't speculate about *why* the architecture is shaped the way it is beyond what a comment elsewhere in the source already says, and don't fail a description for reasonably omitting a generic consumer.

## Field/constant presence

- A **new** field or constant added with no comment at all, where the standard doesn't exempt it (`ORB_QUEUE_LENGTH`, `MESSAGE_VERSION` don't need one): `style`. Name the field and that it's undocumented.
- Don't demand a comment on a field whose name is genuinely self-explanatory in context (`uint64 timestamp` next to an existing sibling `# [us] Time since system start` pattern) — match the standard's own tone, which is "should clarify purpose when not obvious," not "every field needs a paragraph."

## Field/constant quality, once a comment exists

From `style-guide.md`:

- Description starts with a capital letter; terminal-period rule as stated there (single-sentence: no period; multi-sentence: normal punctuation throughout). Don't cite `community-conventions.md` for this — see its own note that the period question is unsettled there, so the written standard is the only source for it.
- Description doesn't just restate the field name (cross-reference with `naming.md` if the actual problem looks like a naming issue instead).
- **Units metadata, when the field needs it.** Per `style-guide.md`, "Field-level documentation": any field that isn't purely boolean or enum-valued needs a `[<unit>]` tag (a genuinely unitless numeric field uses `[-]`); `tool-check.md` only validates a unit *that's already present* against the allowed list, so a field with no `[...]` tag at all is this lens's job, not the generator's — don't assume the tool already caught it.
  A very common variant of the same defect: the unit is spelled out in the prose description instead of the tag — `# time since system start (microseconds)`, `# distance in meters`, `# heading, degrees`. Treat this the same as a missing tag, `style`, and always give the fix as one combined rewrite that both adds the tag and drops the now-redundant prose, never as two separate suggestions:
  `uint64 timestamp # time since system start (microseconds)` → `uint64 timestamp # [us] Time since system start`.
  This exact `timestamp`/`timestamp_sample`-with-prose-unit shape recurs constantly across the tree — apply the fix every time you see it, not just the first time.
  **Don't assert a unit value you haven't sourced.** The two cases above are safe because the unit is already stated, in the field's own comment, in this exact spot — moving it into the tag is mechanical. When a field has no `[<unit>]` tag *and* its own comment says nothing about units, don't fill the tag from the field name, a plausible-sounding neighboring comment, or a similar field elsewhere. Confirm it first, in order of preference: (1) the publishing module's actual source in `src/**` — a raw value's scaling, a documented range, a struct comment (`shared.md` source-of-truth #3); (2) an adjacent group/internal comment or a sibling field in the same message, *only* when it unambiguously states the unit for this exact field, and name it explicitly as your source rather than folding it in silently. If neither confirms a specific unit, still raise the missing-tag finding (`style`), but leave the value out of the suggestion — `add a [<unit>] tag once the unit is confirmed` — rather than guessing `[deg]`/`[m]`/etc. Either way, name the source you used for the unit in the finding's evidence, the same as any other cited rule.

From `community-conventions.md`, "When a comment is required" (cite the link with each finding):

- Real-world purpose/usage context stated when not obvious from the name alone, especially for a protocol-passthrough or logging-only field — `style` if missing on an in-scope field where the purpose genuinely isn't obvious from the name.
- Comment wording uses terminology precise to what the field actually measures/represents, not generic phrasing copied from elsewhere in the file or from a similar-looking field — `style`, and name the more precise term.
- A metainformation constant (version number, max-instance count) this PR introduces should be placed and documented at the top of the message, ahead of the fields it describes — `minor` (placement, not correctness).
- A comment that describes the field as unused, dead, or vestigial: suggest removing the field rather than documenting its disuse — `minor`, a suggestion the author can decline.

## Structural checks not covered by the tool

- **Enum grouping placement**: constants sharing a prefix declared immediately beneath the field carrying the matching `@enum` tag (`style-guide.md`). The tool validates the prefix *matches*; it doesn't validate *placement* — check that separately here, `style`, only for constants this PR adds or moves.
- **Blank-line grouping** (`community-conventions.md`, "Other"): if this PR's diff touches the blank-line structure around a field group, check it wasn't accidentally collapsed — `style`, cite the link.
- **Comment alignment** (`community-conventions.md`, "Other"): a newly-added or reformatted block using column-padded/aligned comments instead of a single space before `#` — `minor` only, cite the link, and say explicitly in the finding that this is a contested preference under discussion, not settled project style.

## What this lens doesn't do

Never raise a finding — of any severity — against a comment on a declaration classified **Untouched**.
That includes a comment that's factually stale or clearly wrong: note it, if truly notable, only as a below-the-tables "pre-existing, not actionable" item (`SKILL.md`), same as `naming.md`'s equivalent case.
