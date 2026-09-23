# Flight-controller page template

The standard for a board page under `docs/en/flight_controller/`: a skeleton page, then numbered checks.
Every lens cites the check ID (`T-RC3`, `T-PWM2`, ...) in a finding's evidence, so the author can look the rule up.

Existing pages vary a lot and many predate this template, so it's the standard for new and changed pages, not a reason to report old ones.
Where two or more comparator pages in the same support category agree on something this template does differently, report the finding and name the comparators below the tables, so the reviewer can judge which should change.

## Skeleton

Sections appear in this order.
A section marked *(if present)* is left out when the board doesn't have the feature; everything else is always present.

````md
# <Manufacturer> <Product>

<Badge type="tip" text="PX4 v1.xx" />

::: warning
PX4 does not manufacture this (or any) autopilot.
Contact the [manufacturer](<manufacturer url>) for hardware support or compliance issues.
:::

<support-category note: see sibling-comparison.md, "Category-specific content">

The [<Product>](<product url>) is <what it is>, manufactured by <Manufacturer>.
It is based on the [<reference design>](<standard url>) <if any>, and <what distinguishes it>.

![<Product>](../../assets/flight_controller/<page-stem>/<image>.jpg)

## Specifications {#specifications}

### Processor {#processor}

### Sensors {#sensors}

### Interfaces {#interfaces}

### Electrical data {#electrical_data}

### Mechanical data {#mechanical_data}

## Where to Buy {#store}

## Pinouts {#pinouts}

## Power {#power}

## Voltage Ratings {#voltage_ratings}

## PWM Outputs {#pwm_outputs}

## Telemetry Radios (Optional) {#telemetry}

## Ethernet {#ethernet}                      (if present)

## SD Card (Optional) {#sd_card}             (if present)

## Serial Port Mapping {#serial_port_mapping}

## Building Firmware {#building_firmware}

## Debug Port {#debug_port}

## Assembly {#assembly}

### Radio Control {#radio_control}

### GPS & Compass {#gps_compass}

## Further Information {#further_information}
````

## Page-wide checks

| ID | Check | Severity if failed |
| --- | --- | --- |
| T-P1 | Headings are exactly as in the skeleton, including the explicit anchor. A heading with the right meaning but different words, level, or anchor is reported with the exact heading as the suggestion. | `style` |
| T-P2 | Sections are in skeleton order. Report the first out-of-order section only, not every section after it. | `minor` |
| T-P3 | No `TODO`, `TBD`, or placeholder text (`<Product>`, `xxx`) anywhere on the rendered page. | `bug` |
| T-P4 | No leftover HTML comments holding guidance, checklists, or raw data (`<!-- ... -->`). A section holding only a `<!-- placeholder ... -->` stub ("Stubs for missing sections" below) isn't a T-P4 finding: it's reported as the missing content it stands in for, at that check's severity. | `style` |
| T-P5 | Every image is local: `../../assets/flight_controller/<page-stem>/<file>`, the folder named after the page's file stem, the file name lower case with underscores. No image loaded from a URL. | `style`; a URL image is `bug` (external images break and aren't translated) |
| T-P6 | Every referenced image exists in the PR or the repository. | `bug` |
| T-P7 | Port and connector names are written as printed on the board, and the same way everywhere on the page: in backticks when naming a port in running text (`TELEM1`), bold when telling the reader what to plug in (**RC IN**). | `style` |
| T-P8 | A block diagram or schematic of the main components (sensors, power supply) is on the page or linked from it (board support guide, step 5). | `bug` |
| T-P9 | Every `##` and `###` heading has an explicit anchor, following "Anchors" below. | `style` |
| T-P10 | Adding or changing an anchor on an existing page doesn't break links to it: every link to the old slug (`<page>.md#<old-slug>` elsewhere in `docs/en/`, and `#<old-slug>` on the page itself) is updated in the same PR. | `bug` per link left broken |

### Stubs for missing sections

When a skeleton section is missing, the report suggests a stub the author can paste in: the heading with its anchor, then a placeholder comment saying what goes there and pointing at good examples.

