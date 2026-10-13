# Rangefinder page template

The standard for a rangefinder page under `docs/en/sensor/` or `docs/en/dronecan/`: a skeleton page, then numbered checks.
Every lens cites the check ID (`R-W2`, `R-A1`, ...) in a finding's evidence, so the author can look the rule up.

Existing pages vary a lot and all of them predate this template, so it's the standard for new and changed pages, not a reason to report old ones.
Where two or more comparator pages agree on something this template does differently, report the finding and name the comparators below the tables, so the reviewer can judge which should change.

## Page kinds

Two things decide which parts of the template apply; the main agent records both in the rangefinder facts (`shared.md`).

**Single-model or family.**
A *single-model* page describes one rangefinder.
A *family* page describes several that share a driver, a manufacturer and most of their setup (the LightWare SF/LW range, the TeraRanger Evo range, the TFmini variants).
A family page uses the same skeleton plus `## Supported Models`, and says everything the models share once ("Family pages" below).

**Connection.**
Which interface carries the data decides what Wiring and PX4 Configuration must contain:

| Connection | Enabled by | Examples |
| --- | --- | --- |
| **Serial** (UART) | A `SENS_<X>_CFG` port parameter | PTGL-100, TFmini, LeddarOne, US-D1, LightWare serial |
| **I2C** | A `SENS_EN_<X>` parameter | Lidar-Lite, TeraRanger, LightWare I2C, VL53L1X |
| **PWM** | A `SENS_EN_<X>` parameter, on fixed pins | Lidar-Lite PWM |
| **DroneCAN** | `UAVCAN_ENABLE`, `UAVCAN_SUB_RNG`, `UAVCAN_RNG_MIN`/`MAX` | ARK DIST, Smartmicro Drone Altimeter |
| **MAVLink** | A `MAV_X_CONFIG` port | ARK DIST over UART |

A rangefinder with more than one connection gets one sub-section per connection (R-W6, R-A7).

## Skeleton

Sections appear in this order.
A section marked *(if present)* is left out when it doesn't apply; everything else is always present.
The sentences shown are the standard wording: use them as written, with the brackets filled in.

````md
# <Manufacturer> <Model> <Kind>

<Badge type="tip" text="PX4 v1.xx" />

The [<Manufacturer> <Model>](<product url>) is a <technology> [rangefinder](../sensor/rangefinders.md) with a range of <min>–<max> m and a <rate> Hz update rate.
It connects to the flight controller using <connection>.
<What PX4 uses it for, or what sets it apart>.

![<Model>](../../assets/hardware/sensors/<page-stem>/<image>.jpg)

