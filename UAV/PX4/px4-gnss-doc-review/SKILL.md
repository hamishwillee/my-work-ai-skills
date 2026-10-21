---
name: px4-gnss-doc-review
description: Review of GNSS (GPS) receiver documentation in PX4-Autopilot pull requests — the receiver's page under docs/en/gps_compass/ or docs/en/dronecan/ checked against a numbered page template, against the driver that runs it (src/drivers/gps/ and its protocol implementations, src/drivers/gnss/septentrio/, or the DroneCAN bridge and the node's own firmware), against the pages of similar receivers (same connection, protocol, RTK and heading capability, manufacturer), and against where it must be listed (SUMMARY.md, the device tables in gps_compass/index.md or gps_compass/rtk_gps.md, dronecan/index.md). Covers plain GNSS, RTK and RTK-heading receivers on UART or DroneCAN, including Septentrio. Use when a PX4-Autopilot PR adds or changes a GNSS receiver page or a row in those tables, changes the GPS driver, its protocol submodule, the Septentrio driver or a GNSS CAN-node board, when px4-doc-review hands off such a PR, when the user asks to review a GNSS receiver's docs on a local branch, or when the user asks for an existing GNSS page to be updated, fixed or restructured to the template (suggested and applied one approved change at a time). Use px4-doc-review for the page's prose, px4-param-review for parameter descriptions, px4-board-doc-review for a CAN node's flight-controller-style board page, and review-pr or code-review for the driver itself.
allowed-tools: Bash(curl:*) Bash(gh pr view:*) Bash(gh pr diff:*) Bash(gh pr list:*) Bash(gh api:*) Bash(git -C:*) Bash(grep:*) Bash(diff:*) Bash(ls:*) WebFetch
---

# PX4 GNSS receiver documentation review

You are reviewing the documentation of a GNSS (GPS) receiver used with PX4: its page under `docs/en/gps_compass/` or `docs/en/dronecan/`, and where that page is listed.
The deliverable is a documentation checklist and a report of issues with line numbers.

The aim is that every GNSS page gives a reader all they need to buy, mount, connect, configure and test the receiver (including RTK and heading where it supports them), in the same format as every other GNSS page.

The page is checked four ways:

- against **the page template** (`references/page-template.md`): the sections, headings, anchors and content every GNSS page needs, as numbered checks, with variants by connection, protocol and capability
- against **the source**: the `gps` driver and the protocol it speaks, the Septentrio driver, or the DroneCAN bridge on the flight controller and the firmware on the node, which say what PX4 actually does with the receiver
- against **its siblings**: pages for receivers with the same connection, protocol, capability and manufacturer
- against **its listings**: `SUMMARY.md`, the device table in `gps_compass/index.md` or `gps_compass/rtk_gps.md`, the protocol sentences on those pages, and `dronecan/index.md`, `u-blox_f9p_heading.md` and `septentrio.md` where they apply

