# Lens: completeness

Does the PR contain everything the docs need for a board to be accepted, and is the page finished?

This lens applies `page-template.md` in full for *presence and form*: every page-wide check (T-P1 to T-P10, including anchors) and every section check's "missing" case.
Whether present content is *correct* is `source-consistency.md`'s job; where a check has both halves, raise only the missing or malformed half here.
Cite the check ID in each finding's evidence.

The source for what's required is `docs/en/hardware/board_support_guide.md` at the base SHA.
Read its "Adding a Flight Controller" section before starting, and quote it for every `bug` this lens raises, since the requirements can change.
At the time of writing, step 5 ("Open the Pull Request") requires:

- board support code (not this skill's concern)
- "Board documentation: a public pinout mapping PX4 pin definitions to the microcontroller pins and physical connectors, plus a block diagram or schematic of the main components (sensors, power supply) sufficient to understand boot order and software requirements"
- "Links to your flight logs from step 4, in the PR description"

## Submission checklist

The checklist is the summary a reviewer reads first; its rows are the template checks that decide whether a board PR's docs are acceptable.
Every item gets a status in the report's **Board submission checklist**: `yes`, `no`, or `partial`, with the evidence (file and line, or what was searched).
A `no` or `partial` also becomes a finding, at the severity given.

| Item | How to check | Missing is |
| --- | --- | --- |
| **Board page exists** | A page under `docs/en/flight_controller/` for the new board directory | `bug` |
| **Reachable from navigation** | An entry in `docs/en/SUMMARY.md` | `bug` |
| **Listed in a support category** | An entry on one of the `autopilot_*.md` category pages | `bug` |
| **Pinout** (T-N1) | Connector pinout tables on the page, or a link to a public manufacturer pinout document. It must map connectors to signals; a photo with connector names only is `partial`. | `bug` |
| **Radio Control section** (T-RC0 to T-RC6) | A `### Radio Control {#radio_control}` section (a differently named or levelled RC section counts as present; its heading is a `style` finding under `page-template.md`) covering T-RC1 to T-RC6. Present but missing any of how RC is connected, the protocols enabled by default, or the wiring limits is `partial`. RC wiring can't be predicted from the design, so without this a reader can't connect a receiver with confidence. | `bug` |
| **Block diagram or schematic** (T-P8) | An image or linked document showing the main components (sensors, power supply) | `bug` |
| **Flight logs** | At least one `logs.px4.io` link in the PR description (`gh pr view --json body`), for the vehicle type the board is aimed at | `bug`, reported on the PR rather than a file |
| **Build target documented** (T-F2) | Building Firmware section with the `make` command | `style` |
| **Where to buy** (T-B1) | A purchase or product link | `style` |
| **PX4 version badge** (T-O2) | `<Badge>` below the H1 | `style` |
| **Hero image** (T-O6) | A photo of the board near the top, stored locally | `style` |
| **No leftovers** (T-P3, T-P4) | No `TODO` or placeholder text, and no guidance or checklist comments | `bug` if visible on the rendered page (`TODO` text), `style` if in a comment |
| **Images resolve** (T-P6) | Every referenced image exists in the PR or the repo, under `docs/assets/flight_controller/<page-stem>/` | `bug` |

A PR that changes an existing board rather than adding one skips the first three rows and the flight-log row, unless the change is large enough that the PR description should justify it with a log (a new sensor set or a new variant): then report the missing log as a question below the tables, not a finding.

Every other template check (section headings, anchors, Debug Port content, Power, Voltage Ratings, and so on) is reported as an ordinary finding, not a checklist row.

A section that holds only a `<!-- placeholder ... -->` stub counts as missing, for the checklist and for findings.
For every missing skeleton section, return a stub as `page-template.md` ("Stubs for missing sections") describes, keyed to the line it goes after, so the report can offer it.

## Release notes

A new board is normally mentioned under "Hardware Support" in `docs/en/releases/main.md`.
Contributors rarely add it and maintainers often do it at release time, so a missing entry is `minor`, with the line to add as the suggestion:

```md
- [<Manufacturer> <Product>](../flight_controller/<page>.md): <processor> autopilot based on <reference design>, with <one distinguishing feature>. ([PX4-Autopilot#<n>](https://github.com/PX4/PX4-Autopilot/pull/<n>))
```

That's the form `releases/1.18.md` uses; check the newest release notes for the form in use before suggesting it.

## Anchoring findings

A missing item anchors to where it would go: the heading it belongs under, the line in `SUMMARY.md` or the category page where the entry would sit alphabetically, or line 1 of the page for a page-level gap.
The flight-log finding anchors to the PR, shown as `PR description` in the Line column.

## What this lens doesn't cover

Whether present content is correct (`source-consistency.md`), whether it matches its siblings (`sibling-comparison.md`), and prose (`px4-doc-review`).
Firmware requirements in the same guide (board ID, VID/PID) belong to `review-pr`.
