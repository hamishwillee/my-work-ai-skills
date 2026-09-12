---
name: mavlink-command-review
description: Reviews mavlink-devguide documentation of MAV_CMD commands and message fields — hand-authored pages describing what a specific command or field means/does (e.g. en/services/mission_item_detail.md), not the auto-generated en/messages/*.md themselves — for accuracy against the MAVLink XML, cited evidence for any implementation-specific claim, and terseness matching the repo's existing style. Use when reviewing a mavlink-devguide PR that touches this kind of content, or when given such a PR by number/URL. Also consult it proactively, without being asked, whenever drafting or editing this kind of documentation yourself in mavlink-devguide, to self-check claims before writing them. A future sibling skill (not yet written) will cover en/services/*.md protocol-level prose that isn't about one command's own parameters — mission.md's upload/download/state-machine sections, camera.md, ftp.md, and similar.
allowed-tools: Bash(gh pr view:*) Bash(gh pr diff:*) Bash(gh pr list:*) Bash(gh api:*) Bash(git -C:*) Bash(grep:*)
---

# MAVLink command/message documentation review

You are reviewing mavlink-devguide pages that describe individual `MAV_CMD` commands or message fields — their meaning, parameters, and per-autopilot behaviour.
This skill exists because a real PR ([mavlink/mavlink-devguide#761](https://github.com/mavlink/mavlink-devguide/pull/761)) bundled a pure file-reorganization with silent, uncited content changes: a behavioural claim added with no source, a params table's documented scope quietly widened, and a wrong claim deleted without anyone noticing until a reviewer manually diffed old and new files by hand. This skill exists so that doesn't have to happen again by hand.

Two modes:

- **Review mode.** A PR (or local branch/diff) already exists. Run Scope → Dispatch → Report below, producing a report the reviewer posts themselves.
- **Authoring mode.** No PR exists yet — you are the one drafting or editing a page in scope (see "Scope reminder" in `references/shared.md`). Skip Scope/Dispatch/Report; instead, before finishing your edit, read `references/shared.md` and `references/accuracy.md`, `references/change-discipline.md`, `references/style-terseness.md` yourself and hold your own draft to the same rules, out loud in your response if anything fails: name the unevidenced claim or the XML disagreement rather than silently fixing your own draft into something that merely reads more confidently. This mode never posts anything or invents a PR to review — it's a self-check on your own upcoming edit.

**Read-only in review mode**, here and in every subagent it spawns.
Never modify a file in the repository under review, and never run `gh pr comment`, `gh pr review`, or any other write operation.
The one file you may create is the report itself, only when the reviewer asks for it and only outside the clone.
Your output is the report; the reviewer posts it to GitHub themselves, after reading it.
Authoring mode is naturally not read-only — you're the one editing — but it never touches files outside the one you were already asked to write.

## Workflow (review mode)

Three lenses apply to every changed file in scope: **accuracy**, **change-discipline**, and **style-terseness**.
Verify runs inside each lens agent, against the requirements in `references/shared.md`.

The files in this skill directory:

- `references/shared.md`: the read-only rule, scope reminder, sources of truth and how to reach them, verification, and severity
- `references/accuracy.md`: lens — claims checked against the XML (via `en/messages/*.md`) and, for implementation-specific claims, a citable source
- `references/change-discipline.md`: lens — does a wording change hide inside a commit labelled as a pure move/reorg; is a new claim added with no evidence at all
- `references/style-terseness.md`: lens — terseness and this repo's own authoring conventions (callout syntax, link style, etc., from the repo's `CLAUDE.md`)
- `preferences.example.md`: boilerplate for a reviewer's own preference file

Read `references/shared.md` yourself before reporting: merging findings and the severity table both depend on it.

### 1. Scope

A bare PR number means `mavlink/mavlink-devguide`; any other repo has to be named, as `owner/mavlink-devguide#123` or a full URL.

Stop and say so if the PR is closed, merged, a draft, or automated (Crowdin sync, the scheduled "MAVLink messages update" bot commits, dependency bumps).

Read the PR description and mine it for what the change is and why.
When it's empty, note that in the report and review anyway.

**A linked issue is part of the scope.**
When the description links or closes an issue, read it and judge the PR against what it asked for.

**Filter to in-scope files.**
Take the PR's full changed-file list. In scope: any hand-authored page whose primary subject is the meaning, parameters, or behaviour of one or more specific `MAV_CMD` commands or message fields — currently `en/services/mission_item_detail.md` is the clearest example, and any future page shaped like it (per-command sections with a Params table) is in scope the same way.
A page that's primarily about a *protocol* (upload/download sequencing, state machines, service-level workflow — `en/services/mission.md`'s own body, `camera.md`, `ftp.md`, etc.) is out of scope for this skill; say so and suggest the services-focused sibling skill once it exists.
A change to `en/messages/*.md` itself is always a `bug`-severity finding from `change-discipline.md` regardless of what it says — those files are generated from the MAVLink XML and should never be hand-edited in a PR (see `references/shared.md`, "Scope reminder").

If nothing in scope changed, say so and stop.

**Reviewer preferences.**
Load `~/.config/mavlink-command-review/preferences.md` if it exists and apply it here, not in the lens agents.
Skip it silently if it's absent.
Preferences may set the shape of the output, extra emphasis, suppressed severities, orientation questions, and tone — never the sources of truth or their precedence, the read-only rule, or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

**Batch by changed lines**, only if needed.
mavlink-devguide PRs in scope for this skill are typically one or two files; fill batches to roughly 1500 changed lines per lens and only ask the reviewer how to proceed if a PR actually needs more than one.

### 2. Dispatch

Spawn one subagent per lens (accuracy, change-discipline, style-terseness), unbatched unless Scope found a PR large enough to need it.

Give each agent the prompt below, filling the bracketed slots, and pass it as written rather than as your own summary:

> You are the [lens] lens of a mavlink-devguide command/message documentation review, and you are read-only: never modify a file, and never run `gh pr comment`, `gh pr review`, or any other write operation.
>
> Read ${CLAUDE_SKILL_DIR}/references/shared.md in full, then ${CLAUDE_SKILL_DIR}/references/[lens-file].md in full.
> Those two files are your instructions. Load only the sources they name, once for your whole assignment rather than once per file.
>
> Repository mavlink/mavlink-devguide, PR [number], head SHA [sha], base SHA [sha].
> Your assignment is [every in-scope changed file in the PR / this batch]: [file paths].
> Review only the files listed above — nothing else changed in this PR is yours to check.
>
> Work the diff systematically. Your lens is done only when every rule your file names has been applied to every changed line you hold.
>
> Verify every finding as references/shared.md requires, then return one row per finding, carrying the file path, the line number, the issue, the severity, the suggestion, and the evidence you verified against.
> If you find nothing, say so rather than returning prose.

`${CLAUDE_SKILL_DIR}` is this skill's own directory, and Claude Code substitutes it for you.
On a harness that leaves it unsubstituted, replace it yourself with the absolute path of the directory this file was loaded from.

**Work silently.** Say nothing between dispatching and the report itself.

**Without subagents.** On a harness that can't spawn them, read all three reference files yourself and run the lenses in sequence, holding to the same verification and return shape. Add one line below the tables saying the review ran in a single context.

### 3. Report

Collect what the lens agents returned and merge duplicates: the same problem flagged by more than one lens is one row, keeping the more specific evidence and the higher severity. Different problems on the same line stay separate rows even at the same severity — fold them into one row that names each, never drop one in favour of the other.

The report has three captioned sections in this order: **PR triage summary**, **Issue summary per file**, **Detailed per-file review of changed lines**. Open at the triage summary, no header block ahead of it.

**In chat by default, in a file when asked.** A file copy opens with:

```markdown
# mavlink-devguide PR 761 — Mission item - separate out to own doc

- PR: https://github.com/mavlink/mavlink-devguide/pull/761
- Head SHA: af6db5e70867415d3f1c36abd3e9468aab1bfe92
- Reviewed: 2026-09-12
```

Write it outside the clone under review, and overwrite the path rather than editing around what's already in it.

**Report findings, not machinery.** Never name a lens, say how many ran, or write that something was confirmed or verified — a finding being in the report already means it passed verification.

**PR triage summary.**

Open with the bug count and where the bugs are ("2 bugs in 1 of 2 changed files"; "No bugs in 1 changed file"). When the PR links an issue, add one line for whether it solves it.

| Issues found | bug | style | minor | total |
| --- | --- | --- | --- | --- |
| XML/evidence accuracy | | | | |
| Change discipline | | | | |
| Style & terseness | | | | |

Three rows, in that order, no others. When there are bugs, close the section by listing every one, each with its file and line. When there are none, close after the table.

**Issue summary per file.**

| File | bug | style | minor | total |
| --- | --- | --- | --- | --- |

Ordered by bug count. Every in-scope changed file gets a row, including ones with no findings.

**Detailed per-file review of changed lines.**

One table per changed file that has findings, the file path as a heading, sorted by line number.

| Line | Issue | Severity | Suggestion |
| --- | --- | --- | --- |
| 115 | "A fixed wing vehicle will fly a circle circle" — duplicated word, and asserts hovering-vehicle behaviour not stated anywhere in the XML or cited to source | bug | Fix the typo; either cite a source for the circling claim or drop it |
| 143 | LOITER_TO_ALT's Heading Required/Xtrack rows link to Exit Conditions, extending scope beyond what the pre-existing text stated | style | Confirm against the XML (both fields are defined for this command) and note the link is a protocol fact, not an implementation-support claim |

- **One issue per row, one row per line** unless the extra problems on it carry different severities.
- Write each row so it's clear to the **author**, not just to you.
- **Keep the Suggestion column to one line**; a longer rewrite goes below the tables, keyed to file and line.

**What goes below the tables.** No closing remarks. Permitted, in this order, each only when it applies:

1. Suggestion blocks too long for the Suggestion column, keyed to file and line
2. Pre-existing issues on lines this PR didn't change
3. Where the sources disagree — including any XML-vs-prose conflict this PR didn't itself introduce (see `references/accuracy.md`, "When the doc and the XML disagree")
4. A single note if the PR description was empty
5. A single note if the review ran in one context rather than one subagent per lens

To cite a line as a GitHub link, use the head SHA in full:
`https://github.com/mavlink/mavlink-devguide/blob/<full-sha>/en/services/mission_item_detail.md#L115`
