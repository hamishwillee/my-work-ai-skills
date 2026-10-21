# Project conventions

## Line breaks in markdown

Use semantic (sentence) line breaks in every markdown file in this repo, not fixed-width hard wraps.
Break after each sentence, not at an arbitrary column — a paragraph is one sentence per line, not one 80-character line wrapped mid-sentence.
This makes diffs land on the sentence that actually changed instead of reflowing the whole paragraph.

Exceptions: table rows and YAML frontmatter values stay on one line each (markdown tables and YAML don't tolerate a mid-cell break), and fenced code blocks are left exactly as their source formats them.

## Editing this skill

- This skill is modelled on `../px4-rangefinder-doc-review`, which is modelled on `../px4-board-doc-review`: the same Scope → Dispatch → Report shape, the same three lenses, the same report, the same update mode.
  A change to how any of them orchestrates or reports is usually worth making in all three.
- `SKILL.md` orchestrates; `references/*.md` hold the rules each lens applies.
  Changing what a lens checks usually means updating both the lens file and, if the lens's inputs change, the Dispatch prompt in `SKILL.md`.
- GNSS facts, the facts worksheet and comparator pages are established once, by the main agent, in Scope, and passed to every lens.
  Don't move that work into a lens: three lenses deriving the protocol or its detection independently will disagree.
- Headings that mean the same as one on a flight-controller or rangefinder page use the same heading and anchor (`page-template.md`, "In common with other hardware pages").
  When any of the three templates renames one, change all of them.
- `references/page-template.md` is the standard: the skeleton, its standard wording, and every numbered check live there, and nowhere else.
  A lens file says which half of a check it owns (completeness: present and well-formed; source-consistency: correct) but never restates the check.
  Check IDs are cited in reports, so don't renumber an existing check; add new ones at the end of their section, and retire an old one by deleting it rather than reusing its ID.
- `references/protocol-sources.md` holds the reading knowledge: which file settles which claim, the protocol table, the counts, the receiver-to-page map and the exemplars.
  The protocol enum, the auto-detect list, the Kconfig defaults and the board counts go stale: re-read them from the source they cite when the GPS driver or its submodule changes, and update the "as of" line.
- The protocol is the first thing to get right.
  The skill came out of a review (PX4-Autopilot PR 28969, GlobalSat BD-100M/K) where the vendor's page linked only to a manual written for ArduPilot, and the receivers speak NMEA, which PX4 never auto-detects; the survey of existing pages then found the same mistake on two DATAGNSS pages.
  Keep "plug and play" tied to the detection rules in `protocol-sources.md`.
- Heading is the second.
  The survey found four DroneCAN pages telling readers to enable heading fusion on single-antenna receivers; keep the heading checks tied to what the protocol actually publishes.
- The sibling-comparison lens needs two agreeing comparators before a difference is a finding.
  Keep that rule: many GNSS pages are out of date, and copy-paste drift between siblings is common.
- `existing-page-issues.md` is a work list, not a source: no lens reads it and nothing in it is evidence.
  Its claims came from one survey and haven't all been verified; verify before acting on one, and delete an item once it's fixed upstream.
- Review is read-only; `references/page-update.md` is the only place that edits the clone, and only approved changes.
- Manufacturer facts and contacts, like the source facts, are gathered once in Scope.
  A manufacturer manual written for another autopilot is evidence about the hardware, never about PX4 configuration.
- Nothing unproven goes onto a page (`shared.md`), including receiver, compass and barometer part numbers in the device tables.
- This skill never reviews prose and never raises a finding on a file under `src/`, `boards/` or `ROMFS/`.
  Prose belongs to `px4-doc-review`, parameter descriptions to `px4-param-review`, driver code to `review-pr` in the PX4-Autopilot repo.
