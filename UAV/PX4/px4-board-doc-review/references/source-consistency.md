# Lens: source consistency

Does the page say what the board's own files configure?

A flight-controller page is mostly a description of settings that already exist in `boards/<vendor>/<board>/`: which UART is `TELEM1`, how many outputs there are, which sensors start.
When the page and the files disagree, a user wires a peripheral to the wrong port or sets up the wrong output.
This is the lens where a wrong claim has physical consequences, so work every checkable claim, not a sample.

Read `references/board-sources.md` in full before starting: it says which file answers which question.

This lens owns the *correctness* half of every `page-template.md` check: where a check's severity says "`bug` if wrong", you decide whether it's wrong.
Whether the content is *present* and in the right form is `completeness.md`'s job.
Cite the check ID alongside the board-file evidence (`T-U2; default.px4board:6 CONFIG_BOARD_SERIAL_TEL1="/dev/ttyS6"`).

## Method

1. **Start from the board facts worksheet** (`board-sources.md`) the main agent filled in, and re-open a board file only to confirm a value you're about to cite or one the worksheet marks `unknown`.
   If you find a worksheet value wrong, report that and use the corrected value.
2. **Check the derived values yourself** where the worksheet's reader could slip: the UART order behind each `/dev/ttyS*`, output numbering from `timer_config.cpp` (capture entries excluded), and DShot and bidirectional DShot per output from "DShot by chip family".
3. **List every checkable claim on the page** that falls in the lookup table: processor, coprocessor, each sensor, each serial-mapping row, the console port, output counts, DShot claims, RC port, power monitoring, CAN, Ethernet, SD card, heater, build targets.
4. **Check each claim** against the file the lookup table names, and record the file and line whatever the outcome, so the evidence exists for any finding.
5. **Check the other direction**: what the board files configure that the page doesn't mention (a serial port missing from the mapping table, a second GPS port, a variant build target).
   Missing rows in a table the page does have are `bug` (the table reads as complete); a whole area the page doesn't cover is left to `completeness.md` and `sibling-comparison.md`.

## Rules

### Serial port mapping

- Every `CONFIG_BOARD_SERIAL_*` in `default.px4board` has a row, plus the debug console (`CONFIG_<UART>_SERIAL_CONSOLE`) and, if there's a PX4IO, the IO link (`PX4IO_SERIAL_DEVICE`).
- Each row's UART and `/dev/ttyS*` agree with the defconfig ordering rule in `board-sources.md`.
- Each row's port name is the label printed on the board as the page uses it elsewhere (`TELEM1`, not `TEL1`, which is the Kconfig spelling), and the page is consistent with itself.
- Flow-control claims ("TELEM1 has full flow control") are backed by RTS/CTS definitions for that UART.
- Two labels mapped to the same device (for example `CONFIG_BOARD_SERIAL_RC` and `PX4IO_SERIAL_DEVICE` both `/dev/ttyS5`): first check the reference board (`boards/px4/<design>/`).
  If it does the same, the board inherited it and there's nothing to report; the page should describe it the way its reference-design siblings do.
  If it doesn't, it's a firmware question, not a docs finding: report it below the tables for the reviewer to raise with the author, and don't guess which is right on the page.

### Outputs

- FMU output count equals `DIRECT_PWM_OUTPUT_CHANNELS` and the `initIOTimerChannel` entries.
- With a PX4IO, the page distinguishes the 8 IO (`MAIN`) outputs from the FMU (`AUX`) outputs, and doesn't claim DShot on IO outputs.
- Timer groups on the page match `timer_config.cpp`.
- DShot and bidirectional DShot claims match, output by output, what `board-sources.md` ("DShot" rows and "DShot by chip family") gives for this board; a board with DShot the page doesn't mention is `style` (T-PWM2).
- DShot claimed on an STM32F4 or STM32F7 board is `bug`: PX4 doesn't support it there.

### Radio Control