::: info
The driver is not included in the firmware for most boards.
See [Firmware Support](#firmware_support) for how to check your board and add it.
:::                                                    (if the driver isn't in the common set)

## Supported Models {#supported_models}               (family pages)

| Model | Range | Connection | <parameter> value | Notes |
| ----- | ----- | ---------- | ----------------- | ----- |

## Specifications {#specifications}

- **Technology:**
- **Range:**
- **Update rate:**
- **Field of view:**
- **Accuracy:**
- **Interface:**
- **Input voltage:**
- **Current draw:**
- **Dimensions:**
- **Weight:**

## Where to Buy {#store}

## Sensor Configuration {#sensor_configuration}       (if the sensor itself has to be set up)

## Hardware Setup {#hardware_setup}

### Mounting {#mounting}

### Pinouts {#pinouts}

### Wiring {#wiring}

The <Model> can be connected to any unused serial port (UART), such as `TELEM2`, `TELEM3` or `GPS2`.

| <Model> pin | Signal | Connect to |
| ----------- | ------ | ---------- |

## Firmware Support {#firmware_support}

The rangefinder is supported by the [<driver>](../modules/modules_driver_distance_sensor.md#<driver>) driver, which is built into firmware by either of the following [board configuration](../hardware/porting_guide_config.md) keys:

- `CONFIG_COMMON_DISTANCE_SENSOR=y`: the common set of rangefinder drivers, which includes this one.
- `CONFIG_DRIVERS_DISTANCE_SENSOR_<X>=y`: this driver on its own.

Most boards set `CONFIG_COMMON_DISTANCE_SENSOR`, so the driver is present in most firmware.
To check your board, look for either key in its configuration file, `boards/<vendor>/<board>/default.px4board`, or check whether [SENS_<X>_CFG](../advanced_config/parameter_reference.md#SENS_<X>_CFG) is listed in _QGroundControl_ (parameters are only shown for drivers that are in the firmware).

If the driver is missing, add either key to the board's `default.px4board` file, or enable it in [boardconfig](../hardware/porting_guide_config.md#px4-menuconfig-setup) under **Drivers > Distance sensors**, and then [build and upload the firmware](../dev_setup/building_px4.md).

The driver does not start until it is enabled using the parameters in [PX4 Configuration](#px4_configuration).

## PX4 Configuration {#px4_configuration}

[Configure the serial port](../peripherals/serial_configuration.md) on which the rangefinder will run using [SENS_<X>_CFG](../advanced_config/parameter_reference.md#SENS_<X>_CFG), and then reboot.
There is no need to set the baud rate for the port, as this is configured by the driver.

If the parameter is not available in _QGroundControl_ then the driver is not in the firmware: see [Firmware Support](#firmware_support).

The configuration that is common to all rangefinders, such as the sensor position offsets used by the estimator, is covered in [Rangefinders > Configuration/Setup](../sensor/rangefinders.md#configuration).

## Testing {#testing}

## Troubleshooting {#troubleshooting}                 (if present)

## Developer Information {#developer_information}     (if present)

## Further Information {#further_information}
````

The Wiring and PX4 Configuration text above is the serial form; "Section checks" gives what the other connections need in its place.

The Firmware Support text above is for a driver in the common set.
For a driver that isn't, the key list has one entry and the paragraph after it reads:

```md
The driver is built into firmware by the [board configuration](../hardware/porting_guide_config.md) key `CONFIG_DRIVERS_DISTANCE_SENSOR_<X>=y`.
It is not part of the common set of rangefinder drivers (`CONFIG_COMMON_DISTANCE_SENSOR`), so it is only present in the firmware for boards that set that key.
At the time of writing these are: <boards, each linked to its page>.
```

### In common with flight-controller pages

Where a section means the same as one on a flight-controller page, it has the same heading and the same anchor as `px4-board-doc-review`'s template, so links and readers carry over.
Keep them identical when either template changes.

| Heading | Shared with the board template |
| --- | --- |
| `## Specifications {#specifications}` | Yes, in the same position (directly after the opening, before Where to Buy), and the labels they share: **Input voltage:**, **Current draw:**, **Dimensions:**, **Weight:**, in the same `- **Label:** value` form |
| `## Where to Buy {#store}` | Yes |
| `### Pinouts {#pinouts}` | Same heading and anchor; a `###` here because it sits under Hardware Setup |
| `## Further Information {#further_information}` | Yes |
| Version badge, hero image, explicit anchors on every skeleton heading | Yes, same form |
| `## Firmware Support {#firmware_support}` | No: the board template's `## Building Firmware {#building_firmware}` is how to build a board's target, which is a different thing, so it keeps a different name and anchor |

## Page-wide checks

| ID | Check | Severity if failed |
| --- | --- | --- |
| R-P1 | Headings are exactly as in the skeleton, including the explicit anchor. A heading with the right meaning but different words, level or anchor (`## Parameter Setup`, `## Software Configuration`, `## Viewing Data`, a top-level `## Wiring`) is reported with the exact heading as the suggestion. When the suggestion changes a heading's level, say where the headings that follow it go. | `style` |
| R-P2 | Sections are in skeleton order. Report the first out-of-order section only. | `minor` |
| R-P3 | No `TODO`, `TBD` or placeholder text or URL (`example.com`, `<Model>`, `xxx`) anywhere on the rendered page, and no heading with nothing under it. | `bug` |
| R-P4 | No leftover HTML comments holding guidance or notes to self (`<!-- Would be good to show serial setup! -->`). A section holding only a `<!-- placeholder ... -->` stub ("Stubs for missing sections" below) is reported as the missing content it stands in for. | `style` |
| R-P5 | Every image is local: `../../assets/hardware/sensors/<folder>/<file>`, in a folder named for the page stem (or the manufacturer's shared folder, for a family), the file name lower case with underscores. No image loaded from a URL. | `style`; a URL image is `bug` |
| R-P6 | Every referenced image exists in the PR or the repository. | `bug` |
| R-P7 | Flight-controller port names are in code style and written as printed on the board (`TELEM2`, `GPS2`, `I2C`, `CAN1`), the same way everywhere on the page. Sensor pin names in a pinout or wiring table stay plain. | `style` |
| R-P8 | Every skeleton heading on the page has its explicit anchor, as "Anchors" below gives it. A heading that isn't in the skeleton needs no anchor. | `style` |
| R-P9 | Adding or changing an anchor on an existing page doesn't break links to it: every link to the old slug elsewhere in `docs/en/` and on the page itself is updated in the same PR. | `bug` per link left broken |
| R-P10 | Each fact is given the same way everywhere it appears: the range, update rate and connection in the opening, Specifications, Supported Models, and the `rangefinders.md` row and summary all agree. | `bug` |
| R-P11 | Every parameter is named in full and linked to `../advanced_config/parameter_reference.md#<NAME>` where it's first used in each section. | `style` |

### Stubs for missing sections

When a skeleton section is missing, the report suggests a stub the author can paste in: the heading with its anchor, then a placeholder comment saying what goes there and pointing at good examples.

```md
### Wiring {#wiring}

<!-- placeholder
Which flight-controller port to use, then a table: sensor pin, signal, what it connects to. Driver sends commands, so both TX and RX are needed. Say whether the port can power the sensor (manufacturer: supply voltage and current).
Good examples: sony_asdt1.md#hardware-setup
-->
```

- **What goes there**: one or two lines, filled with this rangefinder's own values from the facts worksheet wherever the driver gives them (parameter names, baud rate, Kconfig key, range limits), and naming what only the manufacturer can supply otherwise (pinout, supply voltage, dimensions).
- **Good examples**: two or three pages from "Example sections" below, preferring a comparator page when it has a good version of the section. Links are page-relative, and the anchor must exist on that page: check it before citing.
- **Order**: stubs go where the skeleton puts them, one block per run of adjacent missing sections, keyed to the line it goes after.
- **Leave out** a section marked *(if present)* unless the driver source shows it applies.

#### Example sections

Good current versions of each section, as starting points for the "Good examples" line.
Re-check them occasionally: pages get rewritten.

| Section | Examples |
| --- | --- |
| Supported Models | `sfxx_lidar.md#supported-models` |
| Specifications | `../dronecan/smartmicro_t132.md#hardware-specifications`, `../dronecan/ark_dist.md#hardware-specifications` |
| Sensor Configuration | `sf45_rotating_lidar.md#lightware-studio-setup`, `sfxx_lidar.md#lidar-configuration-sf11-c` |
| Pinouts | `lidar_lite.md#pinouts`, `../dronecan/avanon_laser_interface.md#pinouts` |
| Wiring (serial) | `sony_asdt1.md#hardware-setup` |
| Wiring (DroneCAN) | `../dronecan/ark_dist.md#wiring`, `../dronecan/smartmicro_t132.md#wiring` |
| Firmware Support | `grf_lidar.md#add-the-driver-to-the-px4-build` (for adding the key; no page yet has the whole section) |
| Parameters (serial) | `grf_lidar.md#parameter-configuration`, `sony_asdt1.md#parameter-setup` |
| Parameters (DroneCAN) | `../dronecan/smartmicro_t132.md#px4-configuration` |
| Testing | `sony_asdt1.md#testing`, `grf_lidar.md#testing` |
| Troubleshooting | `sf45_rotating_lidar.md#troubleshooting` |

### Anchors

Skeleton headings carry an explicit anchor, so links to the sections every rangefinder page shares survive rewording and translation.

- **Skeleton headings** use the anchor shown in the skeleton, exactly.
  `{#store}` is an established short form and must not be "corrected".
  Headings shared with the flight-controller template use its anchors ("In common with flight-controller pages" above).
- **Any other heading** doesn't need an anchor, and a missing one is not a finding.
  An anchor the author does give it is made from its text: lower case, words joined by underscores, punctuation and parenthetical qualifiers dropped.
- **Per-connection sub-sections** (R-W6, R-A7) take the parent's anchor as a prefix: `#### Serial {#wiring_serial}`, `### Serial {#px4_configuration_serial}`.
- **Separate anchor tags**: an `<a id="..."></a>` on its own line just before a heading is `style`.
  The suggestion moves the id into the heading as `{#...}`, keeping the same id so links to it still work.
  An `<a id>` inside a parameter table cell stays.
- **Unique on the page**: two headings with the same anchor are `bug`.
- **Hyphenated anchors** are `style`: PX4 anchors use underscores.

To find links to an old slug before accepting a changed anchor (R-P9), search from `docs/en/`: `grep -rn "<page>.md#<old-slug>" --include=*.md .` and `grep -n "](#<old-slug>)" <page>.md`.
The old slug of a heading with no explicit anchor is its text, lower case, with spaces as hyphens and punctuation dropped (`Parameter Setup` → `parameter-setup`).

## Family pages

A family page describes several models at once.
The aim is that a reader with any one of them can follow the page without guessing which lines apply.

| ID | Check | Severity |
| --- | --- | --- |
| R-M1 | `## Supported Models {#supported_models}` directly after the opening, as one table with a row per model: `Model` (linked to its product page, or to its own page if it has one), `Range`, `Connection`, the value of the model parameter when the driver selects the model by parameter (the column headed with the parameter name), and `Notes`. | `style` |
| R-M2 | Every model the page names is in the table, and is one the driver supports for that connection (its model parameter has a value for it, or the driver detects it). | `bug` for a model the driver doesn't support |
| R-M3 | Every model the driver supports is in the table, or the page says why not. | `style` |
| R-M4 | Each row's range, connection and parameter value match the driver (`driver-sources.md`, "Models"). | `bug` |
| R-M5 | Discontinued models are in a `::: details Discontinued` block after the table, in a table with the same columns. | `style` |
| R-M6 | **Shared content is written once.** Every section applies to all models unless it says otherwise. A step only some models need names them where it appears, in the heading (`### Sensor Configuration (SF11/C)`) or the sentence ("SF11/C only: ..."). | `style` |
| R-M7 | **Differences are never left implicit.** Where models differ in connection, baud rate, I2C address, parameter value, wiring or power, the page says which model gets which. | `bug` when a reader can't tell which instruction applies to their model |
| R-M8 | A model that needs a different driver or a substantially different setup has its own page, which follows this template as a single-model page, is linked from the Supported Models table, and is nested under the family page in `SUMMARY.md`. The family page doesn't repeat its setup. | `style` |
| R-M9 | The Specifications list holds what the models share; what differs by model is a column of the Supported Models table. | `style` |

A page that covers two near-identical products with one line of difference (ARK DIST SR and MR differ only in range) can be either one family page or two pages; when it's two, they should be word-for-word the same outside the differing facts (`sibling-comparison.md`).

## Section checks

### Opening

| ID | Check | Severity |
| --- | --- | --- |
| R-O1 | One H1, `# <Manufacturer> <Model> <Kind>` (`# JRT PTGL-100 Laser Rangefinder`), naming the product the same way as the `SUMMARY.md` entry and the `rangefinders.md` row. | `style` |
| R-O2 | `<Badge type="tip" text="..." />` directly under the H1, naming the first PX4 release that supports the rangefinder, in the form the flight-controller pages use (`grep -rho '<Badge type="tip" text="[^"]*"' docs/en/flight_controller/`): `main (PX4 vX.Y)` for one not yet in a release. Expected on every new page; on an existing page only when the PR adds it or changes the driver's first release. | `minor` |
| R-O3 | The first paragraph names the manufacturer and model, links the product page, and gives the technology (laser ToF, infrared ToF, radar, ultrasonic), the range as minimum and maximum, the update rate, and the connection. | `bug` if wrong, `style` if missing |
| R-O4 | Says what the data is for, matching what the driver publishes: a rangefinder publishing `distance_sensor` links [Distance Sensors (Rangefinders)](../sensor/rangefinders.md); one publishing `obstacle_distance` says it's for [Collision Prevention](../computer_vision/collision_prevention.md) and doesn't offer it for terrain following or landing. | `bug` if wrong, `style` if missing |
| R-O5 | A hero photo of the sensor, after the opening paragraph, stored locally (R-P5). Expected on every page. | `style` |
| R-O6 | When the driver isn't in the common set (`driver-sources.md`, "In firmware"), the info note from the skeleton, linking `#firmware_support`. A page that reads as though the driver is always present when it isn't is the `bug` case: the reader looks for a parameter that isn't there. | `bug` or `style` |
| R-O7 | A discontinued product has ` (Discontinued)` in the H1, `<Badge type="info" text="Discontinued" />` under it, and a `::: warning` saying it's no longer available and, if stock exists, where. | `style` |
| R-O8 | A "tested on" statement, when there is one, names the board and is in an `::: info` note; it doesn't stand in for R-O6. | `minor` |
| R-O9 | When the manufacturer sells the sensor in interface variants that a unit is configured as at the factory (UART, CAN or DroneCAN), the page says which variant it documents, in a note where the reader meets the wiring, and Where to Buy says which to order when the store offers the choice. | `bug` if the page's setup only works for one variant and nothing says so, otherwise `style` |

### Specifications {#specifications}

| ID | Check | Severity |
| --- | --- | --- |
| R-S1 | A list in the `- **Label:** value` form, colon inside the bold, in this order, each one the manufacturer gives: **Technology:**, **Range:**, **Update rate:**, **Field of view:** (or **Beam divergence:**), **Accuracy:**, **Resolution:**, **Interface:** (with the serial settings or I2C address), **Input voltage:**, **Current draw:** (or **Power consumption:** when the manufacturer gives watts; don't convert), **Dimensions:**, **Weight:**, **Operating temperature:**, **Ingress protection:**, **Laser class:** for a laser, **NDAA compliant:** when the manufacturer claims it. | `style` if missing |
| R-S2 | Each value matches the manufacturer material the page links. | `bug` |
| R-S3 | The range PX4 reports is the driver's (`driver-sources.md`, "Range"). When the driver's limits differ from the manufacturer's figure, the page gives both ("0.17–8 m; PX4 uses 0.2–7.9 m"). | `bug` if the page promises a range the driver won't report and nothing sources it; otherwise a note below the tables |
| R-S5 | Labels the flight-controller template also has are spelled as it spells them: **Input voltage:** (not "Supply voltage" or "Power"), **Current draw:**, **Dimensions:**, **Weight:**. | `style` |
| R-S4 | Units carry a space and ranges use an en dash with the unit once (`0.2–100 m`, `100 Hz`, `460800 baud`). | `style` |

A page can add an item the list doesn't have; it goes in the same form.
A flat marketing list in place of Specifications (`- Unbreakable, lightweight design`) is one finding on its first line (R-S1), with the restructured list written out below the tables, keeping every fact.

### Where to Buy {#store}

| ID | Check | Severity |
| --- | --- | --- |
| R-B1 | A link to where each model can be bought (manufacturer store or listed resellers). A discontinued product says so here instead. | `style`; a placeholder link is `bug` (R-P3) |

### Sensor Configuration {#sensor_configuration} (if present)

Settings made on the sensor itself, with the manufacturer's tool or by updating its firmware.

| ID | Check | Severity |
| --- | --- | --- |
| R-C1 | Present when the sensor has to be changed from its factory state to work with PX4: a baud rate the driver expects but doesn't set, an output mode or protocol, an I2C compatibility mode or address. Names the tool, links it, and gives each setting and its value. | `bug` if the driver needs a setting it doesn't make itself and the page doesn't give it |
| R-C2 | A baud rate, mode or address given here matches the driver (`driver-sources.md`, "Baud rate", "I2C address"). | `bug` |
| R-C3 | For a DroneCAN node: what firmware it runs, how it's updated, and a link to [PX4 DroneCAN Firmware](../dronecan/px4_cannode_fw.md) when it runs that. | `style` |

### Hardware Setup {#hardware_setup}

| ID | Check | Severity |
| --- | --- | --- |
| R-H1 | `### Mounting {#mounting}`: which way the sensor faces by default (downward, unless the driver says otherwise), how to mount it facing another way and whether the driver supports that, and anything that must stay clear of the beam. | `style` if missing |
| R-H2 | Orientation claims match the driver: its orientation parameter and default, or that the direction is fixed (`driver-sources.md`, "Orientation"). | `bug` |
| R-N1 | `### Pinouts {#pinouts}`: the sensor's connector type and a table of pin, signal and voltage, or a link to the manufacturer document that gives them. A photo of the connector is not a pinout. One table per connector when there are several. | `bug` when the page neither gives nor links one |
| R-W1 | `### Wiring {#wiring}` names the kind of flight-controller port to use, with example port labels in code style: the standard serial sentence from the skeleton; the `I2C` port for an I2C sensor; a `CAN` port and a link to [CAN Wiring](../can/index.md#wiring) for DroneCAN. | `style` if missing, `bug` if wrong |
| R-W2 | A table of sensor pin, signal, and what it connects to, with TX and RX crossed for serial. Says whether both TX and RX are needed (the driver sends commands) or RX alone will do. | `bug` if wrong; `style` if missing when R-N1 is met |
| R-W3 | **Power**: the supply voltage and current the sensor needs, whether a flight-controller port can supply it or it needs its own supply, and the signal voltage level when it isn't 3.3 V. | `bug` if it contradicts the manufacturer or the page's own Specifications, `style` if missing |
| R-W4 | An I2C sensor gives its address, and says so if the address can clash with another PX4 device or can be changed. | `bug` if wrong, `minor` if missing |
| R-W5 | A PWM sensor names the pins the driver uses and says they're fixed. | `bug` if wrong |
| R-W6 | A sensor with more than one connection has one `####` sub-section per connection under Wiring, named for it (`#### I2C {#wiring_i2c}`, `#### Serial {#wiring_serial}`), in the order the opening lists them. | `style` |

Mounting, Pinouts and Wiring can be one `## Hardware Setup` section with no sub-headings when the whole of it is a few lines, as long as R-H1, R-N1 and R-W1 to R-W3 are covered.

### Firmware Support {#firmware_support}

Every rangefinder that needs a driver in the flight controller's firmware has this section, whether or not the driver is in most builds: it's where a reader finds out if their board already supports the sensor, and what to do if it doesn't.
The values come from the facts worksheet (`driver-sources.md`, "In firmware").

| ID | Check | Severity |
| --- | --- | --- |
| R-F1 | The section exists, as `## Firmware Support {#firmware_support}`, between Hardware Setup and PX4 Configuration. | `style` if missing; `bug` if missing and the driver isn't in the common set |
| R-F3 | **The driver**: named, and linked to its module reference. | `style` |
| R-F4 | **The keys**: every board configuration key that builds the driver, each in code style with `=y`. That's the driver's own key, `CONFIG_DRIVERS_DISTANCE_SENSOR_<X>`, and also `CONFIG_COMMON_DISTANCE_SENSOR` when the common set selects the driver. The page says what each is: the common set, or this driver alone. | `bug` for a key that's wrong, in an obsolete form (`distance_sensor/cm8jl65`, `drivers/ll40ls`), or a common-set key given for a driver the set doesn't select; `style` for a key left out |
| R-F5 | **How widely it's built**, following from which key applies: in the common set, "most boards" (the standard sentence); not in it, that only boards setting the driver's own key have it, naming them, each linked to its flight-controller page. | `bug` if it says "most boards" for a driver outside the common set, or the reverse; `bug` for a named board that doesn't build it; `style` if missing |
| R-F6 | **How to check a board**: look for the key(s) in `boards/<vendor>/<board>/default.px4board`, or see whether the enabling parameter is listed in _QGroundControl_. | `style` |
| R-F7 | **How to add it**: add a key to the board's `default.px4board`, or enable the driver in [boardconfig](../hardware/porting_guide_config.md#px4-menuconfig-setup) under **Drivers > Distance sensors**, then [build and upload](../dev_setup/building_px4.md). | `style` if missing, `bug` if the menu path or key is wrong |
| R-F8 | **How it's enabled**: says that being in firmware doesn't start the driver, and links PX4 Configuration for the parameter that does. A driver a board starts by itself (a line in its `rc.board_sensors`) says so, naming the board. | `style`; `bug` if it says the driver starts automatically when it doesn't |
| R-F9 | A sensor with several drivers (one per connection) lists each driver with its own keys, and says which connection each serves. | `bug` when a reader can't tell which key their connection needs |
| R-F10 | A DroneCAN or MAVLink sensor has no driver of its own in the flight controller. The section says so in a line, and names what the flight controller does need: the DroneCAN driver (`CONFIG_DRIVERS_UAVCAN=y`, in most boards) or MAVLink on the port. The sensor's own firmware is covered in Sensor Configuration (R-C3). | `style` |

### PX4 Configuration {#px4_configuration}

| ID | Check | Severity |
| --- | --- | --- |
| R-A1 | Gives the parameter that enables the sensor and what to set it to, for the page's connection: the `SENS_<X>_CFG` port parameter with a link to [Serial Port Configuration](../peripherals/serial_configuration.md); the `SENS_EN_<X>` parameter and its value; or, for DroneCAN, [UAVCAN_ENABLE](../advanced_config/parameter_reference.md#UAVCAN_ENABLE), [UAVCAN_SUB_RNG](../advanced_config/parameter_reference.md#UAVCAN_SUB_RNG), and [UAVCAN_RNG_MIN](../advanced_config/parameter_reference.md#UAVCAN_RNG_MIN) and [UAVCAN_RNG_MAX](../advanced_config/parameter_reference.md#UAVCAN_RNG_MAX) set to this sensor's range, with a link to [DroneCAN > Distance Sensor](../dronecan/index.md#distance-sensor-range-finder). | `bug` if wrong or missing |
| R-A9 | Says that if the enabling parameter isn't listed in _QGroundControl_ the driver isn't in the firmware, and links `#firmware_support` (the sentence from the skeleton) in place of the older "add the driver to the firmware" info note. | `style` |
| R-A2 | Says whether the port's baud rate has to be set. When the driver sets it, the standard sentence from the skeleton; when it doesn't, the `SER_<port>_BAUD` value. | `bug` if wrong, `style` if missing |
| R-A3 | Every other parameter the driver defines (model, orientation, rate, mode) is listed with what it does and when to change it, and any default the page states is the driver's. Several parameters go in a table, `Parameter` and `Description`. | `bug` if wrong, `style` for a driver parameter the page doesn't mention |
| R-A4 | Says to reboot after setting any parameter the driver marks `reboot_required`, and that a serial port already assigned to another service has to be freed first, linking Serial Port Configuration. | `style` |
| R-A5 | Links [Rangefinders > Configuration/Setup](../sensor/rangefinders.md#configuration) for the `EKF2_RNG_*` parameters every rangefinder shares, using the sentence from the skeleton, instead of repeating them. A value this sensor needs that differs from the default ([EKF2_RNG_QLTY_T](../advanced_config/parameter_reference.md#EKF2_RNG_QLTY_T) for DroneCAN sensors) is given here. | `style` |
| R-A6 | A sensor publishing `obstacle_distance` links [Collision Prevention](../computer_vision/collision_prevention.md) and [CP_DIST](../advanced_config/parameter_reference.md#CP_DIST), and leaves out R-A5. | `style` |
| R-A7 | A sensor with more than one connection has one `###` sub-section per connection under PX4 Configuration (`### I2C {#px4_configuration_i2c}`), in the same order as under Wiring. | `style` |
| R-A8 | Steps that must be done in order are a numbered list. | `minor` |

### Testing {#testing}

| ID | Check | Severity |
| --- | --- | --- |
| R-T1 | Says how to confirm the sensor works: the driver's `status` command and `listener distance_sensor` (or `listener obstacle_distance`) in the MAVLink Console, or the `DISTANCE_SENSOR` (or `OBSTACLE_DISTANCE`) message in the MAVLink Inspector. | `style` if missing |
| R-T2 | Links [Rangefinders > Testing](../sensor/rangefinders.md#testing) for the generic steps instead of repeating them; what's written here is what's particular to this sensor. | `minor` |
| R-T3 | Every command, option, topic and message named exists (`driver-sources.md`, "Commands", "Topic"). | `bug` |

### Troubleshooting {#troubleshooting} (if present)

| ID | Check | Severity |
| --- | --- | --- |
| R-X1 | One `###` per problem, named for the symptom. Commands and parameters named exist. | `bug` if a command or parameter doesn't exist |

### Developer Information {#developer_information} (if present)

| ID | Check | Severity |
| --- | --- | --- |
| R-D1 | Names the driver and links its module reference, `../modules/modules_driver_distance_sensor.md#<driver>`, and the uORB topic it publishes. | `style` |
| R-D2 | What only a driver developer needs (protocol details, running the driver by hand, diagnostics counters) is here, after everything a user needs, and not mixed into the sections above. | `style` |
| R-D3 | Unit-test and build commands, and byte-level protocol tables that restate the driver source, are better kept with the driver. | `minor` |
| R-D4 | What it says about the driver's behaviour matches the source. | `bug` |

### Further Information {#further_information}

| ID | Check | Severity |
| --- | --- | --- |
| R-I1 | Links the module reference for each driver the page uses, and the manufacturer's manual or datasheet. | `style` |
| R-I2 | The manual and datasheet links are the current revisions, the ones the manufacturer's product page links now. A link that still resolves but is a superseded revision is the `style` case; say which revision is current. | `style`; `bug` if the link is dead |

## Listings

Where a rangefinder page has to be listed; `completeness.md` applies these.

| ID | Check | Severity |
| --- | --- | --- |
| R-L1 | An entry in `docs/en/SUMMARY.md` under `Distance Sensors \(Rangefinders\)`, with the H1's product name as link text, in alphabetical order by manufacturer among the current products. A model page is nested under its family page. A discontinued product has a `✘ ` prefix and sits after the current ones. A DroneCAN product ends ` (CAN)`. | `bug` if missing, `style` for form or order |
| R-L2 | A row in the Supported Rangefinders table of `docs/en/sensor/rangefinders.md`, with all of `Rangefinder`, `Technology`, `Range (min – max)`, `Connections`, `NDAA` and `Notes`, and its link reference definition below the table. One row per model for a family page. Alphabetical by name; a discontinued product is marked `_(disc.)_` with `Discontinued` in Notes and sits with the other discontinued rows. | `bug` if missing, `style` for form or order |
| R-L3 | A `### <Name>` summary under the table in `rangefinders.md`: two or three sentences giving what it is, its range and connection, linked to the page. | `style` |
| R-L4 | The row and the summary agree with the page and the driver on range, technology, connection and update rate (R-P10). | `bug` |
| R-L5 | A DroneCAN rangefinder is listed under "Distance sensors" in `docs/en/dronecan/index.md`. | `style` |
| R-L6 | A sensor publishing `obstacle_distance` is listed under [Supported Rangefinders](../computer_vision/collision_prevention.md#rangefinder) in `collision_prevention.md`. | `style` |
| R-L7 | The `NDAA` cell is `✔️` only when the page says the manufacturer claims compliance, `✖️` only when it's known not to be, and `~` otherwise. | `bug` for a `✔️` nothing backs |
