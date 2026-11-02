# Final pass: consistency and context

Run once, after every lens has returned, the link check has run, and the main agent has merged their findings (`SKILL.md`, "Final pass").
Also run it over the edited files whenever changes are applied rather than only reported: link fixes in a standalone link check, or suggestions the reviewer asks to have applied and committed.

The lenses check changed lines one at a time.
This pass checks what they can't see from a single line: whether each change was made everywhere it needed to be, in the same way, and whether the page still reads as one document with the changes in place.
It covers both the PR's own changes and the review's suggested fixes, since a fix that is right for its line can still leave the page inconsistent.

Read every changed `docs/en/` file in full at the head SHA, not only its diff.
Run the two checks in order.

## 1. Changes applied consistently

**The PR's changes.**
From the diff, list each kind of change the PR makes, for example:

- a term, product, parameter, port or command renamed
- a value, unit or default changed
- a heading, anchor or link target changed
- a convention applied, such as port labels put in code style, a space added between number and unit, or a spelling corrected

For each one, find the other places it applies and check they got the same change:

- the rest of the same file
- the PR's other changed files
- for a rename, a changed value, or a changed anchor, the rest of `docs/en/` (`grep -rn` for the old form)

Report an instance that was missed or changed differently.
An old value or name left beside the new one is `bug` when the two now contradict each other (two different defaults for one parameter, two names for one port that read as two ports); otherwise it is `style`.
A missed instance on a page the PR doesn't change goes below the report's tables as a stale page (`SKILL.md`, "What goes below the tables", item 3), not into the per-file tables.

**The review's own suggestions.**
Check the merged findings as a set:

- The same problem on several lines has a row for each line, or one row that names every line it applies to.
- The same problem gets the same fix everywhere: two rows must not suggest different spellings, labels, units or wordings for one thing.
- No two suggestions conflict: one row must not rename a heading or anchor that another row's suggestion links to by its old name, or reword a sentence another row also rewrites differently.
- A suggestion that changes a term, value, heading or anchor names the other places that must change with it.

Return a missing instance as a new finding, and a conflict or inconsistency as a correction to the rows involved, giving the row's file and line and the consistent fix.

## 2. Reads through in context

Read each changed file from top to bottom as the reader will see it, with the PR's changes and the review's suggestions in place, and check that it still works as a whole:

- **References within the page** still hold: "above", "below", "the following", "as in step 3", step and list numbering, and counts ("both ports", "the three outputs").
- **Links to headings on the page** still resolve after any heading or anchor change.
- **No contradiction or repetition**: changed text doesn't state a fact differently from elsewhere on the page, or repeat a section that already exists.
- **Names and voice** match the rest of the page: the changed text uses the page's established names for things, and steps stay in the imperative.
- **Order makes sense**: a step doesn't come before the thing it depends on, a paragraph isn't left without the introduction it relied on, and no heading is left without content.
- **Introductions and summaries** that describe the page's contents still match them.

Severity: `bug` when the reader is misled or a step no longer works (a stale "step 3", two values that contradict each other, a link to a heading that no longer exists).
`style` for inconsistent naming or an order that departs from the page's own pattern.
`minor` for a flow preference the author can decline.

A problem the read-through turns up that the PR didn't cause goes in the pre-existing issues below the tables, not in the findings.

## Return shape

Return new findings in the same shape as the lenses: file path, line, issue, severity, suggestion, and evidence (the other lines or files involved).
Return corrections to existing rows separately, each naming the row by file and line and saying what to change.
If you find nothing, say so rather than returning prose.

## What this pass doesn't cover

It doesn't repeat the lenses' line-by-line checks of grammar, style, structure or accuracy.
It only checks consistency across changes and how the changes fit their page.
