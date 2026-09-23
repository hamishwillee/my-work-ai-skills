# px4-board-doc-review

A Claude Code skill for reviewing the documentation of a flight-controller board in a [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) pull request.

A board PR adds a firmware target under `boards/<vendor>/<board>/` and a page under `docs/en/flight_controller/`.
The page is mostly a description of settings that already exist in the board's files (which UART is `TELEM1`, how many outputs there are, which sensors start), and it should look like the pages of the boards it's most like.
This skill checks:

- **Against a page template**: a skeleton page and numbered checks (`T-P1`, `T-RC5`, ...) covering every section, heading, anchor and required piece of content, each with a severity
- **Against the board's source**: serial port mapping, output counts and DShot groups, sensors, processor, power monitoring, console port, and build targets, checked against the files that configure them
- **Against its siblings**: pages for boards on the same reference design (every FMUv6X board, say), in the same support category, and from the same manufacturer — disclaimers, listing placement, section set, and whether a paragraph copied from a sibling is still true for this board
- **Against the board support guide**: pinout, block diagram or schematic, flight logs in the PR description, navigation and category listings
- **Radio Control, always**: RC wiring varies board to board, so every page needs a `### Radio Control {#radio_control}` section under Assembly, saying whether RC goes to the FMU, the PX4IO or both, what the wiring rules out, and which protocols are built in and enabled by default, all checked against the board's source

It doesn't review the page's prose (that's [px4-doc-review](../px4-doc-review)) or the board firmware itself (that's `review-pr` in the PX4-Autopilot repo, or `code-review`).

`px4-doc-review` hands board PRs to this skill and includes its findings in its own report, the same way it hands `.msg` files to [px4-uorb-review](../px4-uorb-review).
You can also run it on its own.

## Skill structure

```
px4-board-doc-review/
├── SKILL.md                        # the main agent's instructions: scope, dispatch, report
├── references/
│   ├── shared.md                   # read by every lens: read-only rule, scope, board facts, sources, severity
│   ├── board-sources.md            # board facts worksheet; which board file answers which claim; processors, UART order, DShot by chip
│   ├── page-template.md            # page skeleton and every numbered check, with severities
│   ├── source-consistency.md       # lens: page claims vs board files
│   ├── sibling-comparison.md       # lens: page vs reference-design, category, and manufacturer siblings
│   └── completeness.md             # lens: template presence/form checks and board support guide requirements
├── preferences.example.md          # boilerplate to copy to ~/.config/px4-board-doc-review/preferences.md
└── README.md                       # this file
```

## Sources of truth

In precedence order, from `references/shared.md`:

1. The board's own files in the PR
2. The PX4 docs' published requirements (`hardware/board_support_guide.md`, `contribute/docs.md`)
3. The page template (`references/page-template.md`)
4. Comparator pages, when at least two agree
5. Manufacturer material the page links
6. The rest of this skill

## Installing

Symlink the skill into Claude Code's skills directory:

```bash
ln -s ~/github/hamishwillee/my-work-ai-skills/UAV/PX4/px4-board-doc-review ~/.claude/skills/px4-board-doc-review
```

Optionally copy the preferences file:

```bash
mkdir -p ~/.config/px4-board-doc-review
cp ~/.claude/skills/px4-board-doc-review/preferences.example.md ~/.config/px4-board-doc-review/preferences.md
```

## Requirements

- **`gh` CLI**, authenticated.
- **A local clone of `PX4-Autopilot`**, strongly recommended: the review reads many board files and comparator pages, which is slow over the API.

## Using

```
/px4-board-doc-review <PR number>
```

With no PR, it offers **Enter PR** or **Local branch**; a local-branch run diffs your working tree against the default branch.

## Output

1. **Board summary**: board directory, page, reference design, support category, and the comparator pages used; bug and finding counts.
2. **Board submission checklist**: each documentation requirement with `yes` / `no` / `partial` and evidence.
3. **Issues found**, by area: matches board source, matches sibling pages, template and submission requirements.
4. **Issue summary per file** and **Detailed review**, one row per issue with line, severity, the template check it fails, and suggested fix.

| Severity | Meaning |
| --- | --- |
| `bug` | Misinforms the reader or blocks them: a wrong port or output count, a missing required pinout, an unreachable page, a category note that contradicts the listing |
| `style` | Departs from the form its siblings share, or from the template, but what it says is right |
| `minor` | A suggestion the author can decline |
