---
name: px4-param-review
description: Review of PX4-Autopilot parameter descriptions (short, long, and enum/bitmask option labels in module.yaml, *_params.yaml, or legacy PARAM_DEFINE comment blocks) against the project's description standard — no facts lost in a rewrite, no duplication of option labels or metadata, terse short descriptions, stock phrasing — with schema validation and a before/after size count. Use when the user asks for a review of a PX4-Autopilot PR that adds or changes parameter descriptions, including description-shortening PRs, or asks for parameter descriptions on a local branch or named parameters to be checked. Use px4-doc-review for docs/en/ prose changes; it hands parameter changes to this skill.
allowed-tools: Bash(gh pr view:*) Bash(gh pr diff:*) Bash(gh pr list:*) Bash(gh api:*) Bash(git -C:*) Bash(python3:*) Bash(grep:*)
---

# PX4 parameter description review

You are reviewing PX4-Autopilot parameter descriptions: the `short` and `long` description and the option labels of each parameter a PR adds or changes.
The standard they're reviewed against comes from the parameter-trimming work in [PX4-Autopilot#27758](https://github.com/PX4/PX4-Autopilot/pull/27758) and its first split-off, [#28850](https://github.com/PX4/PX4-Autopilot/pull/28850): descriptions ship in flash, so they should say everything a reader needs to configure the parameter, once, in the right place, and nothing else.
The deliverable is a report of issues with line numbers.

**Read-only**, here and in every subagent this review spawns (`references/shared.md`, "Read-only").
Never modify a file in the clone, and never run `gh pr comment`, `gh pr review`, or any other write operation.
The one file you may create is the report itself, only when the reviewer asks for it and only outside the clone.

## Workflow

