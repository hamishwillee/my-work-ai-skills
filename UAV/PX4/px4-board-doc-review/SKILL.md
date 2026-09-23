---
name: px4-board-doc-review
description: Review of flight-controller board documentation in PX4-Autopilot pull requests — the board's docs/en/flight_controller/ page checked against a numbered page template, against the board's own source files (boards/<vendor>/<board>/), against the pages of its siblings (same reference design, same support category, same manufacturer), and against the board support guide's documentation requirements. Use when a PX4-Autopilot PR adds or changes a board under boards/ or adds a page under docs/en/flight_controller/, when px4-doc-review hands off such a PR, or when the user asks to review a board's docs on a local branch. Use px4-doc-review for the page's prose, and review-pr or code-review for the board firmware itself.
allowed-tools: Bash(gh pr view:*) Bash(gh pr diff:*) Bash(gh pr list:*) Bash(gh api:*) Bash(git -C:*) Bash(grep:*) Bash(diff:*) Bash(ls:*)
---

# PX4 flight-controller board documentation review

You are reviewing the documentation of a PX4 flight-controller board: its page under `docs/en/flight_controller/`, and where that page is listed.
The deliverable is a submission checklist and a report of issues with line numbers.

The page is checked four ways:

- against **the page template** (`references/page-template.md`): the sections, headings, anchors and content every board page needs, as numbered checks
- against **the board's own files** in `boards/<vendor>/<board>/`, which say what PX4 actually configures
- against **its siblings**: pages for boards on the same reference design, in the same support category, and from the same manufacturer
- against **the board support guide**, which says what a board PR's docs must contain

This skill doesn't review the page's prose (that's `px4-doc-review`) or the board firmware (that's `review-pr` or `code-review`).

**Read-only**, here and in every subagent this review spawns.
Never modify a file in the repository under review, and never run `gh pr comment`, `gh pr review`, or any other write operation.
Your output is the report; the reviewer posts it themselves.

## Workflow