Check the Radio Control section (`page-template.md`, "Radio Control") claim by claim against the RC rows of `board-sources.md`:

- **Path**: a page saying RC goes to the IO needs `CONFIG_DRIVERS_PX4IO=y`; a page saying it goes to the FMU needs `CONFIG_BOARD_SERIAL_RC` / `RC_SERIAL_PORT` (serial) or `GPIO_PPM_IN` (PPM).
  A board with both paths in source whose page describes only one is `bug`: a reader with a receiver on the other path can't make it work.
- **Protocols built in**: every FMU protocol the page names must be built (`CONFIG_DRIVERS_RC_INPUT`, `CONFIG_COMMON_RC`, or the individual `CONFIG_DRIVERS_RC_*` line); a protocol named but not built is `bug`.
- **Enabled by default**: a claim that a protocol works "out of the box" or "by default" on the FMU needs either `rc_input` (default port RC) or a `param set-default RC_<X>_PRT_CFG 300` line in `rc.board_defaults`.
  With `CONFIG_COMMON_RC` and no such line, the page must say the user has to set a `RC_<X>_PRT_CFG` parameter; saying nothing is `bug`, because the receiver silently won't work.
- **Wiring limits**: the page's limits agree with the wiring macros (single-wire, swapped RX/TX, shared PPM pin, inversion, Spektrum power), and with the chip family (no hardware UART inversion on STM32F4).
  A protocol the page offers that the wiring rules out is `bug`.
  A limit in source the page doesn't mention (for example, CRSF offered on the IO path) is `bug` if a reader following the page would wire a receiver that won't work, otherwise `style`.
- **Enabling parameters**: the parameter names exist (`RC_CRSF_PRT_CFG`, `RC_DSM_PRT_CFG`, `RC_GHST_PRT_CFG`, `RC_SBUS_PRT_CFG`, `RC_PORT_CONFIG`, `RC_INPUT_PROTO`) and link to `../advanced_config/parameter_reference.md#<NAME>`.

Which physical connector the IO's RC input reaches isn't in board source.
Take the page's word for it unless the pinout on the page contradicts it; a contradiction between the Radio Control section and the pinout is `bug`.

### Sensors and processor

- Each named IMU, barometer and magnetometer has a start line in `rc.board_sensors` (or is covered by a generic probe the page acknowledges as external).
- A sensor started only in one `ver hwtypecmp` block is described as revision-specific, or the page says which revision it describes.
- Processor part number matches the defconfig; core, clock, flash and RAM match `board-sources.md`, "Processors" (T-S1).
- Each Interfaces count (T-S3) matches its lookup-table row: serial ports and their labels, I2C internal/external, SPI buses and any external one, CAN, Ethernet, parameter storage, SD card.
- **Power monitoring** under Electrical data (T-S4) names the monitor that's on by default per `rc.board_defaults` and `rc.board_sensors`.

### Power

- The monitor type (analog/digital, chip name) matches the drivers started in `rc.board_sensors`.
- The number of power inputs matches `BOARD_NUMBER_BRICKS`.

### Build targets

- The `make` command in Building Firmware names a target that exists (`<vendor>_<board>_default`), with the vendor and board spelled exactly as the directory names them.
- Every variant `.px4board` either has its target listed or the page says why not.

### Physical specifications

Voltage ratings, dimensions, weight and temperature range aren't in the board files.
Check them only against manufacturer material the page links (`shared.md`, source 5), and against the same figures elsewhere on the page.
An unsourced figure you can't check is not a finding.

## Severity

A claim the board files contradict is `bug`.
A table that omits a row the board files configure is `bug`.
A feature the board files configure that the page never mentions is `style`.
A claim you can't check against any source is not a finding; if it matters to wiring (a pin assignment on an undocumented connector), note it below the tables as unverified.

## What this lens doesn't cover

Page form, disclaimers and listing (`sibling-comparison.md`), required content (`completeness.md`), and prose (`px4-doc-review`).
