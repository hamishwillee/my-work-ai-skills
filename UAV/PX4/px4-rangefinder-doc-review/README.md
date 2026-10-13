# px4-rangefinder-doc-review

A Claude Code skill for reviewing the documentation of a rangefinder (distance sensor) in a [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) pull request.

A rangefinder PR adds a driver under `src/drivers/distance_sensor/<driver>/` and a page under `docs/en/sensor/` (or `docs/en/dronecan/` for a DroneCAN sensor).
The page is mostly a description of things the driver already settles (which parameter enables it, what baud rate it uses, which models it knows, what range it reports), and it should give the reader the same information, in the same order, as every other rangefinder page.
This skill checks:

- **Against a page template**: a skeleton page with standard wording, and numbered checks (`R-O3`, `R-W2`, `R-A1`, ...) covering every section, heading, anchor and required piece of content, each with a severity
- **Against the driver**: enabling parameter and its values, baud rate, I2C address, supported models, range limits, orientation, other parameters, the configuration keys that build it and how many boards set them, commands and topics
- **Against its siblings**: pages for rangefinders with the same connection (serial, I2C, DroneCAN), role and manufacturer — shared steps worded the same way, and text copied from a sibling that's no longer true
- **Against its listings**: `SUMMARY.md`, the table row and summary in `sensor/rangefinders.md`, and the DroneCAN and Collision Prevention pages where they apply

It handles two kinds of page:

- **Single-model** pages, for one rangefinder
- **Family** pages, for several models that share a driver and most of their setup (LightWare SF/LW, TeraRanger Evo, TFmini): the same skeleton plus a Supported Models table, with shared content written once and every per-model difference stated

It doesn't review the page's prose (that's [px4-doc-review](../px4-doc-review)), the driver's parameter descriptions ([px4-param-review](../px4-param-review)), or the driver code (that's `review-pr` in the PX4-Autopilot repo, or `code-review`).

`px4-doc-review` hands rangefinder PRs to this skill and includes its findings in its own report, the same way it hands boards to [px4-board-doc-review](../px4-board-doc-review), which this skill is modelled on.
You can also run it on its own.

It can also **update** an existing page: after a review, it works down the page in template order, researches each section from the driver and the manufacturer's manual, and proposes one change at a time with its evidence, applying each only when you approve it.
It can draw replacement wiring diagrams and run a live preview of the page.
Along the way it collects questions for the manufacturer, people who could review the page, and draft comments for you to post.

## Skill structure

```
px4-rangefinder-doc-review/
├── SKILL.md                        # the main agent's instructions: scope, dispatch, report
├── references/
│   ├── shared.md                   # read by every lens: read-only rule, scope, rangefinder facts, sources, severity
│   ├── driver-sources.md           # facts worksheet; which driver file answers which claim; firmware keys; driver-to-page map
│   ├── page-template.md            # page kinds, skeleton with standard wording, every numbered check
│   ├── source-consistency.md       # lens: page claims vs driver source
│   ├── sibling-comparison.md       # lens: page vs connection, role and manufacturer siblings
│   ├── completeness.md             # lens: template presence/form checks, documentation checklist, listings
│   └── page-update.md              # updating an existing page, one approved suggestion at a time
├── preferences.example.md          # boilerplate to copy to ~/.config/px4-rangefinder-doc-review/preferences.md
└── README.md                       # this file
```

## Sources of truth

In precedence order, from `references/shared.md`:

1. The driver source in the PR
2. The PX4 docs' shared pages (`sensor/rangefinders.md`, `peripherals/serial_configuration.md`, `dronecan/index.md`)
3. The page template (`references/page-template.md`)
4. Comparator pages, when at least two agree
5. Manufacturer material the page links
6. The rest of this skill

## Installing

Symlink the skill into Claude Code's skills directory:

```bash
ln -s ~/github/hamishwillee/my-work-ai-skills/UAV/PX4/px4-rangefinder-doc-review ~/.claude/skills/px4-rangefinder-doc-review
```

Optionally copy the preferences file:

```bash
mkdir -p ~/.config/px4-rangefinder-doc-review
cp ~/.claude/skills/px4-rangefinder-doc-review/preferences.example.md ~/.config/px4-rangefinder-doc-review/preferences.md
```

## Requirements

- **`gh` CLI**, authenticated.
- **A local clone of `PX4-Autopilot`**, strongly recommended: the review reads driver files and comparator pages, which is slow over the API.
- **A way to read PDFs**, for manufacturer manuals: `pdftotext` (poppler-utils), or Python with `venv` so `pypdf` can be installed in a scratch directory.

## Using

```
/px4-rangefinder-doc-review <PR number>
```

With no PR, it offers **Enter PR**, **Local branch** or **Existing page**; a local-branch run diffs your working tree against the default branch.

To update a page rather than review it, ask for that: "update `sensor/<page>.md` to the template".

## Output

1. **Rangefinder summary**: page, kind and models, connections, drivers, role, firmware support, and the comparator pages used; bug and finding counts.
2. **Rangefinder documentation checklist**: each thing a reader needs, with `yes` / `no` / `partial` / `n/a` and evidence.
3. **Issues found**, by area: matches driver source, matches sibling pages, template and listings.
4. **Issue summary per file** and **Detailed review**, one row per issue with line, severity, the template check it fails, and suggested fix.
5. Below the tables: stubs for missing sections, firmware questions, questions for the manufacturer, who to ask, and draft comments to post.

| Severity | Meaning |
| --- | --- |
| `bug` | Misinforms the reader or blocks them: a wrong parameter, baud rate or range, a model the driver doesn't support, no pinout, a driver that isn't in firmware with nothing saying so, an unreachable page, placeholder text |
| `style` | Departs from the template or from the form its siblings share, but what it says is right |
| `minor` | A suggestion the author can decline |
