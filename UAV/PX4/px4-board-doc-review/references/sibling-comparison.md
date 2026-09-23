# Lens: sibling comparison

Does the board's page look and read like the pages of the boards it's most like?

A board built on a reference design, sold by a manufacturer, and listed in a support category has three sets of siblings.
Pages in each set share a form: the same disclaimers, the same sections, the same kind of listing entry, often the same paragraphs about the parts of the design they share.
A new page that drops something every sibling has, or words a shared fact differently, is either a gap or a copy that went wrong.
This lens finds both.

## Choosing comparator pages

The main agent picks these in Scope and passes them to every lens; if you're given none, pick them yourself by these rules and say which you used.

1. **Reference-design siblings.**
   Every other board implementing the same design: `ls -d boards/*/<design>` at the base SHA (for `fmu-v6x`: `ark`, `auterion`, `cuav`, `px4`, ...), plus boards whose own page says it implements that design (`grep -l -i "FMUv6X" docs/en/flight_controller/*.md`).
   Map each board to its page by its build target: `grep -l "<vendor>_<board>_default" docs/en/flight_controller/*.md`.
   The `px4/<design>` reference board usually maps to several pages (Holybro, CUAV, ... Pixhawk-branded boards); include one of them.
   `docs/en/flight_controller/pixhawk_series.md` and `docs/en/hardware/reference_design.md` list the Pixhawk-branded boards for each design.
2. **Support-category siblings.**
   The three most recently added pages listed on the same category page, found with `git log --diff-filter=A --format='%h %ad' --date=short -- docs/en/flight_controller/<page>.md` for each listed page.
   Skip commits that add many pages at once (a repository import or a bulk move): they don't date the page.
   Recent pages show the form the maintainers accept today.
3. **Manufacturer siblings.**
   Other pages by the same manufacturer, if any, for naming (how the manufacturer and its products are written) and for the manufacturer's contact link.

Use two to five comparators in all, favouring reference-design siblings.
List them, with the reason each was chosen, in your return, so the report can name them.

## What to compare

### Category-specific content

Each support category tells the reader something different about who stands behind the board, so each has its own disclaimers, links and listings.
Compare the page with its **support-category siblings**, not with pages from other categories: a manufacturer-supported page that copies a Pixhawk-standard page's note makes a support promise the PX4 team hasn't made.

What each category's pages share, at the time of writing:

| | Pixhawk standard (`autopilot_pixhawk_standard.md`) | Manufacturer supported (`autopilot_manufacturer_supported.md`) | Experimental (`autopilot_experimental.md`) |
| --- | --- | --- | --- |
| **Support note** | `::: tip` / `This autopilot is [supported](../flight_controller/autopilot_pixhawk_standard.md) by the PX4 maintenance and test teams.` / `:::` | `::: info` / `This flight controller is [manufacturer supported](../flight_controller/autopilot_manufacturer_supported.md).` / `:::` | No standard note; pages carry warnings about what's untested or unsupported instead |
| **Standards links** | Links to the Pixhawk standards it implements (the FMU and connector standard PDFs in [Pixhawk-Standards](https://github.com/pixhawk/Pixhawk-Standards)); most link the Pixhawk Debug port definition (`../debug/swd_debug.md#pixhawk-debug-full` or `-mini`) | Only for the standards it actually claims; a board "based on" a reference design links that design | Not expected |
| **Other listings** | Listed by FMU version in `pixhawk_series.md` ("Pixhawk Series"), next to its reference-design siblings | Not listed in `pixhawk_series.md`, which is for Pixhawk-standard products | None |

This table is a starting point, not the rule: confirm each row against two category siblings before reporting from it, since wording and practice change.
The manufacturer warning (`page-template.md`, "Page opening") is the same in every category.

Findings:

- A support note that names a different category from the listing is `bug`: it tells the reader who supports the board.
- A support note with the right category in different words, or missing, is `style`.
- Links, listings or claims that belong to another category (a Pixhawk-standard note or `pixhawk_series.md` entry for a manufacturer-supported board; a Pixhawk-standard board with no standards links) are `style`, or `bug` when they promise support or compliance the board doesn't have.
- A claim of standard compliance ("Pixhawk standard connectors", "Pixhawk Debug Mini") that the page's own pinout contradicts is `bug`.
- The manufacturer warning missing or reworded is `style`; a contact link that points somewhere other than the manufacturer is `bug`.

### Listing placement

- The category page lists the board in alphabetical order by manufacturer and product, in the same link form as its neighbours (`- [<Manufacturer> <Product>](../flight_controller/<page>.md)`).
- `docs/en/SUMMARY.md` lists it under the same category heading, in the same position relative to its neighbours, with the same link text as the category page and the page's H1.
- If the PR edits `docs/en/_sidebar.md` (generated from `SUMMARY.md`), its entry must match `SUMMARY.md` exactly apart from the leading `/`.
- A board listed in one category on the category page and another in `SUMMARY.md` is `bug`.

### Shared-design facts

Use the reference-design diff from `board-sources.md` ("Diffing against the reference design").

- **Where the board's files match the reference board**, the page should agree with its reference-design siblings on that area: the same serial mapping, the same output count and grouping, the same console port.
  A disagreement is `bug` if the board files back the siblings, and a question for the reviewer if they don't settle it.
- **Where the board's files differ from the reference board**, the page must describe this board.
  A paragraph that matches a sibling's word for word in an area where the board files differ is a likely copy that wasn't updated: check each claim in it against the board files, and report any that are wrong as `bug`.
- **A feature the siblings document that this board has** (per its board files) but its page doesn't mention, such as Ethernet, an IMU heater, a PX4IO coprocessor and its MAIN/AUX split, or the Pixhawk Autopilot Bus form factor, is `style`.
- **A feature the siblings document that this board lacks** should be absent from the page, or stated as absent when a reader would expect it from the design ("unlike other FMUv6X boards, the Atlas has no Ethernet port").

### Section set and order

`completeness.md` checks the section set against `page-template.md`; don't repeat those findings.
This lens adds what the template can't know: a section every comparator has that the template doesn't (for example a `## Peripherals` section on every FMUv6X page) is `minor`, and where two or more comparators agree on a heading or section the template does differently, note it below the tables for the reviewer.
Don't report a difference in which comparators disagree among themselves.

### Naming

- The product and manufacturer are named the same way in the H1, the category page, `SUMMARY.md`, and the page body.
- The reference design is named as the sibling pages name it (`FMUv6X`, not `FMU-v6X` or `v6x`), and links where they link (the Pixhawk standard PDF on GitHub, or `../hardware/reference_design.md`).

## What this lens doesn't cover

- Whether the page's claims match the board files, except through the shared-design comparison above: that's `source-consistency.md`.
- Whether the page has what the board support guide requires: that's `completeness.md`.
- Prose quality: that's `px4-doc-review`.