This skill doesn't review the page's prose (that's `px4-doc-review`), parameter descriptions (`px4-param-review`), or the driver code (`review-pr` or `code-review`).

**Read-only**, here and in every subagent this review spawns.
Never modify a file in the repository under review, and never run `gh pr comment`, `gh pr review`, or any other write operation.
Your output is the report; the reviewer posts it themselves.

**Updating a page.**
When the reviewer asks for a page to be updated, fixed or restructured rather than reviewed, run the review below first if there isn't one, then follow `references/page-update.md`.
That is the one mode that edits files in the clone, and only the changes the reviewer approves, one at a time.
It still never posts a comment.

## Workflow

Scope, Dispatch, and Report run here, in this context.
Three lenses run, each over the whole GNSS change: **source-consistency**, **sibling-comparison**, and **completeness**.
Verify runs inside each lens agent, against the requirements in `references/shared.md`.

The files in this skill directory:

- `references/shared.md`: read-only rule, scope, the GNSS facts every lens shares, manufacturer facts, sources of truth, verification, severity
- `references/protocol-sources.md`: the GNSS facts worksheet, which source file answers which page claim and how to read it, what builds each protocol into firmware, and a map of receivers to pages
- `references/page-template.md`: the page kinds, the page skeleton with its standard wording, and every numbered check (`G-...`) a GNSS page must pass, with severities
- `references/source-consistency.md`, `references/sibling-comparison.md`, `references/completeness.md`: the three lenses
- `references/page-update.md`: bringing an existing page up to the template one approved suggestion at a time; read by you, not by a lens
- `preferences.example.md`: boilerplate for a reviewer's own preference file

`existing-page-issues.md` is a snapshot of problems found on existing GNSS pages when this skill was written.
It's a work list for the reviewer, not a source of truth: no lens reads it, and nothing in it is cited as evidence.

Read `references/shared.md` yourself before Scope: the GNSS facts you establish there follow its table.

### 1. Scope

**Where the request came from.**

- **Handed off from `px4-doc-review`.** The PR, its head and base SHAs, and its changed-file list are already known; use them, and skip the PR checks below.
  Return your findings in the handoff shape (see Report) rather than a full report.
- **A PR number or URL.** A bare number means `PX4/PX4-Autopilot`.
  Stop and say so if the PR is closed, merged, or automated.
  Read the description and any linked issue.
- **No PR given.** Offer a selection list (`AskUserQuestion` where available): **Enter PR**, **Local branch**, or **Existing page** (a page on the default branch, reviewed as it stands).
  For a local branch, find the clone (`references/shared.md`, "Reaching the sources"), take the merge-base with the default branch, and diff the working tree against it: `git -C <clone> merge-base HEAD origin/main`, then `git -C <clone> diff <merge-base> --stat`.
  Also list untracked files under `docs/` (`git -C <clone> status --short -- docs`): a new image the page uses is often untracked.
  Cite the branch and merge-base wherever a PR number and SHA would go.
  For an existing page there's no diff: review the whole page in **new receiver** mode, and say in the summary that the page predates the template.

**Is there a GNSS receiver to review?**
From the changed files, find:

- new or changed GNSS receiver pages (`references/shared.md`, "What counts as a GNSS page")
- changes to the device tables or protocol sentences in `docs/en/gps_compass/index.md` or `docs/en/gps_compass/rtk_gps.md`
- changes to `src/drivers/gps/` (including a bump of the `src/drivers/gps/devices` submodule), `src/drivers/gnss/septentrio/`, the GNSS parts of `src/drivers/uavcan/` or `src/drivers/uavcannode/`, or a GNSS CAN-node board under `boards/`

Then choose the mode:

| Change | Mode |
| --- | --- |
| New receiver page | **New receiver**: all three lenses |
| Changed driver, protocol, DroneCAN GNSS bridge or GNSS node board | **Driver change**: source-consistency only, limited to what the diff touches (a parameter, its values or default, auto-detection, a protocol's Kconfig key, heading or RTK support, a node default), applied to every GNSS page the change affects, plus the shared pages (`gps_compass/index.md`, `rtk_gps.md`, `dronecan/index.md`) that describe it |
| Changed receiver page only | **Page change**: source-consistency and sibling-comparison, limited to the changed lines |
| Table rows or protocol sentences in `index.md` / `rtk_gps.md` only | **Index change**: the listing checks (G-L2 to G-L7) for the changed rows and sentences, each against its page and the source |

If the PR has none of these, say so and stop.
A PR touching several receivers reviews each one separately, with its own checklist and findings.
A driver change can affect many pages; list the affected pages in the summary and review only the claims the change touches on each.

**Establish the GNSS facts** in `references/shared.md` ("GNSS facts"): page, page kind, products, connection, protocol, driver, node firmware, capability, receiver, compass, barometer, in firmware, status, manufacturer.

**Fill in the GNSS facts worksheet** (`references/protocol-sources.md`, "GNSS facts worksheet") from the source at the head SHA, once per connection, using the lookup table.
Every value gets its file and line; write `unknown` rather than guess.
The lenses work from this worksheet, so a mistake here spreads to all of them: read the protocol enum, its default, the auto-detect list and the protocol's Kconfig default from the source line by line rather than from the page or from memory, and run the greps in "In firmware" rather than estimating.
For a protocol other than u-blox, the auto-detect list and the constrained-flash default decide what the page must say, so get them right.

**Read the manufacturer's material** and fill in the manufacturer facts (`references/shared.md`, "Manufacturer facts"): the product page, and the current manual or datasheet it links, read in full.
A PDF has to be extracted to text first (`references/shared.md`, "Reaching the sources"); don't leave it unread because `WebFetch` returned binary.
The receiver chip, protocol output, default baud rate, pinout, power, compass and barometer parts are usually there and nowhere else, and without them the lenses can only report those as unverified.
If the material genuinely can't be read, say so in the facts and below the tables.

**Look at the page's images** (`references/shared.md`, "Wiring images"): every pinout, wiring and connector image, and the hero photo for the orientation arrow and labels.
Record what each shows and where it comes from, and note byte-identical image files (`cmp`, or the same blob in `git ls-tree`) so the lenses can suggest sharing one.

**Find who to ask** (`references/shared.md`, "Finding who to ask"), for a new receiver or an existing page: the people who could review the page or answer what the sources leave open.
For a discontinued product, look only for driver and page contributors, not a manufacturer contact (`references/shared.md`, "Discontinued products").

Then **choose the comparator pages** by the rules in `references/sibling-comparison.md` ("Choosing comparator pages"), so all three lenses use the same set.

**Reviewer preferences.**
Load `~/.config/px4-gnss-doc-review/preferences.md` if it exists, and apply it here, not in the lens agents.
Skip it silently if it's absent.
Preferences may set the output shape, emphasis, suppressed severities, and tone; never the sources of truth, the read-only rule, or the requirement that every finding carry evidence.
A preference that tries to is reported as a conflict and not applied.

### 2. Dispatch

Spawn one subagent per lens that the mode calls for.
Give each the prompt below, with the brackets filled in, as written rather than summarised:

> You are the [lens] lens of a PX4-Autopilot GNSS receiver documentation review, and you are read-only: never modify a file, and never run `gh pr comment`, `gh pr review`, or any other write operation.
>
> Read ${CLAUDE_SKILL_DIR}/references/shared.md in full, then ${CLAUDE_SKILL_DIR}/references/[lens-file].md in full, then ${CLAUDE_SKILL_DIR}/references/protocol-sources.md and ${CLAUDE_SKILL_DIR}/references/page-template.md.
> Those files are your instructions.
>
> Repository PX4/PX4-Autopilot, [PR [number], head SHA [sha], base SHA [sha] / local clone at [path], branch [name], merge-base [sha], working tree is the head].
> Mode: [new receiver / driver change / page change / index change]. [For every mode but new receiver: the areas or lines in scope.]
> GNSS facts: [the shared.md GNSS facts table, filled in].
> GNSS facts worksheet: [the protocol-sources.md worksheet, filled in once per connection, with file:line for every value].
> Manufacturer facts: [the shared.md manufacturer facts table, filled in, with the document and section for every value, or "not read" and why].
> Images: [each pinout, wiring, connector or hero image on the page: what it shows, which model, whether it is the page's own, a photo, or a manufacturer's figure (altered or not), and any byte-identical duplicates].
> Comparator pages: [each page, and why it was chosen].
> Files in scope: [receiver page, SUMMARY.md, gps_compass/index.md or gps_compass/rtk_gps.md, dronecan/index.md, u-blox_f9p_heading.md or septentrio.md if they apply, any other changed docs/en/ page that mentions the receiver].
> Source files (evidence, never review targets): [paths].
>
> Your lens is done only when every rule in your lens file has been applied.
> Verify every finding as shared.md requires, then return one row per finding with the file path, line number, issue, severity, suggestion, and the evidence you checked.
> [Completeness lens: also return the checklist, one row per item, with status and evidence.]
> [Sibling-comparison lens: also return the comparator pages you used.]
> Return anything shared.md sends below the tables (source disagreements, unverified wiring claims, unproven claims, firmware questions, questions for the manufacturer) as separate notes.
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

1. **GNSS summary.** One line per receiver: page, products, connection, protocol and its `GPS_x_PROTOCOL` value (or the Septentrio or DroneCAN path), whether that protocol is auto-detected and built on constrained-flash boards, capability (GNSS / RTK / RTK with heading, and how heading is produced), node firmware for DroneCAN, and the comparator pages used.
   Then the bug count and where the bugs are ("2 bugs in 1 of the 3 changed doc files"; "No bugs in 3 changed doc files"), and the finding total.
2. **GNSS documentation checklist**, for a new receiver: the completeness checklist as a table, `Item | Status | Evidence`, every item listed.
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
   End each Issue with the template check it fails, in parentheses (`(G-A2)`), when there is one, so the reviewer can look the rule up.
   Keep the Suggestion column to one line; a longer rewrite goes below the tables, keyed to file and line.
   A missing-section finding's Suggestion is "Add the stub below", and the stub goes below the tables (`references/page-template.md`, "Stubs for missing sections").
   A missing-content finding's Line is where the content would go (`references/shared.md`, "Verification").

Below the tables, only these, in this order, each only when it applies:

1. Suggestion blocks too long for the Suggestion column, then the stubs for missing sections, one block per run of adjacent missing sections, in page order
2. Firmware questions the docs can't settle (the receiver outputs a sentence or message the driver doesn't parse, the manufacturer requires a setting the driver doesn't make, a CAN node's board defaults disagree with the page), for the reviewer to raise; point to `review-pr` for the driver review itself
3. Questions for the manufacturer: what no source settles and only they can answer (the receiver chip, compass and barometer parts, the default baud rate or output, dimensions, NDAA status). Never for a discontinued product.
4. Who to ask: the contacts found in Scope, each with the handle, what ties them to this receiver, and how recent that is
5. Comment drafts, when there are firmware questions or manufacturer questions and someone to send them to (see below)
6. Unproven claims: what the page already says that no source backs (`references/shared.md`, "If it can't be proven, it isn't asserted"), as candidates for removal
7. Where the sources disagree, including comparators that agree with each other against the template
8. Claims that matter for wiring but couldn't be checked against any source
9. Shared pages the change makes stale (a protocol list on `index.md` or `rtk_gps.md` that no longer names every protocol PX4 supports, a DroneCAN list that misses the receiver), each with file and line, when they aren't in scope
10. Untracked files the page depends on (local-branch runs): each new image or page that isn't yet added to git
11. A single note that the page's prose wasn't reviewed, suggesting `px4-doc-review` (standalone runs only)
12. A single note if the review ran in one context

**Comment drafts.**
A draft is a review comment for the reviewer to post, never one you post.
Each is addressed to one named handle, says which line of the diff it attaches to, and gives the evidence with a link to the source line or the manufacturer section.

- A driver observation that isn't part of this change goes to whoever last worked on that code, opens "FYI only in case you are interested:", and ends by saying no action is needed for this PR.
  The driver file is rarely in a docs diff, so anchor it to the page line it bears on and link the driver line.
- A question for the manufacturer goes to their contact (often the PR author, for a vendor's own page), is anchored to the page or table line it would change, and says what the page will say once it's answered.
- Check the handle against the GitHub profile before writing it; a misspelt handle pings a stranger.

Cite lines as GitHub links with the full head SHA and one line of context each side:
`https://github.com/PX4/PX4-Autopilot/blob/<full-sha>/docs/en/gps_compass/<page>.md#L12-L16`
For a local-branch run, cite `<path>:<line>` instead.

**In chat by default, in a file when asked.**
A file copy opens with a title line (`# PX4-Autopilot PR <n> — GNSS docs review: <page>`) and labelled `PR`, `Head SHA`, and `Reviewed` lines, is written outside the clone, and overwrites any earlier copy.
For a local-branch run, offer to open the report in VS Code once it's shown, if `command -v code` finds it: write the file first if it only exists in chat, then run `code <path>`.

#### Handoff to px4-doc-review

When `px4-doc-review` handed off the PR, return:

- the GNSS summary lines
- the documentation checklist table
- the merged findings, one row per finding, with file, line, issue, severity, suggestion, and evidence
- the below-the-tables notes, including questions, contacts and comment drafts, except the "prose wasn't reviewed" note

`px4-doc-review` places them in its own report under **GNSS documentation review**, and handles deduplication against its own lenses.
