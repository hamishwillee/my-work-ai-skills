# Lens: completeness

Does the PR contain everything a reader needs to buy, connect, enable and test this rangefinder, and can they find the page?

This lens applies `page-template.md` in full for *presence and form*: every page-wide check (R-P1 to R-P11), the family-page checks' form half, every section check's "missing" case, and the listing checks (R-L1 to R-L7).
Whether present content is *correct* is `source-consistency.md`'s job; where a check has both halves, raise only the missing or malformed half here.
Cite the check ID in each finding's evidence.

Presence, not wording.
When a shared step is on the page but worded differently from the template's standard sentence (the port sentence, the baud-rate sentence, the missing-parameter note, a listing cell's form), leave it to `sibling-comparison.md`, which compares wording against the template and the comparators together.
Report it here only when the step or the section is absent, or a heading or anchor is wrong.

Use the rangefinder facts to decide what applies: the connection decides which Wiring and PX4 Configuration content is required, whether the driver is in the common set decides what Firmware Support says and whether the top-of-page note is needed, the role decides between R-A5 and R-A6, and the page kind decides whether the family checks run.

## Documentation checklist

The checklist is the summary a reviewer reads first: can a reader get from the box to a working sensor with this page?
Every item gets a status in the report's **Rangefinder documentation checklist**: `yes`, `no`, `partial`, or `n/a`, with the evidence (file and line, or what was searched).
A `no` or `partial` also becomes a finding, at the severity given.

| Item | How to check | Missing is |
| --- | --- | --- |
| **Page exists** | A page under `docs/en/sensor/` or `docs/en/dronecan/` for the new driver or product | `bug` |
| **Reachable from navigation** (R-L1) | An entry in `docs/en/SUMMARY.md` under `Distance Sensors \(Rangefinders\)` | `bug` |
| **Listed in the rangefinder index** (R-L2, R-L3) | A table row with its link reference, and a summary section, in `docs/en/sensor/rangefinders.md`. A row with no summary, or the reverse, is `partial`. | `bug` for the row, `style` for the summary |
| **PX4 version badge** (R-O2) | `<Badge>` below the H1 | `minor` |
| **Hero image** (R-O5) | A photo of the sensor near the top, stored locally | `style` |
| **What it is** (R-O3) | Opening gives technology, range and connection. Update rate is optional. | `style` |
| **Where to buy** (R-B1) | A real purchase or product link | `style`; `bug` for a placeholder |
| **Specifications** (R-S1) | The list, with at least range, interface, input voltage and current draw | `style` |
| **Pinouts** (R-N1) | On the page or linked from it. When the manufacturer facts hold the pinout, put it in the stub as the suggested table. | `bug` |
| **Wiring** (R-W1 to R-W3) | Which port, what connects to what, and how it's powered. Missing any one of the three is `partial`. | `bug` if none, `style` if partial |
| **Sensor configuration** (R-C1) | `n/a` unless the driver needs a setting it doesn't make | `bug` |
| **Firmware support** (R-F1, R-F4 to R-F8, R-O6) | The Firmware Support section, with the keys, how widely the driver is built, how to check a board, how to add it, and how it's enabled; plus the top-of-page note when the driver isn't in the common set. Missing any of the five is `partial`. | `style`; `bug` when the driver isn't in the common set and nothing says so |
| **Enabling parameter** (R-A1) | Named, linked, with the value to set | `bug` |
| **Other parameters** (R-A3) | Every driver parameter mentioned | `style` |
| **Testing** (R-T1) | A way to confirm the sensor is publishing | `style` |
| **Driver reference** (R-I1) | A link to the module reference | `style` |
| **Current manual** (R-I2) | A link to the manufacturer's current manual or datasheet | `style` |
| **Variant stated** (R-O9) | `n/a` unless the manufacturer facts show factory-configured interface variants | `style` or `bug`, per the check |
| **No leftovers** (R-P3, R-P4) | No `TODO`, placeholder URL, empty section, or guidance comment | `bug` if visible on the rendered page, `style` if in a comment |
| **Images resolve** (R-P5, R-P6) | Every referenced image exists, under `docs/assets/hardware/sensors/` | `bug` |
| **Family table** (R-M1) | `n/a` for a single-model page | `style` |

A PR that changes an existing page rather than adding one skips the first three rows.

Every other template check (headings, anchors, order, the remaining section checks) is reported as an ordinary finding, not a checklist row.

A section that holds only a `<!-- placeholder ... -->` stub counts as missing, for the checklist and for findings.
For every missing skeleton section, return a stub as `page-template.md` ("Stubs for missing sections") describes, keyed to the line it goes after, so the report can offer it.
Where the worksheet or the manufacturer facts hold the content (a pinout, the firmware keys, mounting limits), write the suggested text out in full instead of a placeholder; a stub never contains a value neither of them proves (`shared.md`, "If it can't be proven, it isn't asserted").

## Family pages

Apply R-M1, R-M5, R-M6, R-M8 and R-M9 for form: the table is there, has the columns, discontinued models are folded away, model-specific steps name their model.
For R-L2, check there's one `rangefinders.md` row per model, each with a link reference.

## Listings

- **`SUMMARY.md`** (R-L1): the entry exists, under the right parent, in order, with the product name the H1 uses.
- **`rangefinders.md`** (R-L2, R-L3): the row has all six cells, the link reference definition exists and points at the page, and the summary section links the page.
  An empty `Range` cell is `style`.
- **`dronecan/index.md`** (R-L5) and **`collision_prevention.md`** (R-L6), when the connection or role calls for them.

Whether the listing's facts match the page and driver is `source-consistency.md`'s (R-L4).

## Release notes

A new rangefinder driver is normally mentioned in `docs/en/releases/main.md`.
Contributors rarely add it and maintainers often do it at release time, so a missing entry is `minor`, with the line to add as the suggestion.
Check the newest release notes for the section and form in use before suggesting one.

## Anchoring findings

A missing item anchors to where it would go: the heading it belongs under, the line in `SUMMARY.md` or the `rangefinders.md` table where the entry would sit alphabetically, or line 1 of the page for a page-level gap.

## What this lens doesn't cover

Whether present content is correct (`source-consistency.md`), whether it matches its siblings (`sibling-comparison.md`), and prose (`px4-doc-review`).
