---
name: px4-rangefinder-doc-review
description: Review of rangefinder (distance sensor) documentation in PX4-Autopilot pull requests — the sensor's page under docs/en/sensor/ or docs/en/dronecan/ checked against a numbered page template, against the driver that runs it (src/drivers/distance_sensor/<driver>/, its parameters, startup lines and Kconfig), against the pages of similar rangefinders (same connection, same manufacturer), and against where it must be listed (SUMMARY.md, sensor/rangefinders.md). Handles single-model pages and family pages that cover several models. Use when a PX4-Autopilot PR adds or changes a driver under src/drivers/distance_sensor/ or a rangefinder page, when px4-doc-review hands off such a PR, when the user asks to review a rangefinder's docs on a local branch, or when the user asks for an existing rangefinder page to be updated, fixed or restructured to the template (suggested and applied one approved change at a time). Use px4-doc-review for the page's prose, px4-param-review for the driver's parameter descriptions, and review-pr or code-review for the driver itself.
allowed-tools: Bash(gh pr view:*) Bash(gh pr diff:*) Bash(gh pr list:*) Bash(gh api:*) Bash(git -C:*) Bash(grep:*) Bash(diff:*) Bash(ls:*) WebFetch
---

# PX4 rangefinder documentation review

You are reviewing the documentation of a PX4 rangefinder (distance sensor): its page under `docs/en/sensor/` or `docs/en/dronecan/`, and where that page is listed.
The deliverable is a documentation checklist and a report of issues with line numbers.

The aim is that every rangefinder page gives a reader all they need to buy, connect, enable and test the sensor, in the same format as every other rangefinder page.

The page is checked four ways:

- against **the page template** (`references/page-template.md`): the sections, headings, anchors and content every rangefinder page needs, as numbered checks, with a variant for family pages that cover several models
- against **the driver** in `src/drivers/distance_sensor/<driver>/`, which says what PX4 actually does with the sensor
- against **its siblings**: pages for rangefinders with the same connection, role and manufacturer
- against **its listings**: `SUMMARY.md`, the rangefinder index, and the DroneCAN and Collision Prevention pages where they apply

