# Lens: sibling comparison

Does the page read like the pages of the receivers it's most like?

Receivers that connect and speak the same way are set up the same way, so their pages share sentences: which port a primary GPS goes on, how to select a protocol PX4 doesn't use by default, how to enable DroneCAN, where RTK and heading setup are described.
A new page that words a shared step differently, or drops one every sibling has, is either a gap or a copy that went wrong.
GNSS pages are often written by copying a sibling, and the survey behind this skill found product names, intros, hero images and links left over from the page they were copied from.
This lens finds both.

## Choosing comparator pages

The main agent picks these in Scope and passes them to every lens; if you're given none, pick them yourself by these rules and say which you used.
`protocol-sources.md` ("Receivers and their pages") is the starting map.

1. **Connection and protocol siblings.**
   Pages for receivers with the same connection (UART, UART-Septentrio, DroneCAN) and, for UART, the same protocol, since together they decide the wiring and configuration text.
   For DroneCAN, prefer the same node firmware (PX4 cannode, AP_Periph, vendor).
2. **Capability siblings.**
   For an RTK receiver, other RTK pages; for an RTK heading receiver, other heading pages with the same heading method (dual antenna, moving base).
3. **Manufacturer siblings.**
   Other pages by the same manufacturer, for naming and for text the manufacturer's products share, and to catch a page copied from one of them.
4. **Recent pages.**
   Prefer the most recently added or rewritten: `git log --diff-filter=A --format='%h %ad' --date=short -- docs/en/gps_compass/<page>.md`, skipping commits that add many pages at once.

Use two to four comparators in all, favouring connection and protocol siblings.
Many existing GNSS pages are incomplete or out of date, so prefer the exemplars in `protocol-sources.md` where they fit, and never use a page as a comparator for a section where it's known to be wrong.
List them, with the reason each was chosen, in your return, so the report can name them.

## What to compare

### Shared steps

For each step the page shares with its connection siblings, compare the wording with the template's standard sentence (`page-template.md`, "Skeleton" and "Standard wording") and with the comparators.

| Step | Connection | Standard form |
| --- | --- | --- |
| Which port | UART | The primary receiver on the 10-pin `GPS1` port of a flight controller that follows the Pixhawk connector standard ("Full GPS + Safety Switch Port") |
| Protocol, u-blox | UART, UBX | The receiver is detected automatically on `GPS1`; no protocol or baud rate needs setting |
| Protocol, other | UART, not UBX | Set [GPS_1_PROTOCOL](../advanced_config/parameter_reference.md#GPS_1_PROTOCOL) to the value (`6` for NMEA) and reboot, with the reason (not auto-detected, or not the default) |
| Secondary receiver | UART | Set [GPS_2_CONFIG](../advanced_config/parameter_reference.md#GPS_2_CONFIG) to the port, and the protocol if needed, linking [Secondary GPS Configuration (UART)](../gps_compass/index.md#secondary-gps-configuration-uart) |
| Constrained flash | UART, not UBX | A note that the protocol isn't included in firmware for boards with constrained flash |
| RTK | any | A link to [RTK GNSS](../gps_compass/rtk_gps.md) for the ground-station and correction setup |
| Heading | heading-capable | `SENS_GNSSn_HDG`, the antenna positions and the `EKF2_GPS_CTRL` bit, linking [Configuring GPS as Yaw/Heading Source](../gps_compass/rtk_gps.md#configuring-gps-as-yaw-heading-source) |
| Enabling DroneCAN | DroneCAN | `UAVCAN_ENABLE`, then the GNSS subscriptions, then `UAVCAN_PUB_RTCM` for RTK, linking [DroneCAN > GPS](../dronecan/index.md#gps) and [RTK GPS](../dronecan/index.md#rtk-gps) |
| Mounting | any | Facing forward (the arrow), away from other electronics, linking [Mounting a Compass](../assembly/mount_gps_compass.md) |
| Position offsets | any | The `SENS_GNSS0_OFF*` parameters for the antenna position |

This lens owns how a shared step is *worded*; whether the step is *there* is `completeness.md`'s.

- The page words a shared step differently from the template and from two agreeing comparators: `style`, with the standard sentence as the suggestion.
- The page leaves a shared step out altogether: not yours when the template has a check for it, which is every row above.
  Report a missing step only when two comparators have it and the template has nothing for it.
- Two comparators agree with each other and differ from the template: report against the template and note the comparators below the tables.

### Copied text that's no longer true

A paragraph that matches a sibling's word for word is fine where the two receivers behave the same, and a likely mistake where they don't.
For each such paragraph, check its claims against *this* receiver's facts: the product name, the protocol sentence ("plug and play" copied from a u-blox page onto an NMEA one), the heading setting (copied from a heading receiver onto a single-antenna one), the links, the hero image.

- A sibling's product name left in the text, intro or links (a Holybro page telling the reader about the "ARK GPS"; a MINI page linking the full-size product) is `bug`.
- A copied sentence the GNSS facts contradict is `bug`.
- A copied figure, image or link that belongs to the sibling (a hero photo of another model, a manual link for another product) is `bug`.

### Pages that should match

Two pages for near-identical products from one manufacturer (two receivers that differ in chip or capability only; an RTK and a non-RTK version) should say the same thing outside the facts that differ.

- Diff the two pages.
  Every difference should be a fact that genuinely differs (receiver, bands, RTK, a feature, a URL).
- A difference that isn't one (a title pattern, a section one has and the other lacks, a step worded two ways) is `style` on the page under review.
- A place where the pages are the same but the products differ is the copied-text case above.
- Byte-identical image files used by both pages should be one shared file (G-P12).

### Discontinued products

Compare with the other discontinued pages for the form in `page-template.md` (G-O7, G-L1, G-L3): H1 suffix, badge, warning, `✘` prefix in `SUMMARY.md`, and the device-table convention.

- A product marked discontinued in one of those places and not the others is `style`; marked discontinued on its page but listed as current in a device table, or the reverse, is `bug`.

### Listing form

- The `SUMMARY.md` entry and device-table row have the same form as their neighbours: link text, `(CAN)` for a DroneCAN product, cell contents (`✓`, `F9P`, `IST8310`).
- A cell written differently from every neighbouring row is `style`.

### Naming

- The product and manufacturer are named the same way in the H1, `SUMMARY.md`, the device table and the page body, and the manufacturer the way the manufacturer and its other pages name it (`GlobalSat`, not `Globalsat`; `u-blox`, not `Ublox` or `UBLOX`).
- Receiver chips are named as their manufacturer names them (`ZED-F9P`, `UM982`, `mosaic-X5`).
- A new page's file name follows its siblings' pattern, `rtk_gps_<manufacturer>_<product>.md` for RTK and `gps_<manufacturer>_<product>.md` for other UART receivers; that's `completeness.md`'s check (G-P14, G-P15), so don't report it twice.

### Section set

`completeness.md` checks the section set against `page-template.md`; don't repeat those findings.
This lens adds what the template can't know: a section two or more comparators have that the template doesn't is `minor`, noted for the reviewer.
Don't report a difference on which comparators disagree among themselves.

## What this lens doesn't cover

- Whether the page's claims match the source, except through the copied-text comparison above: that's `source-consistency.md`.
- Whether the page has every section and listing: that's `completeness.md`.
- Prose quality: that's `px4-doc-review`.
