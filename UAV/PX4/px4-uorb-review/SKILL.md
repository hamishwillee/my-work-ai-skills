---
name: px4-uorb-review
description: Editorial review of uORB message (.msg) documentation in PX4-Autopilot pull requests — field/constant naming, comment presence and quality, and compliance with the uORB documentation standard, checked in part by running the project's own doc generator. Use when the user asks for a review of a PX4-Autopilot PR touching msg/*.msg or msg/versioned/*.msg, or pastes such a PR URL or number. Use px4-doc-review instead for docs/en/ prose changes, and code-review for firmware/build/CI changes with no msg/ documentation content.
allowed-tools: Bash(gh pr view:*) Bash(gh pr diff:*) Bash(gh pr list:*) Bash(gh api:*) Bash(git -C:*) Bash(git worktree:*) Bash(python3:*) Bash(grep:*)
---

# PX4 uORB message documentation review

You are reviewing PX4-Autopilot uORB message definitions (`msg/*.msg`, `msg/versioned/*.msg`) for naming, comment quality, and compliance with the project's uORB documentation standard.
This is prose-and-convention review, not code review: the deliverable is a report of issues with line numbers, plus whatever the project's own doc generator reports.

**Read-only**, here and in every subagent this review spawns, with one narrow exception described in `references/shared.md`: the tool-check lens may create and tear down a disposable local git worktree purely to run `Tools/msg/generate_msg_docs.py`.
Never modify a file in the PR under review, and never run `gh pr comment`, `gh pr review`, or any other write operation.
The one file you may create is the report itself, only when the reviewer asks for it and only outside the clone.
Your output is the report; the reviewer posts it to GitHub themselves, after reading it (except for a local run, where there's nothing to post — see "Offer to open in an editor" at the end of the Report step).

## Workflow

Scope, Dispatch, and Report run here, in this context.
Four lenses apply: **tool-check** (runs the project's own generator/validator, unbatched, once), **naming**, **comments**, and **grammar-spelling** — the latter three batched over the changed `.msg` files the same way.
Naming and comments are both gated by the new-or-changed classification in `references/shared.md`: a field/constant this PR doesn't itself introduce or rename never gets a naming finding, and only gets a comment finding if this PR is the one that changed its comment.
Verify runs inside each lens agent, against the requirements in `references/shared.md`.

The files in this skill directory:

- `references/shared.md`: the read-only rule, scope, the new-or-changed gate, sources of truth, verification, and severity (including the `hint` tier)
- `references/style-guide.md`: the uORB documentation standard, extracted as checkable rules
- `references/community-conventions.md`: @MaEtUgR's documented naming and comment norms from real PR review history, with links
- `references/tool-check.md`: runs `Tools/msg/generate_msg_docs.py -e` and reports its output
- `references/naming.md`, `references/comments.md`, `references/grammar-spelling.md`: the three prose/convention lenses
- `preferences.example.md`: boilerplate for a reviewer's own preference file

Read `references/shared.md` yourself before reporting: merging findings and counting the triage table both depend on the severity definitions and the new-or-changed gate.

### 1. Scope

A bare PR number means `PX4/PX4-Autopilot`; any other repo has to be named, as `owner/PX4-Autopilot#456` or a full URL.

**No PR given.**
When the reviewer doesn't name a PR, number, or URL, present a numbered selection list rather than a single yes/no question:

1. Enter PR
2. Local branch
3. A particular message

Use a selection-list prompt where the harness supports one (e.g. `AskUserQuestion` in Claude Code); otherwise a plain numbered list in chat, and read back whichever number or label they reply with.

**"Enter PR."** Ask for the PR number/URL and continue with the rest of this Scope step as normal.

**"A particular message."** The fast path for a reviewer who already knows what they want to check — it skips straight to naming a topic instead of first computing and choosing from a full changed-topics list, and it implies local branch (no separate "local vs PR" question needed).
Ask which message/topic, if it wasn't already given in the same request.
Find a local `PX4-Autopilot` clone (`references/shared.md`, "Reaching the sources"); if none exists, say so and fall back to asking for a PR number/URL.
Resolve the name to its file (see "Topics vs message names" below), then check just that one file for a diff against the default branch:
- **Changed.** Run the standard diff-based review scoped to this one topic only — the same outcome as picking "Local branch" and then this topic from its second selection list, just without computing the full list first.
- **Unchanged.** Switch to **single-message audit mode** (below) directly.

**"Local branch."** Find a local `PX4-Autopilot` clone (`references/shared.md`, "Reaching the sources"); if none exists, say so and fall back to asking for a PR number/URL, since there's nothing local to check.
Then, regardless of which branch is currently checked out, diff the working tree (uncommitted edits included) against the default branch to find what changed:
```
git -C <clone> merge-base HEAD origin/<default>
git -C <clone> diff <merge-base>
```
(Find `<default>` with `git -C <clone> remote show origin`, or just try `main`.)
From that diff, collect every changed `msg/*.msg` / `msg/versioned/*.msg` file and, from those, every changed **topic** — see "Topics vs message names" below for how a file maps to one or more topic names.

- **One or more topics changed.** Present a second selection list: one option per individual topic (`Topic: <name>`), plus one option covering all of them at once (`All changed topics: <name1>, <name2>, ...`).
  Picking a single topic scopes the whole review — Scope, Dispatch, Report — to that topic's file and diff only; picking "all" reviews every changed topic together, the same shape as a PR that touched all of them.
  Either way this stays a diff-based review: the new-or-changed gate applies exactly as it does for a PR, just sourced from this local diff instead of `gh pr diff`. Run the rest of this skill exactly as for a PR — no `gh` calls, no PR number or head/base SHA; cite the branch name and merge-base commit instead wherever the workflow below would cite those.
- **Nothing changed.** There's no diff to review — say so and stop. Don't fall back to asking for a topic to audit here; that's what the "A particular message" option at the top level is for, so this path doesn't need to ask it a second way.

#### Topics vs message names

A uORB **topic** is the runtime publish/subscribe name a reviewer thinks in; a message's **struct/file name** (`SensorUwb`, matching `msg/SensorUwb.msg`) is what `generate_msg_docs.py -m` and every other lens actually key on. They're usually related by simple case conversion (`SensorUwb` ↔ `sensor_uwb`) but aren't always identical — one message can back several topics via `# TOPICS name1 name2` (`references/style-guide.md`, "Multi-topic messages").

- **File → topic(s)**: read any `# TOPICS ...` lines in the file and use those names; if it has none, its one implied topic is the snake_case of its message name.
- **Topic → file** (here, and when resolving a reviewer-given name via "A particular message" or in single-message audit mode): search every `.msg` file's `# TOPICS` lines for an exact match first, then fall back to matching the snake_case of a message name. If nothing matches, say so and ask again rather than guessing.

Stop and say so if the PR is closed, merged, a draft, or automated (dependency bumps, metadata regeneration, bot commits).

Read the PR description and mine it for what the change is and why.
When it's empty, note that in the report and review anyway.

**A linked issue is part of the scope.**
When the description links or closes an issue, read the issue and judge the PR against what it asked for.

**Filter to `msg/*.msg` and `msg/versioned/*.msg`.**
Take the PR's full changed-file list, but only those two locations are reviewed — see `references/shared.md`, "Scope," for how `msg/px4_msgs_old/**` and generated `docs/en/msg_docs/**` are handled.
If nothing in scope changed, say so and stop.

**Classify every declaration before dispatching.**
For each changed `.msg` file, work the diff and classify every field/constant declaration as New, Renamed or retyped, Comment-only edit, or Untouched (`references/shared.md`, "New-or-changed determination").
This classification is what `naming.md` and `comments.md` gate on, so do it once here rather than leaving each lens agent to re-derive it independently and possibly disagree.

**Reviewer preferences.**
Load `~/.config/px4-uorb-review/preferences.md` if it exists and apply it here, not in the lens agents.
Skip it silently if it's absent.
Preferences may set the shape of the output, extra emphasis, suppressed severities, orientation questions, and tone — never the sources of truth or their precedence, the read-only rule, the new-or-changed gate, or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

**Batch by changed lines.**
`tool-check` runs once, unbatched, over every changed message name in the PR (it's one script invocation regardless of how many messages).
For `naming`, `comments`, and `grammar-spelling`, fill batches to roughly **1500 changed lines**, giving a file whose own diff exceeds that a batch to itself — in practice a `.msg` PR rarely needs more than one batch.
When more than one batch is needed, say how many and ask the reviewer how to proceed.

**Single-message audit mode** (entered from "A particular message" when the named topic turns out to have no local changes vs the default branch).
Resolve the topic to its file per "Topics vs message names" above.
There's no diff, so the new-or-changed gate in `references/shared.md` doesn't apply the normal way — instead, every field and constant in the resolved message counts as in scope for every lens, since the reviewer explicitly asked to audit this one file rather than a change.
`tool-check` runs `-m "<MessageName>"` directly against the working tree (see `references/tool-check.md`, "Local and audit modes" — no scratch worktree needed, nothing is being diffed against a PR).
`naming.md` still applies, but every finding is capped at `minor` and phrased as advisory ("worth knowing, not something to fix without another reason to touch this field") rather than actionable: a field's name is still a wire contract even when you're looking at it outside a PR, and there's no PR here forcing a compat break that would make a rename free.
`comments.md` and `grammar-spelling.md` run at their normal severities — those are always freely fixable regardless of mode.
Batching still applies if the one message is unusually large, but in practice it won't be.

### 2. Dispatch

Spawn one subagent per lens instance: one `tool-check` pass (unbatched), and one pass each of `naming`, `comments`, `grammar-spelling` per batch.

Give each agent the prompt below, filling the bracketed slots, and pass it as written rather than as your own summary:

> You are the [lens] lens of a PX4-Autopilot uORB message documentation review, and you are read-only: never modify a file, and never run `gh pr comment`, `gh pr review`, or any other write operation. [Tool-check lens only: you may create and must tear down a disposable local git worktree, per your own reference file.]
>
> Read ${CLAUDE_SKILL_DIR}/references/shared.md in full, then ${CLAUDE_SKILL_DIR}/references/[lens-file].md in full.
> Those two files are your instructions. [Naming/comments lenses: also read ${CLAUDE_SKILL_DIR}/references/community-conventions.md in full, and ${CLAUDE_SKILL_DIR}/references/style-guide.md in full.] [Comments lens only: for the message-level long description, only flag whether one is present or absent — don't search for publishers/subscribers, don't judge whether a present one is accurate, and don't draft a suggestion. If one's missing, its Suggestion column is the literal placeholder text `(pending source search)`, nothing more specific — the main agent runs that part itself, separately (it needs to time it and may need to check in with the reviewer), and will replace your placeholder with the real draft before the report.]
> Load only the sources they name, once for your whole assignment rather than once per file.
>
> Repository PX4/PX4-Autopilot, PR [number], head SHA [sha], base SHA [sha]. [Local branch mode instead: Repository PX4/PX4-Autopilot, local clone at <path>, branch [name] vs default branch [name] at merge-base [commit], scope: [selected topic / all changed topics]. Single-message audit mode instead: Repository PX4/PX4-Autopilot, local clone at <path>, auditing topic [name] ([MessageName].msg) in full, no diff.]
> Your assignment is [every changed msg file in the PR / this batch / the single audited file]: [file paths].
> Here is the new-or-changed classification for every declaration in your assignment, computed by the main agent: [paste the classification].
> Review only the files listed above — nothing else changed in this PR is yours to check.
>
> Work the diff systematically.
> Your lens is done only when every rule your file names has been applied to every in-scope declaration/line you hold.
>
> Verify every finding as references/shared.md requires, then return one row per finding, carrying the file path, the line number, the issue, the severity, the suggestion, and the evidence you verified against.
> If you find nothing, say so rather than returning prose.

`${CLAUDE_SKILL_DIR}` is this skill's own directory, and Claude Code substitutes it for you.
On a harness that leaves it unsubstituted, replace it yourself with the absolute path of the directory this file was loaded from.
Never pass a relative path: the working directory during a review is the `PX4-Autopilot` clone or the reviewer's shell, not the skill directory.

**Work silently.**
Say nothing between dispatching and the report itself: no plan, no per-lens status, no count of what has come back.

**Without subagents.**
On a harness that can't spawn them, read all seven files under `references/` yourself and run the lenses in sequence over the whole PR, holding to the same verification and return shape.
Add one line below the tables saying the review ran in a single context.

**Long-description verification.**
Runs in this context, one in-scope message at a time — never delegated to the `comments` subagent, because it needs to time itself and may need to check in with the reviewer mid-run, and a dispatched subagent can do neither.

For every in-scope message (`references/comments.md`, "Message-level long description"):

1. Note the start time, run that one message's publisher/subscriber search (`references/comments.md`, "Finding the actual publishers and subscribers"), note the end time, and record how long it took.
2. Turn the result into that message's long-description finding exactly as `comments.md` describes: **missing** → replace the `comments` subagent's `(pending source search)` placeholder with the actual drafted paragraph, folding in both the publisher/subscriber findings and anything the short-description check flagged as trimmed from an oversized short description for the same message; **present** → confirmed, or flagged as wrong/incomplete with the specific correction.
   The placeholder is never something the report shows — if you reach the report step and a Suggestion column still reads `(pending source search)` or any other generic stand-in ("add a long description," "consider documenting this"), that message's verification didn't actually run; go back and run it, or apply the "Stop" handling below, rather than publishing the placeholder.
3. Keep a running total of time spent on this search across the review. Once that total passes **5 minutes** *and* messages remain unchecked, stop and ask the reviewer whether to continue, quoting the estimated time to finish as (average seconds per message so far) × (messages remaining).
   - **Continue**: keep going the same way, checking in again the next time the running total crosses a further 5-minute boundary with messages still remaining.
   - **Stop**: skip the source search entirely for every message not yet reached, and instead:
     - No long description at all → replace the subagent's `(pending source search)` placeholder with a `minor` warning in the normal per-file table, labelled as unverified (no drafted suggestion — the search that would produce one didn't run).
     - A long description already present → no finding; list it in a single below-the-tables note naming every message whose existing long description wasn't checked against source (see "What goes below the tables").

This budget applies only to the publisher/subscriber source search. Every other check in this skill — tool-check, naming, field/constant comments, short-description length, grammar/spelling — runs to completion regardless of how long the search takes or whether the reviewer chooses to stop it.

### 3. Report

Collect what the lens agents returned. Two different situations both count as "merging," and they're easy to conflate — don't:

- **Same underlying problem, flagged by more than one lens.** A true duplicate: one row, keeping the more specific evidence and the higher severity.
- **Different problems on the same line.** Every one of them survives — merging never means picking the "more interesting" one and dropping the rest. Same severity → fold into one row that names each issue and combines their suggestions (see "Detailed per-file review" below — fold means *combine into one row*, not *keep only one*). Different severities → keep separate rows, one per severity, so a `bug` is never buried inside a `style` row.

A mechanical tool-check finding is exactly as real as a narrative finding from another lens: a capitalization fix and a multiple-whitespace fix on the same line are two different problems, not competing drafts of one problem, even though both happen to be `style`. **Before finalizing the report, check that every tool-check finding on a changed line actually appears in the tables** — its own row, or named inside a combined row — since it's easy to let a mechanical finding get silently dropped under a more prominent one for the same line. If one's missing from your draft, put it back rather than let it go.

The report has four captioned sections in this order: **PR triage summary**, **Issue summary per file**, **Detailed per-file review of changed lines**, and **Hints** (omit this last section entirely if there are none — don't write an empty heading).
Open at the triage summary, with no header block ahead of it.

**In chat by default, in a file when asked.**
A reviewer who asks for the report as a file, or whose preferences set a path, gets the same sections written there and a one-line confirmation in chat.
A file copy opens with a title line and three labelled lines, adjusted to whichever of the four modes produced the review:

```markdown
# PX4-Autopilot PR 25990 — Add SensorUwb message

- PR: https://github.com/PX4/PX4-Autopilot/pull/25990
- Head SHA: fada6198026a53cd77293b8b551d06da8edfbb07
- Reviewed: 2026-09-03
```

```markdown
# PX4-Autopilot local review — branch add-sensor-uwb vs main, topic sensor_uwb

- Local clone: ~/github/PX4/PX4-Autopilot
- Merge-base: fada6198026a53cd77293b8b551d06da8edfbb07
- Scope: topic sensor_uwb (1 of 3 changed topics — sensor_uwb, wind, vehicle_land_detected)
- Reviewed: 2026-09-03
```

```markdown
# PX4-Autopilot single-message audit — topic sensor_uwb (SensorUwb.msg)

- Local clone: ~/github/PX4/PX4-Autopilot
- Branch: main (clean working tree, full-file audit, not a diff)
- Reviewed: 2026-09-03
```

Write it outside the clone under review, and overwrite the path rather than editing around what's already in it.

**Report findings, not machinery.**
Never name a lens, say how many ran, or write that something was confirmed or verified: that a finding is in the report already means it passed verification.
A file with no findings gets its row in the per-file summary and nothing else.

**PR triage summary.**

Open with the bug count and where the bugs are, as "2 bugs in 1 of the 3 changed files."
With no bugs, "No bugs in 3 changed files."
Follow it with the changed-line and finding totals.
When the PR links an issue, add one line for whether it solves it.

| Issues found | bug | style | minor | total |
| --- | --- | --- | --- | --- |
| Generated-doc validity | | | | |
| Naming | | | | |
| Comments | | | | |
| Grammar & spelling | | | | |

Four rows, in that order, and no others — one per lens, since here (unlike a pure prose review) each lens checks a genuinely different kind of thing: `Generated-doc validity` is `tool-check.md`'s findings; the rest are self-explanatory.
`hint`-severity findings never appear in this table — they're not findings against the PR, they're suggestions, and they live only in the Hints section.

When there are bugs, close the section by listing every one, each with its file and line.
When there are none, close the section after the table.

**Issue summary per file.**

| File | bug | style | minor | total |
| --- | --- | --- | --- | --- |

Ordered by bug count. Every changed in-scope file gets a row.

**Detailed per-file review of changed lines.**

One table per changed file that has findings, the file path as a heading, sorted by line number ascending.

| Line | Issue | Severity | Suggestion |
| --- | --- | --- | --- |
| 12 | `[meters]` isn't an allowed unit (generator: `unknown_unit`) | bug | Use `[m]` |
| 24 | New field `priority`: name describes origin, not current use — this instance-ID field is never used as a priority | style | Rename to `id` ([MaEtUgR](https://github.com/PX4/PX4-Autopilot/pull/24789#discussion_r2073408190)) |
| 31 | Comment "Uwb dist" doesn't say what the value measures or its frame | style | "Distance to anchor, in the body frame" or similar |
| 9 | Comment starts lowercase; multiple whitespace before the field name (generator: `field_or_constant_has_multiple_whitepsace`); unit written in prose instead of the `[unit]` tag | style | `uint64 timestamp # [us] Time since system start` |

- **One issue per row, one row per line — unless the extra problems on that line carry different severities.** "One row per line" means *combine*, not *pick one*: row 9 above folds three separate findings (a comments.md capitalization rule, a tool-check whitespace note, and a comments.md units-metadata rule) into a single row precisely because all three landed on the same line at the same severity — see "Report," above, for why none of the three gets dropped in favor of the others.
- Write each row so it's clear to the **author**, not just to you.
- **Keep the Suggestion column to one line**; a longer rewrite goes below the tables, keyed to file and line.

**Hints.**

Only Tier-2 grammar hints from `grammar-spelling.md` (never spelling, never Tier 1, never anything from another lens).
One flat list, not a table, each entry keyed to file and line, phrased as a suggestion:

```markdown
## Hints

- `msg/versioned/Wind.msg:14` — "Wind speed measure at anchor" reads more naturally as "Wind speed measured at anchor."
```

**What goes below the tables.**
No closing remarks. These are permitted, in this order, each only when it applies:

1. Suggestion blocks too long for the Suggestion column, keyed to file and line
2. Pre-existing issues on declarations this PR didn't change (`shared.md`, "New-or-changed determination") — including a naming or comment issue on an **Untouched** declaration, and a tool-check finding whose line falls outside any changed hunk
3. Where the sources disagree (`shared.md`, "Sources of truth")
4. A single note if `tool-check.md` couldn't run (no local clone found)
5. A single note if the PR description was empty
6. A single note if the review ran in one context rather than one subagent per lens
7. A single list naming every message whose existing long description wasn't checked against source, if the reviewer chose to stop the publisher/subscriber search early ("Long-description verification")
8. **Hints** section (above), last of all

To cite a line as a GitHub link, use the head SHA in full:
`https://github.com/PX4/PX4-Autopilot/blob/<full-sha>/msg/versioned/Wind.msg#L12-L16`

**Offer to open in an editor, for local runs.**
Once the report itself has been shown, and only when this review ran against a local branch (any of "A particular message," "Local branch," or single-message audit mode — never a PR, since there the reviewer's next step is posting to GitHub, not opening an editor locally): check whether a `code` command is on the reviewer's `PATH` (`command -v code`).
If it is, offer to open the report in VS Code.
On "yes": if the report wasn't already written to a file (the chat-only default), write it first — same format as "In chat by default, in a file when asked," to a sensible default path if the reviewer doesn't name one — then run `code <path>` to open it.
If `code` isn't found, or the reviewer declines, drop it without further comment; this is a courtesy for a local run, not something to press on.
