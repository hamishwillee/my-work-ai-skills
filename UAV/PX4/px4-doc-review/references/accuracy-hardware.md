# Accuracy lens: hardware

Covers the **hardware** category from the routing table in `shared.md`: airframes, flight controllers, dev kits, frames, sensors, buses (CAN/DroneCAN/UART), power system components, GPS/compass, telemetry radios, cameras, payloads, ESCs, VTX, and complete vehicle write-ups.

These pages describe physical things: what connects to what, what a value means on real hardware, what a part is called and where to get it.
Get the sources of truth in `shared.md` open before starting — items 2 (firmware source, for board/driver-defined values), 3 (sibling pages, for consistency across frame/vehicle variants), and 5 (linked vendor material) all apply here more than to any other category.

## Wiring and connectors

- A named connector, pin, or wire colour claim (e.g. "connect the red wire to the + pin", "use the `I2C2` port") checked against the board's own docs page or a linked pinout/datasheet.
  A wiring instruction that would misconnect hardware if followed is `bug` — this is the category where a wrong claim has physical consequences.
- A pinout table or diagram added or changed: check pin count and labelling against the board's other documented pinouts (a board with an existing pinout table elsewhere in the repo) rather than trusting the new table in isolation.

## Driver and startup claims

A page for a sensor, peripheral, or other supported part makes claims that PX4's own code settles, so check them there, as Validating the docs against the code in `shared.md` describes, rather than against the vendor's material:

- The supported interfaces and the default bus address, against the driver under `src/drivers/` (its `*_main.cpp` and its `PRINT_MODULE_USAGE_*` options).
- How the driver is enabled, such as which `SENS_EN_*` or serial `*_CFG` parameter starts it, against the driver's `module.yaml` or parameter file and the startup lines in `ROMFS/px4fmu_common/init.d/rc.sensors` or the board's `init/rc.board_sensors`.
- Whether the driver is built for the boards the page implies, against `CONFIG_DRIVERS_*` in the relevant `boards/<vendor>/<board>/*.px4board` files.

A claim these contradict is `bug`: a reader who follows it ends up with a part that doesn't start.
Flight-controller board pages are checked against their own board directory by the `px4-board-doc-review` skill (see Scope in `SKILL.md`); this section covers the parts that connect to them.
Rangefinder pages are checked against their driver, claim by claim, by the `px4-rangefinder-doc-review` skill (see Scope in `SKILL.md`), so on those pages leave the driver and startup claims to it and apply the rest of this lens.
GNSS receiver pages are checked against the GPS driver and protocol source, claim by claim, by the `px4-gnss-doc-review` skill (see Scope in `SKILL.md`), so on those pages leave the protocol, port, RTK, heading and DroneCAN configuration claims to it and apply the rest of this lens.

## Firmware support

A page for a part whose driver isn't built into most boards' firmware needs a `## Firmware Support {#firmware_support}` section, because a reader on any other board otherwise looks for an enabling parameter that isn't there.
Rangefinder and GNSS pages are checked for this by their own skills (`px4-rangefinder-doc-review` rules R-F1 to R-F10 and R-O6, `px4-gnss-doc-review` rules G-F1 to G-F3), so on those pages leave it to them.
Apply this to every other hardware page that documents a part with a PX4 driver: airspeed sensors, optical flow, magnetometers, ESCs and their protocols, telemetry radios, cameras, payloads, and other peripherals.

**Is the driver in most firmware?**
Find the driver's own key, the `menuconfig DRIVERS_<...>` symbol in its `Kconfig`, used as `CONFIG_DRIVERS_<...>=y`.
Check whether a common set selects it: a `menuconfig COMMON_<...>` symbol in the parent folder's `Kconfig` (for example `src/drivers/distance_sensor/Kconfig`, `src/drivers/magnetometer/Kconfig`) with a `select` line for the driver.
Then count the boards: `grep -rl "<key>=y" boards --include=default.px4board | wc -l` for each key that builds it, against `ls boards/*/*/default.px4board | wc -l`.
Leave out test targets such as `boards/px4/sitl/test.px4board`.
About half the boards or more is "most firmware" and needs no section; fewer needs one.
A DroneCAN or MAVLink part has no driver of its own in the flight controller: it needs `CONFIG_DRIVERS_UAVCAN=y` or MAVLink on the port, which a line is enough for.