Scope, Dispatch, and Report run here, in this context.
Three lenses run, each over the whole board change (a board PR has one page, so there's no batching): **source-consistency**, **sibling-comparison**, and **completeness**.
Verify runs inside each lens agent, against the requirements in `references/shared.md`.

The files in this skill directory:

- `references/shared.md`: read-only rule, scope, the board facts every lens shares, sources of truth, verification, severity
- `references/board-sources.md`: the board facts worksheet, which board file answers which page claim and how to read it (processors, UART order, DShot by chip family), and the reference-design diff
- `references/page-template.md`: the page skeleton and every numbered check (`T-...`) a board page must pass, with severities
- `references/source-consistency.md`, `references/sibling-comparison.md`, `references/completeness.md`: the three lenses
- `preferences.example.md`: boilerplate for a reviewer's own preference file

Read `references/shared.md` yourself before Scope: the board facts you establish there follow its table.

### 1. Scope

**Where the request came from.**

- **Handed off from `px4-doc-review`.** The PR, its head and base SHAs, and its changed-file list are already known; use them, and skip the PR checks below.
  Return your findings in the handoff shape (see Report) rather than a full report.
- **A PR number or URL.** A bare number means `PX4/PX4-Autopilot`.
  Stop and say so if the PR is closed, merged, or automated.
  Read the description and any linked issue.
- **No PR given.** Offer a selection list (`AskUserQuestion` where available): **Enter PR** or **Local branch**.
  For a local branch, find the clone (`references/shared.md`, "Reaching the sources"), take the merge-base with the default branch, and diff the working tree against it: `git -C <clone> merge-base HEAD origin/main`, then `git -C <clone> diff <merge-base> --stat`.
  Cite the branch and merge-base wherever a PR number and SHA would go, and skip the flight-log check (there's no PR description), noting it below the tables.

**Is there a board to review?**
From the changed files, find:

- new or changed board directories: `boards/<vendor>/<board>/` containing a `default.px4board`
- new or changed pages under `docs/en/flight_controller/` other than the category and index pages (`autopilot_*.md`, `index.md`, `pixhawk_series.md`, `silicon_errata.md`)

Then choose the mode:

| Change | Mode |
| --- | --- |
| New board directory, or new board page | **New board**: all three lenses |
| Changed board files for a board that has a page | **Board change**: source-consistency only, limited to the areas the board-file diff touches, plus a check that the page still matches them even if the page itself didn't change |
| Changed board page only | **Page change**: source-consistency and sibling-comparison, limited to the changed lines |

If the PR has none of these, say so and stop.
A PR touching several boards reviews each one separately, with its own checklist and findings.

**Establish the board facts** in `references/shared.md` ("Board facts"): board directory, build targets, board page, reference design, support category, manufacturer.

**Fill in the board facts worksheet** (`references/board-sources.md`, "Board facts worksheet") from the board's files at the head SHA, using the lookup table, "Processors", "UART order", and "DShot by chip family".
Every value gets its file and line; write `unknown` rather than guess.
The lenses work from this worksheet, so a mistake here spreads to all of them: work out the UART order and the per-output DShot capability step by step rather than by eye.

Then **choose the comparator pages** by the rules in `references/sibling-comparison.md` ("Choosing comparator pages"), so all three lenses use the same set.

**Run the reference-design diff** (`references/board-sources.md`, "Diffing against the reference design") once, when there's a reference design, and record which areas differ from `boards/px4/<design>/` in the worksheet's last row.

**Reviewer preferences.**
Load `~/.config/px4-board-doc-review/preferences.md` if it exists, and apply it here, not in the lens agents.
Skip it silently if it's absent.
Preferences may set the output shape, emphasis, suppressed severities, and tone; never the sources of truth, the read-only rule, or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

### 2. Dispatch

Spawn one subagent per lens that the mode calls for.
Give each the prompt below, with the brackets filled in, as written rather than summarised:

> You are the [lens] lens of a PX4-Autopilot flight-controller board documentation review, and you are read-only: never modify a file, and never run `gh pr comment`, `gh pr review`, or any other write operation.
>
> Read ${CLAUDE_SKILL_DIR}/references/shared.md in full, then ${CLAUDE_SKILL_DIR}/references/[lens-file].md in full, then ${CLAUDE_SKILL_DIR}/references/board-sources.md and ${CLAUDE_SKILL_DIR}/references/page-template.md.
> Those files are your instructions.
>
> Repository PX4/PX4-Autopilot, [PR [number], head SHA [sha], base SHA [sha] / local clone at [path], branch [name], merge-base [sha]].
> Mode: [new board / board change / page change]. [For board change and page change: the areas or lines in scope.]
> Board facts: [the shared.md board facts table, filled in].
> Board facts worksheet: [the board-sources.md worksheet, filled in, with file:line for every value].
> Comparator pages: [each page, and why it was chosen].
> Files in scope: [board page, SUMMARY.md, category page, _sidebar.md if changed, any other changed docs/en/ page that mentions the board].
> Board files (evidence, never review targets): [paths].
>
> Your lens is done only when every rule in your lens file has been applied.
> Verify every finding as shared.md requires, then return one row per finding with the file path, line number, issue, severity, suggestion, and the evidence you checked.
> [Completeness lens: also return the checklist, one row per item, with status and evidence.]
> [Sibling-comparison lens: also return the comparator pages you used.]
> Return anything shared.md sends below the tables (source disagreements, unverified wiring claims, firmware questions) as separate notes.
> If you find nothing, say so rather than returning prose.

`${CLAUDE_SKILL_DIR}` is this skill's own directory.
On a harness that doesn't substitute it, replace it with the absolute path of the directory this file was loaded from; never pass a relative path.

**Work silently.**
Say nothing between dispatching and the report: no plan, no per-lens status.

**Without subagents.**
Read every file under `references/` and run the lenses in sequence, holding to the same verification and return shape.
Add one line below the tables saying the review ran in a single context.

### 3. Report

Merge what the lenses returned: the same problem on the same line from two lenses is one row, keeping the more specific evidence and the higher severity.
Different problems on one line at the same severity combine into one row naming each; different severities stay separate rows.

**Report findings, not machinery.**
Never name a lens or say how many ran.
A file with no findings gets its row in the per-file summary and nothing else.

#### Standalone report

Sections, captioned, in this order, with nothing above the first:

1. **Board summary.** One line per board: board directory, board page, reference design, support category, and the comparator pages used.
   Then the bug count and where the bugs are ("2 bugs in 1 of the 3 changed doc files"; "No bugs in 3 changed doc files"), and the finding total.
2. **Board submission checklist**, for a new board: the completeness checklist as a table, `Item | Status | Evidence`, every item listed.
3. **Issues found**:

   | Issues found | bug | style | minor | total |
   | --- | --- | --- | --- | --- |
   | Matches board source | | | | |
   | Matches sibling pages | | | | |
   | Template and submission requirements | | | | |

   Rows count the findings of source-consistency, sibling-comparison, and completeness, in that order.
   When there are bugs, list each with its file and line after the table.
4. **Issue summary per file**: `File | bug | style | minor | total`, ordered by bug count, every in-scope file listed.
5. **Detailed review**: one table per file with findings, `Line | Issue | Severity | Suggestion`, sorted by line.
   End each Issue with the template check it fails, in parentheses (`(T-RC5)`), when there is one, so the reviewer can look the rule up.
   Keep the Suggestion column to one line; a longer rewrite goes below the tables, keyed to file and line.
   A missing-section finding's Suggestion is "Add the stub below", and the stub goes below the tables (`references/page-template.md`, "Stubs for missing sections").
   A missing-content finding's Line is where the content would go (`references/shared.md`, "Verification"); the flight-log finding's Line is `PR description`.

Below the tables, only these, in this order, each only when it applies:

1. Suggestion blocks too long for the Suggestion column, then the stubs for missing sections, one block per run of adjacent missing sections, in page order
2. Firmware questions the docs can't settle (two labels on one device, a board ID that looks copied), for the reviewer to raise; point to `review-pr` for the firmware review itself
3. Where the sources disagree, including comparators that agree with each other against the template
4. Claims that matter for wiring but couldn't be checked against any source
5. A single note that the page's prose wasn't reviewed, suggesting `px4-doc-review` (standalone runs only)
6. A single note if the review ran in one context

Cite lines as GitHub links with the full head SHA and one line of context each side:
`https://github.com/PX4/PX4-Autopilot/blob/<full-sha>/docs/en/flight_controller/<page>.md#L12-L16`

**In chat by default, in a file when asked.**
A file copy opens with a title line (`# PX4-Autopilot PR <n> — board docs review: <board directory>`) and labelled `PR`, `Head SHA`, and `Reviewed` lines, is written outside the clone, and overwrites any earlier copy.
For a local-branch run, offer to open the report in VS Code once it's shown, if `command -v code` finds it: write the file first if it only exists in chat, then run `code <path>`.

#### Handoff to px4-doc-review

When `px4-doc-review` handed off the PR, return:

- the board summary lines
- the submission checklist table
- the merged findings, one row per finding, with file, line, issue, severity, suggestion, and evidence
- the below-the-tables notes, except the "prose wasn't reviewed" note

`px4-doc-review` places them in its own report under **Board documentation review**, and handles deduplication against its own lenses.