This skill doesn't review the page's prose (that's `px4-doc-review`), the driver's parameter descriptions (`px4-param-review`), or the driver code (`review-pr` or `code-review`).

**Read-only**, here and in every subagent this review spawns.
Never modify a file in the repository under review, and never run `gh pr comment`, `gh pr review`, or any other write operation.
Your output is the report; the reviewer posts it themselves.

**Updating a page.**
When the reviewer asks for a page to be updated, fixed or restructured rather than reviewed, run the review below first if there isn't one, then follow `references/page-update.md`.
That is the one mode that edits files in the clone, and only the changes the reviewer approves, one at a time.
It still never posts a comment.

## Workflow

Scope, Dispatch, and Report run here, in this context.
Three lenses run, each over the whole rangefinder change: **source-consistency**, **sibling-comparison**, and **completeness**.
Verify runs inside each lens agent, against the requirements in `references/shared.md`.

The files in this skill directory:

- `references/shared.md`: read-only rule, scope, the rangefinder facts every lens shares, sources of truth, verification, severity
- `references/driver-sources.md`: the rangefinder facts worksheet, which driver file answers which page claim and how to read it, which configuration keys build a driver into firmware and how to count the boards that set them, and a map of drivers to pages
- `references/page-template.md`: the page kinds, the page skeleton with its standard wording, and every numbered check (`R-...`) a rangefinder page must pass, with severities
- `references/source-consistency.md`, `references/sibling-comparison.md`, `references/completeness.md`: the three lenses
- `references/page-update.md`: bringing an existing page up to the template one approved suggestion at a time; read by you, not by a lens
- `preferences.example.md`: boilerplate for a reviewer's own preference file

Read `references/shared.md` yourself before Scope: the rangefinder facts you establish there follow its table.

### 1. Scope

**Where the request came from.**

- **Handed off from `px4-doc-review`.** The PR, its head and base SHAs, and its changed-file list are already known; use them, and skip the PR checks below.
  Return your findings in the handoff shape (see Report) rather than a full report.
- **A PR number or URL.** A bare number means `PX4/PX4-Autopilot`.
  Stop and say so if the PR is closed, merged, or automated.
  Read the description and any linked issue.
- **No PR given.** Offer a selection list (`AskUserQuestion` where available): **Enter PR**, **Local branch**, or **Existing page** (a page on the default branch, reviewed as it stands).
  For a local branch, find the clone (`references/shared.md`, "Reaching the sources"), take the merge-base with the default branch, and diff the working tree against it: `git -C <clone> merge-base HEAD origin/main`, then `git -C <clone> diff <merge-base> --stat`.
  Cite the branch and merge-base wherever a PR number and SHA would go.
  For an existing page there's no diff: review the whole page in **new rangefinder** mode, and say in the summary that the page predates the template.

**Is there a rangefinder to review?**
From the changed files, find:

- new or changed driver directories under `src/drivers/distance_sensor/`
- new or changed rangefinder pages (`references/shared.md`, "What counts as a rangefinder page")
- changes to `docs/en/sensor/rangefinders.md`

Then choose the mode:

| Change | Mode |
| --- | --- |
| New driver directory, or new rangefinder page | **New rangefinder**: all three lenses |
| Changed driver for a rangefinder that has a page | **Driver change**: source-consistency only, limited to what the driver diff touches (parameters, models, range limits, baud rate, commands, Kconfig), plus a check that the page and its `rangefinders.md` row still match even if neither changed |
| Changed rangefinder page only | **Page change**: source-consistency and sibling-comparison, limited to the changed lines |
| `rangefinders.md` only | **Index change**: the listing checks (R-L2 to R-L4, R-L7) for the changed rows and sections, each against its page and driver |

If the PR has none of these, say so and stop.
A PR touching several rangefinders reviews each one separately, with its own checklist and findings.
A new driver with no page at all is a new rangefinder whose checklist starts with "Page exists: no".

**Establish the rangefinder facts** in `references/shared.md` ("Rangefinder facts"): page, page kind, models, connections, drivers, role, in firmware, status, manufacturer.

**Fill in the rangefinder facts worksheet** (`references/driver-sources.md`, "Rangefinder facts worksheet") from the driver's files at the head SHA, once per driver, using the lookup table.
Every value gets its file and line; write `unknown` rather than guess.
The lenses work from this worksheet, so a mistake here spreads to all of them: read the model list, the range limits per model, and the baud rate from the source line by line rather than from the page, and run the greps in "In firmware" for the configuration keys and the boards that set them rather than estimating.

**Read the manufacturer's material** and fill in the manufacturer facts (`references/shared.md`, "Manufacturer facts"): the product page, and the current manual or datasheet it links, read in full.
A PDF has to be extracted to text first (`references/shared.md`, "Reaching the sources"); don't leave it unread because `WebFetch` returned binary.
The pinout, power, mounting, serial settings and frame format are usually there and nowhere else, and without them the lenses can only report those as unverified.
If the material genuinely can't be read, say so in the facts and below the tables.

**Find who to ask** (`references/shared.md`, "Finding who to ask"), for a new rangefinder or an existing page: the people who could review the page or answer what the sources leave open.

Then **choose the comparator pages** by the rules in `references/sibling-comparison.md` ("Choosing comparator pages"), so all three lenses use the same set.

**Reviewer preferences.**
Load `~/.config/px4-rangefinder-doc-review/preferences.md` if it exists, and apply it here, not in the lens agents.
Skip it silently if it's absent.
Preferences may set the output shape, emphasis, suppressed severities, and tone; never the sources of truth, the read-only rule, or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

### 2. Dispatch

Spawn one subagent per lens that the mode calls for.
Give each the prompt below, with the brackets filled in, as written rather than summarised:

> You are the [lens] lens of a PX4-Autopilot rangefinder documentation review, and you are read-only: never modify a file, and never run `gh pr comment`, `gh pr review`, or any other write operation.
>
> Read ${CLAUDE_SKILL_DIR}/references/shared.md in full, then ${CLAUDE_SKILL_DIR}/references/[lens-file].md in full, then ${CLAUDE_SKILL_DIR}/references/driver-sources.md and ${CLAUDE_SKILL_DIR}/references/page-template.md.
> Those files are your instructions.
>
> Repository PX4/PX4-Autopilot, [PR [number], head SHA [sha], base SHA [sha] / local clone at [path], branch [name], merge-base [sha]].
> Mode: [new rangefinder / driver change / page change / index change]. [For every mode but new rangefinder: the areas or lines in scope.]
> Rangefinder facts: [the shared.md rangefinder facts table, filled in].
> Rangefinder facts worksheet: [the driver-sources.md worksheet, filled in once per driver, with file:line for every value].
> Manufacturer facts: [the shared.md manufacturer facts table, filled in, with the document and section for every value, or "not read" and why].
> Comparator pages: [each page, and why it was chosen].
> Files in scope: [rangefinder page, SUMMARY.md, sensor/rangefinders.md, dronecan/index.md or collision_prevention.md if they apply, any other changed docs/en/ page that mentions the rangefinder].
> Driver files (evidence, never review targets): [paths].
>
> Your lens is done only when every rule in your lens file has been applied.
> Verify every finding as shared.md requires, then return one row per finding with the file path, line number, issue, severity, suggestion, and the evidence you checked.
> [Completeness lens: also return the checklist, one row per item, with status and evidence.]
> [Sibling-comparison lens: also return the comparator pages you used.]
> Return anything shared.md sends below the tables (source disagreements, unverified wiring claims, firmware questions, questions for the manufacturer) as separate notes.
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

1. **Rangefinder summary.** One line per rangefinder: page, page kind and models, connections, drivers, role, which configuration keys build the driver and how many boards set them, and the comparator pages used.
   Then the bug count and where the bugs are ("2 bugs in 1 of the 3 changed doc files"; "No bugs in 3 changed doc files"), and the finding total.
2. **Rangefinder documentation checklist**, for a new rangefinder: the completeness checklist as a table, `Item | Status | Evidence`, every item listed.
3. **Issues found**:

   | Issues found | bug | style | minor | total |
   | --- | --- | --- | --- | --- |
   | Matches driver source | | | | |
   | Matches sibling pages | | | | |
   | Template and listings | | | | |

   Rows count the findings of source-consistency, sibling-comparison, and completeness, in that order.
   When there are bugs, list each with its file and line after the table.
4. **Issue summary per file**: `File | bug | style | minor | total`, ordered by bug count, every in-scope file listed.
5. **Detailed review**: one table per file with findings, `Line | Issue | Severity | Suggestion`, sorted by line.
   End each Issue with the template check it fails, in parentheses (`(R-A2)`), when there is one, so the reviewer can look the rule up.
   Keep the Suggestion column to one line; a longer rewrite goes below the tables, keyed to file and line.
   A missing-section finding's Suggestion is "Add the stub below", and the stub goes below the tables (`references/page-template.md`, "Stubs for missing sections").
   A missing-content finding's Line is where the content would go (`references/shared.md`, "Verification").

Below the tables, only these, in this order, each only when it applies:

1. Suggestion blocks too long for the Suggestion column, then the stubs for missing sections, one block per run of adjacent missing sections, in page order
2. Firmware questions the docs can't settle (a driver range limit narrower than the manufacturer's, a model in the parameter the driver doesn't handle, something the manufacturer requires of an integrator that the driver doesn't do), for the reviewer to raise; point to `review-pr` for the driver review itself
3. Questions for the manufacturer: what no source settles and only they can answer (NDAA status, which interface variant is sold by default, whether a newer model or connection works with the driver)
4. Who to ask: the contacts found in Scope, each with the handle, what ties them to this sensor, and how recent that is
5. Comment drafts, when there are firmware questions or manufacturer questions and someone to send them to (see below)
6. Where the sources disagree, including comparators that agree with each other against the template
7. Claims that matter for wiring but couldn't be checked against any source
8. A module-reference anchor that won't exist until the reference is regenerated after merge
9. A single note that the page's prose wasn't reviewed, suggesting `px4-doc-review` (standalone runs only)
10. A single note if the review ran in one context

