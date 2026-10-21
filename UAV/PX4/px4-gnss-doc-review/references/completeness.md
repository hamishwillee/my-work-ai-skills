# Lens: completeness

Does the PR contain everything a reader needs to buy, mount, connect, configure and test this receiver, and can they find the page?

This lens applies `page-template.md` in full for *presence and form*: every page-wide check (G-P1 to G-P15), the family-page checks' form half, every section check's "missing" case, and the listing checks (G-L1 to G-L7).
Whether present content is *correct* is `source-consistency.md`'s job; where a check has both halves, raise only the missing or malformed half here.
Cite the check ID in each finding's evidence.

Presence, not wording.
When a shared step is on the page but worded differently from the template's standard sentence (the port sentence, the protocol sentence, the RTK link, a listing cell's form), leave it to `sibling-comparison.md`, which compares wording against the template and the comparators together.
Report it here only when the step or the section is absent, or a heading or anchor is wrong.

Use the GNSS facts to decide what applies: the connection decides which Wiring and PX4 Configuration content is required; the protocol decides whether a protocol setting and a Firmware Support section are needed; the capability decides whether RTK and heading content is required; the node firmware decides what Receiver Configuration covers; and the page kind decides whether the family checks run.

## Documentation checklist

The checklist is the summary a reviewer reads first: can a reader get from the box to a working receiver with this page?
Every item gets a status in the report's **GNSS documentation checklist**: `yes`, `no`, `partial`, or `n/a`, with the evidence (file and line, or what was searched).
A `no` or `partial` also becomes a finding, at the severity given.

| Item | How to check | Missing is |
| --- | --- | --- |
| **Page exists** | A page under `docs/en/gps_compass/` (UART) or `docs/en/dronecan/` (DroneCAN) for the product | `bug` |
| **Reachable from navigation** (G-L1) | An entry in `docs/en/SUMMARY.md` under `GNSS (GPS)` or `RTK GNSS`, matching the capability | `bug` |
| **Listed in the device table** (G-L2) | A row, with its link, in the `gps_compass/index.md` table (non-RTK) or the `rtk_gps.md` table (RTK) | `bug` |
| **PX4 version badge** (G-O2) | `<Badge>` below the H1, when the template asks for one | `minor` |
| **Hero image** (G-O4) | A photo of the receiver near the top, stored locally | `style` |
| **What it is** (G-O3) | Opening gives manufacturer, product, receiver or bands, capability (GNSS, RTK, heading), and connection | `style` |
| **Where to buy** (G-B1) | A real purchase or product link | `style`; `bug` for a placeholder |
| **Specifications** (G-S1) | The list, with at least the receiver or bands, compass, interface, input voltage | `style` |
| **Mounting** (G-H1) | Orientation, distance from other electronics, and antenna separation for heading | `style` |
| **Pinouts** (G-N1) | On the page or linked from it; for a Pixhawk-standard connector, a statement that it follows the standard is enough when the pinout image or table agrees | `bug` for a non-standard connector with neither |
| **Wiring** (G-W1, G-W2) | Which port, and how it's powered | `bug` if none, `style` if partial |
| **Receiver configuration** (G-C1) | `n/a` unless the receiver must be changed from its factory state for PX4, or is a DroneCAN node whose firmware the reader may need to update | `bug` when PX4 can't use the receiver as shipped and nothing says what to change |
| **Firmware support** (G-F1 to G-F3) | `n/a` for a u-blox UART receiver; otherwise the Kconfig key and which builds leave it out (protocol, Septentrio driver) or the DroneCAN driver | `style`; `bug` when the protocol isn't in every build and nothing says so |
| **Protocol and port** (G-A1) | What to set for the protocol and port, or a correct statement that nothing needs setting | `bug` |
| **Secondary receiver** (G-A3) | How to run it as a second GPS, or a link to the shared section | `style` |
| **RTK** (G-A4) | `n/a` for a non-RTK receiver; otherwise a link to RTK setup and, for DroneCAN, the correction publication | `bug` for DroneCAN when `UAVCAN_PUB_RTCM` isn't covered; `style` otherwise |
| **Heading** (G-A5) | `n/a` unless PX4 uses the receiver's heading; otherwise `SENS_GNSSn_HDG`, the antenna positions and the heading-fusion bit | `bug` |
| **DroneCAN setup** (G-A6) | `n/a` for UART; otherwise enabling DroneCAN, the subscriptions, and node parameters | `bug` |
| **Testing** (G-T1) | A way to confirm the receiver is publishing a fix (and RTK fix type, and heading, where they apply) | `style` |
| **Current manual** (G-I1) | A link to the manufacturer's current manual or datasheet, labelled as such | `style` |
| **Variant stated** (G-O8) | `n/a` unless the manufacturer facts show interface variants (UART and CAN versions) | `style` or `bug`, per the check |
| **No leftovers** (G-P3, G-P4) | No `TODO`, placeholder URL, empty section, or guidance comment | `bug` if visible on the rendered page, `style` if in a comment |
| **Images resolve** (G-P5, G-P6) | Every referenced image exists, under `docs/assets/hardware/gps/`; on a local branch, is tracked or staged | `bug` |
| **Family table** (G-M1) | `n/a` for a single-product page | `style` |

A PR that changes an existing page rather than adding one skips the first three rows.

Every other template check (headings, anchors, order, the remaining section checks) is reported as an ordinary finding, not a checklist row.

A section that holds only a `<!-- placeholder ... -->` stub counts as missing, for the checklist and for findings.
For every missing skeleton section, return a stub as `page-template.md` ("Stubs for missing sections") describes, keyed to the line it goes after, so the report can offer it.
Where the worksheet or the manufacturer facts hold the content (the protocol value, the Kconfig key, a pinout), write the suggested text out in full instead of a placeholder, using the template's standard wording; a stub never contains a value neither of them proves (`shared.md`, "If it can't be proven, it isn't asserted").

## Family pages

Apply G-M1 to G-M5 for form: the table is there, has the columns, discontinued products are folded away, product-specific steps name their product.
For G-L2, check there's a device-table row per product, each with its link.

## Listings

- **`SUMMARY.md`** (G-L1): the entry exists, under `GNSS (GPS)` for a non-RTK receiver or `RTK GNSS` for an RTK one, in order, with the product name the H1 uses, ending ` (CAN)` for a DroneCAN product.
- **Device table** (G-L2, G-L3): a row in exactly one of the two tables, every cell filled as its neighbours fill them, the link resolving, and the row in alphabetical order.
- **Protocol sentences** (G-L5): when the receiver uses a protocol, the sentences on `index.md` and `rtk_gps.md` that list supported protocols name it.
- **`dronecan/index.md`** (G-L6), **`u-blox_f9p_heading.md`** and **`septentrio.md`** (G-L7), when the connection or receiver calls for them.

Whether the listing's facts match the page and source is `source-consistency.md`'s (G-L4).

## Release notes

A new GNSS protocol or driver feature is normally mentioned in `docs/en/releases/main.md`; a new receiver page that needs no new firmware is not.
A missing entry for a firmware change is `minor`, with the line to add as the suggestion.
Check the newest release notes for the section and form in use before suggesting one.

## Anchoring findings

A missing item anchors to where it would go: the heading it belongs under, the line in `SUMMARY.md` or the device table where the entry would sit alphabetically, or line 1 of the page for a page-level gap.

## What this lens doesn't cover

Whether present content is correct (`source-consistency.md`), whether it matches its siblings (`sibling-comparison.md`), and prose (`px4-doc-review`).
