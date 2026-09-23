# Project conventions

## Line breaks in markdown

Use semantic (sentence) line breaks in every markdown file in this repo, not fixed-width hard wraps.
Break after each sentence, not at an arbitrary column — a paragraph is one sentence per line, not one 80-character line wrapped mid-sentence.
This makes diffs land on the sentence that actually changed instead of reflowing the whole paragraph.

Exceptions: table rows and YAML frontmatter values stay on one line each (markdown tables and YAML don't tolerate a mid-cell break), and fenced code blocks are left exactly as their source formats them.

## Editing this skill

- `SKILL.md` orchestrates (Scope → Dispatch → Report); `references/*.md` hold the rules each lens applies.
  Changing what a lens checks usually means updating both the lens file and, if the lens's inputs change, the Dispatch prompt in `SKILL.md`.
- Board facts and comparator pages are established once, by the main agent, in Scope, and passed to every lens.
  Don't move that work into a lens: three lenses deriving the reference design or picking comparators independently will disagree.
- `references/page-template.md` is the standard: the skeleton and every numbered check live there, and nowhere else.
  A lens file says which half of a check it owns (completeness: present and well-formed; source-consistency: correct) but never restates the check.
  Check IDs are cited in reports, so don't renumber an existing check; add new ones at the end of their section, and retire an old one by deleting it rather than reusing its ID.
- `references/board-sources.md` holds the reading knowledge (processor specs, UART order, DShot by chip family).
  When PX4 adds a chip family or changes DShot support, update those tables from the platform source they cite.
- The sibling-comparison lens needs two agreeing comparators before a difference is a finding.
  Keep that rule: one sibling is often the out-of-date one.
- This skill never reviews prose and never raises a finding on a file under `boards/`.
  Prose belongs to `px4-doc-review`, firmware to `review-pr` in the PX4-Autopilot repo.