**Comment drafts.**
A draft is a review comment for the reviewer to post, never one you post.
Each is addressed to one named handle, says which line of the diff it attaches to, and gives the evidence with a link to the source line or the manufacturer section.

- A driver observation that isn't part of this change goes to whoever last worked on that code, opens "FYI only in case you are interested:", and ends by saying no action is needed for this PR.
  The driver file is rarely in a docs diff, so anchor it to the page line it bears on and link the driver line.
- A question for the manufacturer goes to their contact, is anchored to the page or index line it would change, and says what the page will say once it's answered.
- Check the handle against the GitHub profile before writing it; a misspelt handle pings a stranger.

Cite lines as GitHub links with the full head SHA and one line of context each side:
`https://github.com/PX4/PX4-Autopilot/blob/<full-sha>/docs/en/sensor/<page>.md#L12-L16`
For a local-branch run, cite `<path>:<line>` instead.

**In chat by default, in a file when asked.**
A file copy opens with a title line (`# PX4-Autopilot PR <n> — rangefinder docs review: <page>`) and labelled `PR`, `Head SHA`, and `Reviewed` lines, is written outside the clone, and overwrites any earlier copy.
For a local-branch run, offer to open the report in VS Code once it's shown, if `command -v code` finds it: write the file first if it only exists in chat, then run `code <path>`.

#### Handoff to px4-doc-review

When `px4-doc-review` handed off the PR, return:

- the rangefinder summary lines
- the documentation checklist table
- the merged findings, one row per finding, with file, line, issue, severity, suggestion, and evidence
- the below-the-tables notes, including questions, contacts and comment drafts, except the "prose wasn't reviewed" note

`px4-doc-review` places them in its own report under **Rangefinder documentation review**, and handles deduplication against its own lenses.
