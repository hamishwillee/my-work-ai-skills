# Project conventions

## Line breaks in markdown

Use semantic (sentence) line breaks in every markdown file in this repo, not fixed-width hard wraps.
Break after each sentence, not at an arbitrary column — a paragraph is one sentence per line, not one 80-character line wrapped mid-sentence.
This makes diffs land on the sentence that actually changed instead of reflowing the whole paragraph.

Exceptions: table rows and YAML frontmatter values stay on one line each (markdown tables and YAML don't tolerate a mid-cell break), and fenced code blocks are left exactly as their source formats them.

## Editing this skill

- This skill is modelled on `../px4-board-doc-review`: the same Scope → Dispatch → Report shape, the same three lenses, the same report.
  A change to how either skill orchestrates or reports is usually worth making in both.
- `SKILL.md` orchestrates; `references/*.md` hold the rules each lens applies.
  Changing what a lens checks usually means updating both the lens file and, if the lens's inputs change, the Dispatch prompt in `SKILL.md`.
- Rangefinder facts and comparator pages are established once, by the main agent, in Scope, and passed to every lens.
  Don't move that work into a lens: three lenses deriving the driver or the model list independently will disagree.
- Headings that mean the same as one on a flight-controller page use the board template's heading and anchor (`page-template.md`, "In common with flight-controller pages").
  When either template renames one, change both.
- `references/page-template.md` is the standard: the skeleton, its standard wording, and every numbered check live there, and nowhere else.
  A lens file says which half of a check it owns (completeness: present and well-formed; source-consistency: correct) but never restates the check.
  Check IDs are cited in reports, so don't renumber an existing check; add new ones at the end of their section, and retire an old one by deleting it rather than reusing its ID.
- The template serves two page kinds, single-model and family.
  Keep family-only rules in "Family pages" (`R-M...`) so a single-model review can skip them whole, and keep everything else written so it's true for both.
- `references/driver-sources.md` holds the reading knowledge (which file settles which claim, the firmware keys and common-set list, the driver-to-page map).
  The `COMMON_DISTANCE_SENSOR` list and the driver map go stale: update them from the source they cite when a driver is added.
- The sibling-comparison lens needs two agreeing comparators before a difference is a finding.
  Keep that rule: one sibling is often the out-of-date one, and every existing rangefinder page predates the template.
- Review is read-only; `references/page-update.md` is the only place that edits the clone, and only approved changes.
  Keep the two apart: a lens never edits, and the update mode never applies anything the reviewer hasn't seen.
- Manufacturer facts and contacts, like the driver facts, are gathered once in Scope.
  The lenses were unable to verify wiring on the first real run because nobody had read the manual; don't let a lens be the first to open it.
- Nothing unproven goes onto a page, and a discontinued product gets no manufacturer questions (`shared.md`).
  Both came from the reviewer during the TeraRanger update; don't soften them into "ask the reviewer".
- Wording of shared steps belongs to sibling-comparison, presence to completeness.
  When both report the same line, tighten that boundary rather than relying on the merge.
- This skill never reviews prose and never raises a finding on a file under `src/`, `boards/` or `ROMFS/`.
  Prose belongs to `px4-doc-review`, parameter descriptions to `px4-param-review`, driver code to `review-pr` in the PX4-Autopilot repo.