```md
## PWM Outputs {#pwm_outputs}

<!-- placeholder
16 outputs: 8 IO (MAIN) and 8 FMU (AUX). DShot and bidirectional DShot on AUX 1-6, not 7-8. Groups: AUX 1-4 (Timer5), 5-6 (Timer4), 7-8 (Timer12). Same protocol and rate within a group.
Good examples: nwblue_pro-h757.md#pwm-outputs, amovlab_flycore.md#pwm_outputs, ark_v6xrt.md#pwm_outputs
-->
```

- **What goes there**: one or two lines, filled with this board's own values from the board facts worksheet wherever the source gives them (output counts, DShot outputs, port labels, default configuration), and naming what only the manufacturer can supply otherwise (voltage ratings, dimensions, connector pinouts).
- **Good examples**: two or three pages from "Example sections" below, preferring a reference-design or support-category sibling when it has a good version of the section. Links are page-relative (`ark_v6xrt.md#pwm_outputs`), and the anchor must exist on that page: an explicit `{#anchor}`, or the heading's generated slug (`#voltage-ratings`). Check it before citing.
- **Order**: stubs go where the skeleton puts them, so a page with several gaps gets one block per run of adjacent missing sections, keyed to the line it goes after.
- **Leave out** a section marked *(if present)* when the board source doesn't settle whether the board has the feature; say why below the tables instead.

A page that already holds a stub is reviewed as if the section were missing (T-P4), until the author replaces the placeholder with content.

#### Example sections

Good current versions of each section, as starting points for the "Good examples" line.
Re-check them occasionally: pages get rewritten.

| Section | Examples |
| --- | --- |
| Specifications (all sub-sections) | `ark_v6xrt.md#specifications` (the model form), `cuav_pixhawk_v6x.md#interfaces`, `pixhawk6x.md#electrical-data`, `pixhawk6x.md#mechanical-data` |
| Where to Buy | `ark_v6xrt.md#store`, `cuav_pixhawk_v6x.md#store` |
| Pinouts | `amovlab_flycore.md#pinouts`, `radiolink_pix6.md#pinouts`, `cuav_pixhawk_v6x.md#pinouts` |
| Voltage Ratings | `cuav_pixhawk_v6x.md#voltage-ratings`, `agam_v6xrt.md#voltage-ratings` |
| PWM Outputs | `nwblue_pro-h757.md#pwm-outputs`, `amovlab_flycore.md#pwm_outputs`; `ark_v6xrt.md#pwm_outputs` for an i.MX RT board with no timer groups |
| Telemetry Radios | `amovlab_flycore.md#telemetry` |
| Ethernet | `siyi-unifc-6-pico.md#ethernet` |
| Debug Port | `agam_v6xrt.md#debug_port`, `ark_v6xrt.md#debug_port`, `cuav_pixhawk_v6x.md#debug_port` |
| Radio Control | `ark_v6xrt.md#radio_control` |
| GPS & Compass | `ark_v6xrt.md#gps_compass`, `amovlab_flycore.md#gps_compass` |

### Anchors

Every heading below the H1 carries an explicit anchor, so links survive rewording and translation.

- **Skeleton headings** use the anchor shown in the skeleton, exactly.
  Several are established short forms that differ from the heading text (`{#store}`, `{#telemetry}`, `{#gps_compass}`) and must not be "corrected".
- **Any other heading** (an extra section such as `## Peripherals` or `### GPS2 Port`) takes an anchor made from its text: lower case, words joined by underscores, `&` and punctuation dropped, parenthetical qualifiers such as `(Optional)` dropped.
  For example `## Peripherals {#peripherals}`, `### GPS2 Port {#gps2_port}`, `### Power & Safety {#power_safety}`.