**The heading** is exactly `## Firmware Support {#firmware_support}`, with that explicit anchor, placed between the hardware setup or wiring section and the configuration section.
Another name, such as "Firmware Setup", "Firmware Configuration" or "Add the Driver to the PX4 Build", or the heading without its anchor, is `style`: suggest the exact heading, since the top-of-page note and the configuration section link `#firmware_support`.

**What the section holds**, following the rangefinder template (`px4-rangefinder-doc-review/references/page-template.md`, "Firmware Support"), which is also the wording to suggest:

- The driver, named and linked to its module reference.
- Every key that builds it, in code style with `=y`, saying which is the driver alone and which a common set.
- Which boards set it, each linked to its flight-controller page, or that most boards do when a common set that most boards set includes it.
- How to check a board: the key in `boards/<vendor>/<board>/default.px4board`, or whether the enabling parameter is listed in _QGroundControl_.
- How to add it: the key in the board's `default.px4board`, or [`boardconfig`](../hardware/porting_guide_config.md#px4-menuconfig-setup) and its menu path (read it from the `menu "..."` lines of the `Kconfig` files above the driver), then [build and upload the firmware](../dev_setup/building_px4.md).
- That being in firmware doesn't start the driver, linking the configuration section with the enabling parameter, or naming the board that starts it in `rc.board_sensors` when one does.

When the driver isn't in most firmware, the page also opens with an `::: info` note, after the hero image, saying the driver isn't included in the firmware for most boards and linking `#firmware_support`.
A "tested on" note naming a board doesn't stand in for it.
The configuration section ends with "If the parameter is not available in _QGroundControl_ then the driver is not in the firmware: see [Firmware Support](#firmware_support)."

Severity: a page that reads as though the driver is in every build when it isn't is `bug`.
A page that says so somewhere but lacks the section, the note, the exact heading and anchor, or one of its items is `style`.
A wrong key or menu path, or a named board that doesn't set the key, is `bug`.

## Physical specifications

- Voltage, current, weight, dimension, and similar numeric physical specs: checked against a linked datasheet/vendor page when the page cites one.
  When the page states a spec with no citation and you have no way to verify it, don't invent a `bug` — note it under "pre-existing issues" or flag as needing a source, not as wrong.
- A changed spec value: compare against the same spec elsewhere in the docs for the same part (a flight controller's specs often appear on both its own page and a `complete_vehicles_*` page referencing it) — a mismatch between the two is worth flagging even without an external source.

## Part identity and naming

- Part numbers, model names, and manufacturer names spelled and formatted consistently with how the same part is named elsewhere in the docs (check `hardware`, `flight_controller`, or the relevant `frames_*`/`complete_vehicles_*` folder for prior mentions).
- A product marked (Discontinued), (Discouraged for New Designs), or similar in one place but not a changed reference to it elsewhere — flag the inconsistency.

## Vendor links

- A newly added or changed link to a manufacturer's product page, datasheet, or store listing: spot-check it resolves.
  A link that 404s or redirects to an unrelated product page is `bug`.

## Cross-vehicle-type consistency

Hardware described identically across `complete_vehicles_fw` / `_mc` / `_rover` / `_vtol` should stay identical where the underlying part is the same; a claim that diverges without an evident reason (a genuinely different config for that vehicle type) is worth flagging even when neither instance is independently wrong — note it as a cross-reference question for the reviewer.

## What this lens doesn't cover

Firmware parameter names/defaults, flight-mode behaviour, and configuration-software claims belong to the flight-behavior lens even on a hardware-category page that mentions a parameter in passing — flag it there under that lens's category if you're reviewing a straddling file yourself (see `shared.md`'s note on straddling files), but don't attempt to verify a parameter default against source from this lens.
