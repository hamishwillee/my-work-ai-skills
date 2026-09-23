# Shared rules

Read by every lens, before that lens's own file.
This holds what all lenses share: the read-only rule, what's in scope, the board facts every lens works from, the sources of truth and their precedence, verification, and severity.

## Read-only

You are read-only.
Never modify a file in the repository under review, and never run `gh pr comment`, `gh pr review`, `gh pr edit`, or any other write operation.
The one file you may create is the report itself, and only the main agent does that, only when the reviewer asks for it, and only outside the clone.

## Scope

This skill reviews the **documentation of a flight controller board**: its page under `docs/en/flight_controller/`, and the places that page must be listed.
It does not review the board's firmware.
Board ID uniqueness, USB VID/PID, flash fit, CI build coverage, and copy-pasted driver forks belong to the `review-pr` skill in the PX4-Autopilot repo (`.claude/skills/review-pr/SKILL.md`, "New board") or to `code-review`.
Never raise a finding on a file under `boards/`: those files are evidence, not review targets.

Prose quality (grammar, spelling, heading case, emphasis) belongs to `px4-doc-review`.
When this skill runs inside a `px4-doc-review` review, that skill's lenses already cover the page's prose, so don't raise a grammar or style-guide finding here.
When this skill runs on its own, say so once below the tables and suggest running `px4-doc-review` for prose.

### Files in scope

- The board's page: `docs/en/flight_controller/<page>.md`.
- Its listing entries: `docs/en/SUMMARY.md`, the support-category page that lists it (see Board facts), and `docs/en/_sidebar.md` if the PR edits it.
- Images under `docs/assets/flight_controller/<page-stem>/` referenced by the page (existence and path only; the picture's content isn't reviewed).
- Any other `docs/en/` page the PR changes to mention the board (a quick-start or wiring page, `pixhawk_series.md`, release notes).

## Board facts

The main agent establishes these once in Scope and passes them to every lens, so no two lenses derive them differently.
A lens that finds one of them wrong reports that rather than silently using its own value.

| Fact | How it's established |
| --- | --- |
| **Board directory** | `boards/<vendor>/<board>/`, the directory containing `default.px4board`. A PR can add several variants of one board (`default.px4board` plus `<variant>.px4board`); they share one directory. |
| **Build targets** | `<vendor>_<board>_default` plus one `<vendor>_<board>_<variant>` per other `*.px4board` file in the directory. |
| **Board page** | The page under `docs/en/flight_controller/` whose Building Firmware section names the default build target. For a new board it's normally the one new page in that folder. For an existing board, `grep -l "<vendor>_<board>_default" docs/en/flight_controller/*.md`. |
| **Reference design** | The FMU standard the board implements (`fmu-v5x`, `fmu-v6x`, `fmu-v6c`, `fmu-v6xrt`, ...), or `none`. Evidence, strongest first: the board directory name, the page's own claim ("based on the FMUv6X reference design"), the `description` in `firmware.prototype`, and a close file-level match to `boards/px4/<design>/` (compare `nuttx-config/nsh/defconfig`, `src/board_config.h`, `src/timer_config.cpp`). When the evidence disagrees, record `unclear` and name what disagrees. |
| **Support category** | Which of the category pages lists the board: `autopilot_pixhawk_standard.md`, `autopilot_manufacturer_supported.md`, `autopilot_experimental.md`, or `autopilot_discontinued.md`. A new board from a third-party manufacturer is **manufacturer supported** unless the PR description or maintainers say otherwise; a board listed on none of them is itself a finding (`completeness.md`). |
| **Manufacturer** | The company named in the page's title and its "Contact the [manufacturer]" link. |
| **Comparator pages** | Chosen by `sibling-comparison.md`'s selection rules. The main agent picks them in Scope, so the other lenses can use them too. |

## Sources of truth

Listed in precedence order: a claim backed by a higher source outranks one backed by a lower source.
Where two genuinely contradict each other, report the contradiction instead of picking a winner.

1. **The board's own files in this PR** (`boards/<vendor>/<board>/**` at the head SHA).
   What the firmware configures is what the board does under PX4: the port a driver starts on, the UART a label maps to, the number of PWM outputs.
   A page claim that contradicts them is a `bug`.
   `references/board-sources.md` says which file answers which question, and how to read it.
2. **The PX4 docs' own published requirements**: `docs/en/hardware/board_support_guide.md` (what a board PR must contain) and `docs/en/contribute/docs.md`.
3. **The flight-controller page template** (`references/page-template.md`): this skill's standard for a board page, as numbered checks with a severity each.
   Cite the check ID in a finding's evidence.
4. **Comparator pages**: the reference design's other boards and the support category's recent pages, per `sibling-comparison.md`.
   They show the form the maintainers accept today: disclaimers, listing placement, naming, shared-design wording.
   A comparator can itself be wrong or out of date, so a difference from it is a finding only when the comparators agree with each other.
   Where two or more agree on something the template does differently, report against the template and note the comparators below the tables.
5. **Manufacturer material** the page links (product page, datasheet, pinout PDF), only for claims the page sources there.
6. **The rest of this skill**, last on purpose.

### Reaching the sources

- **PR diff, description, linked issue**: `gh pr view`, `gh pr diff`, `gh api`.
- **Board files and comparator pages**: prefer a local `PX4-Autopilot` clone (check `~/github/PX4/PX4-Autopilot` and siblings first).
  Read the PR's head, not whatever the clone has checked out: `git -C <clone> fetch origin pull/<n>/head` then `git -C <clone> show FETCH_HEAD:<path>`, or `gh api repos/PX4/PX4-Autopilot/contents/<path>?ref=<head-sha>`.
  Comparator pages and `boards/px4/<design>/` come from the base SHA.
- **Vendor material**: `WebFetch` the URL the page links.

## Verification

Every finding needs evidence you actually checked:

- **Against board files**: name the file and line, and quote the setting (`default.px4board:14 CONFIG_BOARD_SERIAL_GPS1="/dev/ttyS0"`).
- **Against comparators**: name at least two comparator pages that agree, with the line in each.
  One comparator on its own is an observation for the notes below the tables, not a finding.
- **Against published requirements**: quote the requirement and name its page.
- **Line numbers**: match the head SHA's file.
  A finding about something *missing* anchors to the line where it would go (the heading it belongs under, or line 1 for a page-level gap) and says so.

A finding that fails verification is dropped, not downgraded.

## Severity

| Severity | Meaning |
| --- | --- |
| `bug` | The reader ends up misinformed or unable to act: a wrong port, pin, output count, or build target; a missing pinout the board support guide requires; a page nobody can reach; a support-category claim that contradicts where the board is listed |
| `style` | The page departs from the form its comparators share, or from the template, but what it says is right |
| `minor` | No rule broken and the comparators don't agree on it; a suggestion the author can decline |

A missing section is `bug` when the board support guide requires its content (pinout, and a block diagram or schematic) or when the reader can't connect the board without it (Radio Control, whose wiring varies board to board), and `style` otherwise.