Scope, the tool check, Dispatch, and Report run here, in this context.
Three lenses apply to every in-scope parameter: **facts** (nothing configuration-affecting lost, everything true to the code), **concision** (the standard's placement and redundancy rules), and **wording** (grammar, clarity, YAML form).
Verify runs inside each lens agent, against the requirements in `references/shared.md`.

The files in this skill directory:

- `references/shared.md`: the read-only rule, scope, the classification of each parameter, sources of truth, verification, and severity
- `references/description-standard.md`: the description standard as checkable rules with IDs, and where each came from
- `references/examples.md`: how #28850 applied the standard, before-and-after, and the lessons from #27758's review
- `references/facts.md`, `references/concision.md`, `references/wording.md`: the three lenses
- `references/tool-check.md`: running `scripts/param_desc_check.py`, which classifies parameters, flags mechanical rule breaks, counts description size, and runs the schema validator
- `preferences.example.md`: boilerplate for a reviewer's own preference file

Read `references/shared.md` yourself before reporting: merging findings and counting the triage table both depend on its severity definitions.

### 1. Scope

A bare PR number means `PX4/PX4-Autopilot`; any other repo has to be named, as `owner/PX4-Autopilot#456` or a full URL.

**No PR given.**
When the reviewer names no PR, offer a selection list (`AskUserQuestion` where the harness has it, otherwise a numbered list in chat):

1. Enter PR
2. Local branch: the parameter changes on the current branch of a local clone, against the merge-base with `main`, uncommitted edits included
3. Named parameters: audit the current text of the parameters the reviewer names, with no diff (audit mode in `references/shared.md`)

When invoked by `px4-doc-review`, the PR number, head and base SHAs, and changed-file list are passed in; skip straight to filtering.

Stop and say so if the PR is closed, merged, a draft, or automated (bot commits, metadata regeneration, Crowdin translation sync).
The exception is a reviewer who explicitly asks for a closed or merged PR to be reviewed anyway, such as to calibrate this skill.

Read the PR description, and note any size saving or validation it claims: the tool check confirms or contradicts it.
When the description links an issue or a tracking PR, read it and judge the PR against it; for a split-off of #27758, the tracking PR's spec is the standard, and any parameter its description lists as a known pre-existing error should get the correction the tracker asked for, or be left alone.

**Filter to parameter definitions.**
In scope are the changed files that define parameters: `*.yaml` under `src/` with a `parameters:` list, and `.c` files whose changes touch a `PARAM_DEFINE_*` comment block.
A hand-edited `docs/en/advanced_config/parameter_reference.md` is a `bug` (`references/shared.md`, "Scope"); a regenerated one is ignored.
Other changed files are context for the facts lens, not reviewed.
If no definition file changed, say so and stop.

**Reviewer preferences.**
Load `~/.config/px4-param-review/preferences.md` if it exists and apply it here, not in the lens agents; skip it silently if it's absent.
Preferences may set the shape of the output, extra emphasis, suppressed severities, orientation questions, and tone.
They may not override the sources of truth or their precedence, the read-only rule, the classification, or the requirement that every finding carry evidence; a preference that tries to is reported as a conflict and not applied.

### 2. Tool check

Run `scripts/param_desc_check.py` as `references/tool-check.md` describes, over every in-scope YAML file.
Its output gives every changed parameter's classification, line numbers, size before and after, and candidate flags, and ends with the schema validator's result.

**Batch by parameters.**
Fill batches to roughly **40 Rewritten or New parameters**, keeping a file's parameters together unless the file alone exceeds that.
Each parameter the facts lens checks means reading old text and code, which is why batches are counted in parameters rather than lines.
When the PR needs more than one batch, say how many and ask the reviewer how to proceed: every batch in turn, or a subset of files they name.
A large sweep like #27758 (186 files) needs this; a split-off like #28850 (14 parameters) is one batch.

### 3. Dispatch

Spawn one subagent per lens per batch: facts, concision, and wording.
Give each the prompt below, filling the bracketed slots, and pass it as written rather than as your own summary of it:

> You are the [lens] lens of a PX4-Autopilot parameter description review, and you are read-only: never modify a file, and never run `gh pr comment`, `gh pr review`, or any other write operation.
>
> Read ${CLAUDE_SKILL_DIR}/references/shared.md in full, then ${CLAUDE_SKILL_DIR}/references/description-standard.md in full, then ${CLAUDE_SKILL_DIR}/references/[lens-file].md in full. [Concision lens only: also read ${CLAUDE_SKILL_DIR}/references/examples.md in full.]
> Those files are your instructions.
>
> Repository PX4/PX4-Autopilot, PR [number], head SHA [sha], merge-base [sha], local clone at [path]. [Local-branch mode instead: local clone at [path], branch [name], working tree against merge-base [sha]. Audit mode instead: local clone at [path], auditing the current text of [parameters], no diff.]
> Your assignment is these parameters, with the classification and line numbers computed by the main agent: [paste the script's output for this batch, flags included].
> [Legacy .c definitions to check by hand, if any: [file paths].]
> [Other files the PR changes, as context for what the parameters do: [file paths].]
> Review only the parameters listed above.
>
> Your lens is done only when every rule your file names has been applied to every parameter you hold.
>
> Verify every finding as references/shared.md requires, then return one row per finding, carrying the file path, the line number, the parameter, the issue, the severity, the suggestion, and the evidence you verified against. [Facts lens only: also return the dropped-content note, one line per Rewritten parameter.]
> If you find nothing, say so rather than returning prose.

`${CLAUDE_SKILL_DIR}` is this skill's own directory, and Claude Code substitutes it for you.
On a harness that leaves it unsubstituted, replace it yourself with the absolute path of the directory this file was loaded from; never pass a relative path, since the lenses run from the clone.

**Work silently.**
Say nothing between dispatching and the report: no plan, no per-lens status, no count of what has come back.

**Without subagents.**
On a harness that can't spawn them, read every file under `references/` and run the three lenses in sequence, one at a time, over each batch, holding to the same verification and return shape.
Add one line below the tables saying the review ran in a single context.

### 4. Report

Collect what the lenses returned and merge it.
The same problem caught by two lenses (a cryptic label is both an O3 concision finding and a lost fact) is one row, with the more specific evidence and the higher severity.
Different problems on the same line are all kept: same severity, fold them into one row that names each; different severities, one row each, so a `bug` is never buried in a `style` row.
Every validator error on a changed line appears in the tables.

The report has three captioned sections in this order: **PR triage summary**, **Issue summary per file**, and **Detailed per-file review**, followed by the permitted notes below the tables.
Open at the triage summary, with no header block ahead of it.

**In chat by default, in a file when asked.**
A reviewer who asks for the report as a file, or whose preferences set a path, gets the same sections there and a one-line confirmation in chat.
The file opens with a title line and three labelled lines, and nothing else above the triage summary:

```markdown
# PX4-Autopilot PR 28850 — docs(params): shorten verbose descriptions of commonly used parameters

- PR: https://github.com/PX4/PX4-Autopilot/pull/28850
- Head SHA: b36ca53ca4367ce3a33d688a3a2aa4e0cb1690e9
- Reviewed: 2026-09-29
```

For a local branch, name the clone, branch and merge-base instead of the PR and head SHA.
Write it outside the clone, and overwrite the path rather than editing around what's there.

**Report findings, not machinery.**
Never name a lens or the script, or say that something was confirmed or verified: that a finding is in the report means it passed verification.
A file with no findings gets its row in the per-file summary and nothing else.

**PR triage summary.**

Open with the bug count and where the bugs are, as "2 bugs in 1 of the 7 changed files", or "No bugs in 7 changed files".
Follow it with one line counting the parameters by classification ("14 rewritten, 0 new"), one line with the size change of their description text (`references/tool-check.md`, "Using the output"), and the finding total.
When the PR links an issue or tracking PR, add one line for whether it does what that asked.

| Issues found | bug | style | minor | total |
| --- | --- | --- | --- | --- |
| Schema validity | | | | |
| Facts | | | | |
| Concision | | | | |
| Wording | | | | |

Four rows, in that order, and no others.
When there are bugs, close the section by listing each one with its file, line and parameter.

**Issue summary per file.**

| File | Parameters | bug | style | minor | total |
| --- | --- | --- | --- | --- | --- |

Ordered by bug count; every in-scope file gets a row, with its count of Rewritten and New parameters.

**Detailed per-file review.**

One table per file with findings, the file path as a heading, sorted by line.
Example rows:

| Line | Parameter | Issue | Severity | Suggestion |
| --- | --- | --- | --- | --- |
| 125 | `BAT${i}_I_OVERWRITE` | Unit given in prose ("in amps") while `unit:` is unset; the schema allows `A` (L7) | minor | Add `unit: A` and drop "in amps" |
| 8 | `EXAMPLE_MODE` | `long` re-lists all four options, which the labels already give (L3) | style | Delete the list; move "requires calibration" into option 1's label |

- One issue per row, one row per line unless the problems on it carry different severities.
- Write each row for the author: name the rule ID in the Issue column, so the author can look it up.
- Keep the Suggestion column to one line; a longer rewrite goes below the tables as a YAML snippet.

**What goes below the tables.**
No closing remarks. These are permitted, in this order, each only when it applies:

1. Suggestion blocks too long for the Suggestion column, keyed to file, line and parameter, as YAML the author can paste
2. **Dropped content**: the facts lens's one line per Rewritten parameter, saying what was cut and the rule that permits it, so the reviewer can judge the trim at a glance (in a `<details>` block when there are more than ten)
3. Pre-existing issues in Untouched parameters, including validator errors outside the PR's changes
4. Where the sources disagree (`references/shared.md`, "Sources of truth"), such as old text that contradicts the code
5. A single note if the script or the validator couldn't run
6. A single note if the PR description was empty
7. A single note if the review ran in one context rather than one subagent per lens

To cite a line as a GitHub link, use the head SHA in full:
`https://github.com/PX4/PX4-Autopilot/blob/<full-sha>/src/lib/battery/module.yaml#L124-L126`

**Offer to open in an editor, for local runs.**
After a local-branch or audit review, if `command -v code` finds VS Code, offer to open the report there, writing it to a file first if it's only in chat.
Drop it silently if `code` isn't found or the reviewer declines.
