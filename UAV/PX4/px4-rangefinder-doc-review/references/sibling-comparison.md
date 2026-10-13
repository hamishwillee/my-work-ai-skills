# Lens: sibling comparison

Does the page read like the pages of the rangefinders it's most like?

Rangefinders that connect the same way are set up the same way, so their pages share sentences: where a serial sensor can be plugged in, that the baud rate needn't be set, what to do when the parameter is missing, how to enable a DroneCAN subscription.
A new page that words a shared step differently, or drops one every sibling has, is either a gap or a copy that went wrong.
This lens finds both.

## Choosing comparator pages

The main agent picks these in Scope and passes them to every lens; if you're given none, pick them yourself by these rules and say which you used.
`driver-sources.md` ("Drivers and their pages") is the starting map.

1. **Connection siblings.**
   Pages for rangefinders with the same connection (serial, I2C, DroneCAN), since that decides the wiring and configuration text.
   Prefer the most recently added: `git log --diff-filter=A --format='%h %ad' --date=short -- docs/en/sensor/<page>.md`, skipping commits that add many pages at once.
2. **Role siblings.**
   For a sensor publishing `obstacle_distance`, the other Collision Prevention sensors (`sf45_rotating_lidar.md`, `sony_asdt1.md`).
3. **Manufacturer siblings.**
   Other pages by the same manufacturer, for naming, for the family page a model page belongs under, and for text the manufacturer's products share.
4. **Kind siblings.**
   For a family page, another family page (`sfxx_lidar.md`, `teraranger.md`, `tfmini.md`).

Use two to four comparators in all, favouring connection siblings.
List them, with the reason each was chosen, in your return, so the report can name them.

## What to compare

### Shared steps

For each step the page shares with its connection siblings, compare the wording with the template's standard sentence (`page-template.md`, "Skeleton") and with the comparators.
No existing page has a Firmware Support section yet, so for that row the template is the only standard: an older page's "add the driver to the firmware" info note is not a comparator that outvotes it.

| Step | Connection | Standard form |
| --- | --- | --- |
| Which port to use | Serial | "can be connected to any unused serial port (UART), such as `TELEM2`, `TELEM3` or `GPS2`" |
| Setting the port | Serial | "[Configure the serial port](../peripherals/serial_configuration.md) on which the rangefinder will run using [SENS_<X>_CFG](...)" |
| Baud rate | Serial | "There is no need to set the baud rate for the port, as this is configured by the driver." |
| Firmware support | Serial, I2C, PWM | The Firmware Support section's standard paragraphs: the keys, how widely it's built, how to check, how to add it, how it's enabled |
| Missing parameter | Serial, I2C | "If the parameter is not available in _QGroundControl_ then the driver is not in the firmware: see [Firmware Support](#firmware_support)." |
| Not in most firmware | any, driver not in the common set | The top-of-page `::: info` note linking `#firmware_support` |
| Enabling DroneCAN | DroneCAN | `UAVCAN_ENABLE`, `UAVCAN_SUB_RNG`, `UAVCAN_RNG_MIN`, `UAVCAN_RNG_MAX`, `EKF2_RNG_QLTY_T`, then the link to `../dronecan/index.md#distance-sensor-range-finder` |
| Shared estimator setup | any | The link to `../sensor/rangefinders.md#configuration` |

This lens owns how a shared step is *worded*; whether the step is *there* is `completeness.md`'s.

- The page words a shared step differently from the template and from two agreeing comparators: `style`, with the standard sentence as the suggestion.
  That includes port names not in code style within the standard port sentence, and the older form of the missing-parameter note.
- The page leaves a shared step out altogether: not yours when the template has a check for it, which is every row above.
  Report a missing step only when two comparators have it and the template has nothing for it.
- Two comparators agree with each other and differ from the template: report against the template and note the comparators below the tables.

### Copied text that's no longer true

A paragraph that matches a sibling's word for word is fine where the two drivers behave the same, and a likely mistake where they don't.
For each such paragraph, check its claims against *this* driver's facts: the parameter name, the baud-rate sentence, the Kconfig key, the port examples, the product name.

- A sibling's product or parameter name left in the text (an ARK DIST MR page telling the reader to connect the "ARK DIST SR") is `bug`.
- A copied sentence the driver facts contradict ("no need to set the baud rate" for a driver that doesn't set it) is `bug`.
- A copied range, weight or other figure that belongs to the sibling is `bug`.

### Pages that should match

Two pages for near-identical products from one manufacturer (ARK DIST SR and MR; a model page and its family page) should say the same thing outside the facts that differ.

- Diff the two pages.
  Every difference should be a fact that genuinely differs (range, a parameter value, a part number, a current figure).
- A difference that isn't one (a section one has and the other lacks, a step worded two ways) is `style` on the page under review.
- A place where the pages are the same but the products differ is the copied-text case above.

### Family and model pages

- A model page nested under a family page links back to it in its opening, and the family page's Supported Models table links to it (`page-template.md`, R-M8).
- The family page doesn't repeat the model page's setup, and the model page doesn't repeat the family's shared sections; each links to the other for them.
- The model is named the same way on both (`SF45/B`, not `SF45` on one and `SF45/B` on the other).

### Discontinued products

Compare with the other discontinued pages (`teraranger.md`, `cm8jl65_ir_distance_sensor.md`) for the form in `page-template.md` (R-O7, R-L1, R-L2): H1 suffix, badge, warning, `✘` prefix in `SUMMARY.md`, `_(disc.)_` and `Discontinued` in the `rangefinders.md` row.

- A product marked discontinued in one of those places and not the others is `style`; marked discontinued on its page but listed as current in `rangefinders.md`, or the reverse, is `bug`.

### Listing form

- The `SUMMARY.md` entry and `rangefinders.md` row have the same form as their neighbours: link text, the connection in the name where neighbours give it (`(CAN)`), cell contents (`ToF (IR laser)`, `UART`, `0.2 m – 100 m`).
- A technology, connection or range written differently from every neighbouring row (`Serial` where they have `UART`) is `style`.

### Naming

- The product and manufacturer are named the same way in the H1, `SUMMARY.md`, `rangefinders.md` and the page body, and the manufacturer the way its other pages name it (`LightWare`, not `Lightware`).

### Section set

`completeness.md` checks the section set against `page-template.md`; don't repeat those findings.
This lens adds what the template can't know: a section two or more comparators have that the template doesn't is `minor`, noted for the reviewer.
Don't report a difference on which comparators disagree among themselves.

## What this lens doesn't cover

- Whether the page's claims match the driver, except through the copied-text comparison above: that's `source-consistency.md`.
- Whether the page has every section and listing: that's `completeness.md`.
- Prose quality: that's `px4-doc-review`.
