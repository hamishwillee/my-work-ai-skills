# px4-gnss-doc-review

A Claude Code skill for reviewing the documentation of a GNSS (GPS) receiver in a [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) pull request.

A GNSS PR usually adds a page under `docs/en/gps_compass/` (or `docs/en/dronecan/` for a DroneCAN receiver), a row in the device table on `gps_compass/index.md` or `gps_compass/rtk_gps.md`, and an entry in `SUMMARY.md`.
Most of what the page says is settled by PX4's source: which protocol value to set, whether PX4 finds the receiver by itself, whether RTK corrections reach it, whether it can provide heading, what a DroneCAN node needs.
Vendor pages often get exactly these things wrong, typically by copying a sibling page or linking a manual written for another autopilot.
This skill checks:

- **Against a page template**: a skeleton page with standard wording, and numbered checks (`G-O3`, `G-A1`, `G-L2`, ...) covering every section, heading, anchor and required piece of content, each with a severity, with variants by connection (UART, Septentrio, DroneCAN), protocol, and capability (GNSS, RTK, RTK heading)
- **Against the source**: the protocol and whether it's auto-detected, the protocol's Kconfig key and constrained-flash builds, ports and baud rates, RTK correction injection, heading support, DroneCAN subscriptions and node parameters, and the compass, barometer and LED drivers PX4 starts
- **Against its siblings**: pages for receivers with the same connection, protocol, capability and manufacturer, including text copied from a sibling that's no longer true
- **Against its listings**: `SUMMARY.md`, the device tables, the protocol sentences on the shared pages, and `dronecan/index.md`, `u-blox_f9p_heading.md` and `septentrio.md` where they apply

It doesn't review the page's prose (that's [px4-doc-review](../px4-doc-review)), parameter descriptions ([px4-param-review](../px4-param-review)), or the driver code (that's `review-pr` in the PX4-Autopilot repo, or `code-review`).

`px4-doc-review` hands GNSS PRs to this skill and includes its findings in its own report, the same way it hands boards to [px4-board-doc-review](../px4-board-doc-review) and rangefinders to [px4-rangefinder-doc-review](../px4-rangefinder-doc-review), which this skill is modelled on.
You can also run it on its own.

It can also **update** an existing page: after a review, it works down the page in template order and proposes one change at a time with its evidence, applying each only when you approve it.

## Skill structure

```
px4-gnss-doc-review/
├── SKILL.md                        # the main agent's instructions: scope, dispatch, report
├── references/
│   ├── shared.md                   # read by every lens: read-only rule, scope, GNSS facts, sources, severity
│   ├── protocol-sources.md         # facts worksheet; which source file answers which claim; protocols; firmware keys; receiver-to-page map
│   ├── page-template.md            # page kinds, skeleton with standard wording, every numbered check
│   ├── source-consistency.md       # lens: page claims vs source
│   ├── sibling-comparison.md       # lens: page vs connection, protocol, capability and manufacturer siblings
│   ├── completeness.md             # lens: template presence/form checks, documentation checklist, listings
│   └── page-update.md              # updating an existing page, one approved suggestion at a time
├── existing-page-issues.md         # work list of problems on existing GNSS pages (not read by the review)
├── preferences.example.md          # boilerplate to copy to ~/.config/px4-gnss-doc-review/preferences.md
└── README.md                       # this file
```

## Sources of truth

In precedence order, from `references/shared.md`:

1. The source in the PR: the `gps` driver and its protocol submodule, the Septentrio driver, the DroneCAN bridge and node firmware, startup scripts
2. The PX4 docs' shared pages (`gps_compass/index.md`, `rtk_gps.md`, `u-blox_f9p_heading.md`, `septentrio.md`, `dronecan/index.md`, `peripherals/serial_configuration.md`)
3. The page template (`references/page-template.md`)
4. Comparator pages, when at least two agree
5. Manufacturer material the page links (never as a source for PX4 configuration)
6. The rest of this skill

## Installing

Symlink the skill into Claude Code's skills directory:

```bash
ln -s ~/github/hamishwillee/my-work-ai-skills/UAV/PX4/px4-gnss-doc-review ~/.claude/skills/px4-gnss-doc-review
```

Optionally copy the preferences file:

```bash
mkdir -p ~/.config/px4-gnss-doc-review
cp ~/.claude/skills/px4-gnss-doc-review/preferences.example.md ~/.config/px4-gnss-doc-review/preferences.md
```

## Requirements

- **`gh` CLI**, authenticated.
- **A local clone of `PX4-Autopilot`** with its `src/drivers/gps/devices` submodule, strongly recommended: the review reads the protocol implementations and comparator pages, which is slow over the API.
- **A way to read PDFs**, for manufacturer manuals: `pdftotext` (poppler-utils), or Python with `venv` so `pypdf` can be installed in a scratch directory.

## Using

```
/px4-gnss-doc-review <PR number>
```

With no PR, it offers **Enter PR**, **Local branch** or **Existing page**; a local-branch run diffs your working tree against the default branch.

To update a page rather than review it, ask for that: "update `gps_compass/<page>.md` to the template".

## Output

1. **GNSS summary**: page, products, connection, protocol and whether PX4 detects it, capability, node firmware, and the comparator pages used; bug and finding counts.
2. **GNSS documentation checklist**: each thing a reader needs, with `yes` / `no` / `partial` / `n/a` and evidence.
3. **Issues found**, by area: matches driver source, matches sibling pages, template and listings.
4. **Issue summary per file** and **Detailed review**, one row per issue with line, severity, the template check it fails, and suggested fix.
5. Below the tables: stubs for missing sections, firmware questions, questions for the manufacturer, who to ask, draft comments to post, and shared pages the change leaves stale.

| Severity | Meaning |
| --- | --- |
| `bug` | Misinforms the reader or blocks them: a protocol PX4 won't detect presented as plug and play, a wrong parameter, port or pin, heading enabled for a receiver that can't provide it, RTK corrections that never reach a DroneCAN node, configuration given only as a link to another autopilot's manual, an unreachable page |
| `style` | Departs from the template or from the form its siblings share, but what it says is right |
| `minor` | A suggestion the author can decline |