- **Unique on the page**: two headings with the same anchor are `bug` (the second can't be linked).
  Repeated sub-headings under different sections (for example `### Pinout` under each baseboard) take a prefix from their parent: `{#v2a_pinout}`, `{#mini_pinout}`.
- **Hyphenated anchors** (`{#processors-sensors}`) are `style`: PX4 anchors use underscores.

To find links to an old slug before accepting a changed anchor (T-P10), search from `docs/en/`: `grep -rn "<page>.md#<old-slug>" --include=*.md .` and `grep -n "](#<old-slug>)" <page>.md`.
The old slug of a heading with no explicit anchor is its text, lower case, with spaces as hyphens and punctuation dropped (`Serial Port Mapping` → `serial-port-mapping`).

## Section checks

### Opening

| ID | Check | Severity |
| --- | --- | --- |
| T-O1 | One H1, `# <Manufacturer> <Product>`, with the same text as the `SUMMARY.md` entry and the category-page link. | `style` |
| T-O2 | `<Badge type="tip" text="..." />` directly under the H1, naming the first PX4 release with the board. For a board added on `main`, use the form the newest `main` pages use (`grep -rho '<Badge type="tip" text="[^"]*"' docs/en/flight_controller/`). | `style` |
| T-O3 | The manufacturer warning, word for word as in the skeleton, linking the manufacturer's own site. | `style`; a link to someone other than the manufacturer is `bug` |
| T-O4 | The support-category note for the category the board is listed in (`sibling-comparison.md`). | `bug` if it names another category, `style` if missing |
| T-O5 | The description names the manufacturer, links the product page, and names and links the reference design when there is one. | `style` |
| T-O6 | A hero photo of the board. | `style` |

### Specifications {#specifications}

| ID | Check | Severity |
| --- | --- | --- |
| T-S1 | `### Processor {#processor}`: **Main FMU processor:** the part, linked to its manufacturer page, with core, clock and RAM (`board-sources.md`, "Processors"), and any core PX4 doesn't use. **Code store:** only when code doesn't run from internal flash (say where it runs from and how much PX4 uses). **IO processor:** when there's a PX4IO, and "on carriers that fit one" when that depends on the carrier. | `bug` if wrong, `style` if missing |
| T-S2 | `### Sensors {#sensors}`: **IMU:**, **Barometer:**, **Magnetometer:**, each a comma-separated list of parts linked to their manufacturer pages with the bus in parentheses (`(SPI1)`, `(I2C2)`); **Heater:** when fitted, with how it's controlled. A sensor that differs by hardware revision says which revision. | `bug` if wrong, `style` if missing |
| T-S3 | `### Interfaces {#interfaces}`, in this order, each the board has: **PWM outputs:** (FMU count, plus IO count); **Serial ports:** (count, then the port labels in backticks); **I2C buses:** (count, which are internal); **SPI buses:** (count, and any external bus with its chip selects and data-ready lines); **CAN buses:** (count enabled, and any pinned out but unused); **Ethernet:** (speed); **USB:**; **RC input:**; **Parameter storage:** (FRAM, EEPROM or flash, with part); **SD card:** (slot type, or none). | `bug` if a count is wrong, `style` if missing |
| T-S4 | `### Electrical data {#electrical_data}`: **Input voltage:**, **Current draw:** (with the heater's share when there's a heater), **Power monitoring:** (number of inputs, analog or digital, and which monitor is on by default). | `bug` if wrong, `style` if missing |
| T-S5 | `### Mechanical data {#mechanical_data}`: **Dimensions:**, **Weight:**, and **Form factor:** when the board follows a standard (for example [Pixhawk Autopilot Bus](https://github.com/pixhawk/Pixhawk-Standards/blob/master/DS-010%20Pixhawk%20Autopilot%20Bus%20Standard.pdf)), linked. Operating temperature when the manufacturer gives it. | `style` if missing |
| T-S6 | **Form**: each item is one list entry, `- **Label:** value`, with the colon inside the bold and labels in sentence case as above. Units carry a space (`480 MHz`, `2 MB`). Sub-headings are sentence case (`Electrical data`, not `Electrical Data`). | `style` |

A board page can add an item the list doesn't have (**OSD:**, **Airspeed:**); it goes in the sub-section it belongs to, in the same form.
An item the board doesn't have is left out, except **USB:** and **RC input:**, which say `No` when absent.

Model, for a PAB module with an optional PX4IO:

```md
## Specifications {#specifications}

### Processor {#processor}

- **Main FMU processor:** [NXP i.MX RT1176](https://www.nxp.com/products/i.MX-RT1170) (Arm® Cortex®-M7 at 996 MHz, 2 MB RAM). The second Cortex®-M4 core is unused by PX4.
- **Code store:** no internal flash. Code executes in place from a 64 MB external octal NOR on FlexSPI1, of which PX4 uses the first 4 MB.
- **IO processor:** PX4IO v2, on carriers that fit one.

### Sensors {#sensors}

- **IMU:** [InvenSense ICM-45686](https://invensense.tdk.com/products/motion-tracking/6-axis/icm-45686/) (SPI1), [InvenSense IIM-20670](https://invensense.tdk.com/products/motion-tracking/6-axis/iim-20670/) (SPI2), [ST LSM6DSV80X](https://www.st.com/en/mems-and-sensors/lsm6dsv80x.html) (SPI3)
- **Barometer:** [Bosch BMP390](https://www.bosch-sensortec.com/en/products/environmental-sensors/pressure-sensors/bmp390/) (I2C2)
- **Magnetometer:** [ST IIS2MDC](https://www.st.com/en/mems-and-sensors/iis2mdc.html) (I2C3)
- **Heater:** closed loop on the ICM-45686 die temperature

### Interfaces {#interfaces}

- **PWM outputs:** 12 FMU outputs, plus 8 more from PX4IO on carriers that fit one
- **Serial ports:** 8 (`GPS1`, `GPS2`, `TELEM1`, `TELEM2`, `TELEM3`, `TELEM4`, PX4IO/`RC`, Debug Console)
- **I2C buses:** 4 (I2C3 internal, the rest external)
- **SPI buses:** 4, of which SPI6 is external with 2 chip selects and 2 data-ready lines
- **CAN buses:** 2 enabled by default. PAB pins out a third; no ARK carrier breaks it out.
- **Ethernet:** 100BASE-T (ENET2)
- **USB:** Yes
- **RC input:** Yes
- **Parameter storage:** FRAM (FM25V02A) on FlexSPI2
- **SD card:** MicroSD slot

### Electrical data {#electrical_data}

- **Input voltage:** 5 V
- **Current draw:** 500 mA (300 mA main system, 200 mA heater)
- **Power monitoring:** 2 digital power bricks, INA226 by default

### Mechanical data {#mechanical_data}

- **Dimensions:** 3.6 x 2.9 x 0.5 cm
- **Weight:** 5.0 g
- **Form factor:** [Pixhawk Autopilot Bus (PAB)](https://github.com/pixhawk/Pixhawk-Standards/blob/master/DS-010%20Pixhawk%20Autopilot%20Bus%20Standard.pdf)
```

### Where to Buy {#store}

| ID | Check | Severity |
| --- | --- | --- |
| T-B1 | A link to where the board can be bought (manufacturer store or listed resellers). | `style` |

### Pinouts {#pinouts}

| ID | Check | Severity |
| --- | --- | --- |
| T-N1 | Pinouts for every connector: pin, signal and voltage, as tables on the page or a linked public document from the manufacturer. A photo with connector names but no signals is not a pinout. | `bug` (board support guide, step 5) |
| T-N2 | A connector that follows a Pixhawk connector standard can say so and link [DS-009 Pixhawk Connector Standard](https://github.com/pixhawk/Pixhawk-Standards/blob/master/DS-009%20Pixhawk%20Connector%20Standard.pdf) instead of a table, but only if the whole connector complies. | `bug` if the claim is wrong |

### Power {#power}

| ID | Check | Severity |
| --- | --- | --- |
| T-W1 | Which ports take power (as labelled), their connector type, and whether two inputs give redundancy. | `style` if missing, `bug` if wrong |
| T-W2 | Battery monitoring: analog or digital, the monitor chip for digital, and which is enabled by default. | `bug` if wrong |
| T-W3 | The servo-rail warning when outputs aren't powered from the power input: "The PWM output ports are not powered by the POWER port. The output rail must be [separately powered](../assembly/servo_power.md) if it needs to power servos or other hardware." | `style` |
| T-W4 | A link to [Battery and Power Module Setup](../config/battery.md). | `minor` |

### Voltage Ratings {#voltage_ratings}

| ID | Check | Severity |
| --- | --- | --- |
| T-V1 | **Normal operation maximum ratings** for each power input and the USB input, in the order the board draws from them. | `style` if missing |
| T-V2 | **Absolute maximum ratings**: the range each input survives undamaged, including the servo rail. | `style` if missing |
| T-V3 | Figures match the Specifications section and any linked datasheet. | `bug` |

### PWM Outputs {#pwm_outputs}

| ID | Check | Severity |
| --- | --- | --- |
| T-PWM1 | Output count, split into IO (`MAIN`) and FMU (`AUX`) outputs when there's a PX4IO. | `bug` if wrong |
| T-PWM2 | Which outputs support [DShot](../peripherals/dshot.md) and which support [bidirectional DShot](../peripherals/dshot.md#bidirectional-dshot-telemetry), as output ranges. IO outputs never support DShot. | `bug` if wrong, `style` if missing |
| T-PWM3 | The timer groups, as output ranges, and the rule that "All outputs within the same group must use the same output protocol and rate." | `bug` if wrong, `style` if missing |

### Telemetry Radios (Optional) {#telemetry}

| ID | Check | Severity |
| --- | --- | --- |
| T-T1 | Links [telemetry radios](../telemetry/index.md), names the `TELEM` ports as labelled, and says `TELEM1` needs no further configuration. | `style` |

### Ethernet {#ethernet} (if present)

| ID | Check | Severity |
| --- | --- | --- |
| T-E1 | Present when the board has Ethernet (`CONFIG_BOARD_ETHERNET=y`), absent otherwise. Gives the speed and links [PX4 Ethernet Setup](../advanced_config/ethernet_setup.md). | `style` if missing, `bug` if present on a board without it |

### SD Card (Optional) {#sd_card} (if present)

| ID | Check | Severity |
| --- | --- | --- |
| T-D1 | Present when the board has an SD slot (`CONFIG_MMCSD=y`). Says where the slot is and links [SD Cards](../getting_started/px4_basic_concepts.md#sd-cards-removable-memory). | `style` |

### Serial Port Mapping {#serial_port_mapping}

| ID | Check | Severity |
| --- | --- | --- |
| T-U1 | A table with columns `UART`, `Device`, `Port` (and `Flow Control` when any port has it), one row per configured UART, in `/dev/ttyS*` order. | `style` for form |
| T-U2 | Every row matches board source, including the debug console and the PX4IO link (`source-consistency.md`, "Serial port mapping"). | `bug` |

### Building Firmware {#building_firmware}

| ID | Check | Severity |
| --- | --- | --- |
| T-F1 | The tip: "Most users will not need to build this firmware! It is pre-built and automatically installed by _QGroundControl_ when appropriate hardware is connected." | `style` |
| T-F2 | "To [build PX4](../dev_setup/building_px4.md) for this target:" followed by a ` ```sh ` block with `make <vendor>_<board>_default`, and the other targets for any variant `.px4board` files. | `bug` if the target doesn't exist, `style` if missing |

### Debug Port {#debug_port}

| ID | Check | Severity |
| --- | --- | --- |
| T-G1 | Names the port carrying the [PX4 System Console](../debug/system_console.md) and the [SWD interface](../debug/swd_debug.md), and links both. | `style` |
| T-G2 | Says whether it's the **FMU** or **IO** debug port (or both, when there are two). | `style` |
| T-G3 | Says whether the port follows [Pixhawk Debug Full](../debug/swd_debug.md#pixhawk-debug-full) or [Pixhawk Debug Mini](../debug/swd_debug.md#pixhawk-debug-mini), and links it. | `style` |
| T-G4 | A non-standard port gives the connector type, a pin/signal/voltage table, and whether a debug cable is supplied. | `bug` if missing (no one can connect a debugger) |
| T-G5 | The console UART matches `CONFIG_<UART>_SERIAL_CONSOLE` and the Serial Port Mapping table. | `bug` |

### Assembly {#assembly}

| ID | Check | Severity |
| --- | --- | --- |
| T-A1 | Links the board's quick-start or wiring guide when one exists (`docs/en/assembly/quick_start_*.md`). | `minor` |
| T-A2 | Contains `### Radio Control {#radio_control}` and `### GPS & Compass {#gps_compass}`. GPS & Compass may defer to a quick-start guide; Radio Control may not. | per sub-section |

### Radio Control {#radio_control}

Every board page needs this section, because how RC reaches the firmware depends on the board's wiring and can't be worked out from the design name.
The heading is exactly `### Radio Control {#radio_control}`, under Assembly; `RC Input`, `RC`, `RC/SBUS`, `RC Setup`, a `##` level, or a place outside Assembly are `style` (T-P1).
[ARK V6X-RT](https://docs.px4.io/main/en/flight_controller/ark_v6xrt.html#radio_control) is a good model for the content (not its `##` heading).

| ID | Check | Severity |
| --- | --- | --- |
| T-RC0 | The section exists. | `bug` |
| T-RC1 | Says RC is needed only for manual control, and links [selecting a transmitter/receiver](../getting_started/rc_transmitter_receiver.md). | `style` |
| T-RC2 | **Connection**: the RC port as labelled (bold), its connector type, and whether it goes to the **FMU**, the **PX4IO**, or **both**. When it depends on the carrier or baseboard (a Pixhawk Autopilot Bus module, a board sold with several baseboards), each case separately. | `bug` if missing or wrong |
| T-RC3 | **Wiring limits**: any protocol the wiring rules out, and why. For example: the IO can't decode CRSF or GHST, so those receivers go on an FMU serial port; a single-wire or RX-only port can't carry CRSF/GHST telemetry; with no PPM capture pin there's no PPM on the FMU. | `bug` if a reader would wire a receiver that won't work, otherwise `style` |
| T-RC4 | **Built in**: the protocols built in on each path. For the IO, link the [`px4io` protocol list](../modules/modules_driver.md#px4io) rather than repeating it. | `bug` if wrong, `style` if missing |
| T-RC5 | **Enabled by default**: which protocols work with no configuration on each path, or that none does on the FMU. | `bug` if wrong or missing where the FMU needs configuration |
| T-RC6 | **Enabling others**: the parameters that map a protocol to a port (`RC_CRSF_PRT_CFG`, `RC_DSM_PRT_CFG`, `RC_GHST_PRT_CFG`, `RC_SBUS_PRT_CFG`, or `RC_PORT_CONFIG` for `rc_input`), linked to `../advanced_config/parameter_reference.md#<NAME>`, and that only one protocol can be active on a port. | `style` |
| T-RC7 | A PWM receiver (one wire per channel) needs a [PPM encoder](../getting_started/rc_transmitter_receiver.md#pwm-receivers); say so if the board has no PWM RC input. | `minor` |

T-RC4 to T-RC6 can be one list per path, as the ARK V6X-RT page does.

### GPS & Compass {#gps_compass}

| ID | Check | Severity |
| --- | --- | --- |
| T-GP1 | Each GPS port in backticks, as labelled, with its connector type and what it carries (GPS, compass I2C, safety switch, buzzer, LED). | `bug` if wrong, `style` if missing |
| T-GP2 | Links [mounting the GPS/compass](../assembly/mount_gps_compass.md) (or `../gps_compass/index.md`). | `style` |
| T-GP3 | When the full GPS port carries a safety switch, says how it behaves by default. | `minor` |
| T-GP4 | The onboard magnetometer, if any, and whether an external compass is expected for yaw. | `style` |

### Further Information {#further_information}

| ID | Check | Severity |
| --- | --- | --- |
| T-I1 | Links the manufacturer's own documentation, and the schematic or block diagram if T-P8 is met by a link. | `style` |
| T-I2 | For a board on a reference design, links the design's standard and the [Pixhawk Series](../flight_controller/pixhawk_series.md) or reference-design page where siblings do. | `minor` |
