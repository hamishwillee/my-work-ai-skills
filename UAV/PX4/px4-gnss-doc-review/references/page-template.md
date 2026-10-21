# GNSS page template

The standard for a GNSS receiver page under `docs/en/gps_compass/` or `docs/en/dronecan/`: a skeleton page, then numbered checks.
Every lens cites the check ID (`G-A1`, `G-L2`, ...) in a finding's evidence, so the author can look the rule up.

Existing pages vary a lot and all of them predate this template, so it's the standard for new and changed pages, not a reason to report old ones.
Where two or more comparator pages agree on something this template does differently, report the finding and name the comparators below the tables, so the reviewer can judge which should change.

## Page kinds

Four things decide which parts of the template apply; the main agent records them in the GNSS facts (`shared.md`).

**Single-product or family.**
A *single-product* page describes one receiver.
A *family* page describes several that share a manufacturer and most of their setup (an M8N and an M9N version of one module, a range of Septentrio receivers).
A family page uses the same skeleton plus `## Supported Models`, and says everything the products share once ("Family pages" below).

**Connection.**

| Connection | Enabled by | Examples |
| --- | --- | --- |
| **UART** (`gps` driver) | `GPS_1_CONFIG` (defaults to `GPS1`) and, for any protocol but u-blox, `GPS_1_PROTOCOL` | ARK DAN, Holybro M9N, GlobalSat BD-100M, Holybro UM982 |
| **UART-Septentrio** (`septentrio` driver) | `SEP_PORT1_CFG`, with `GPS_1_CONFIG` disabled on that port | Septentrio mosaic-go, AsteRx-m3 Pro |
| **DroneCAN** | `UAVCAN_ENABLE`; `UAVCAN_PUB_RTCM` for RTK | ARK GPS, ARK RTK GPS, Holybro H-RTK ZED-F9P (DroneCAN) |

A receiver with more than one connection (a unit with both UART and CAN, or sold in either variant) gets one sub-section per connection (G-W5, G-A9).

**Protocol** (UART only): u-blox, which PX4 uses by default, or another protocol, which the reader has to select and which some firmware leaves out (`protocol-sources.md`, "Protocol and detection").

**Capability**: GNSS, RTK, or RTK heading (dual antenna or moving base).
RTK content is required only for RTK receivers, heading content only for heading-capable ones.

## Skeleton

Sections appear in this order.
A section marked *(if present)* is left out when it doesn't apply; everything else is always present.
The sentences shown are the standard wording: use them as written, with the brackets filled in.

````md
# <Manufacturer> <Product> <GPS | RTK GPS | GNSS>

<Badge type="tip" text="PX4 v1.xx" />                     (only when G-O2 asks for one)

The [<Manufacturer> <Product>](<product url>) is a <bands> <GNSS | RTK GNSS> receiver <with dual-antenna heading> that connects to the flight controller using <UART | DroneCAN>.
It <is based on the <receiver chip> and> includes <a compass, barometer, safety switch, buzzer and LED>.
<What sets it apart.>

![<Manufacturer> <Product>](../../assets/hardware/gps/<folder>/<image>.jpg)

## Supported Models {#supported_models}                   (family pages)

## Specifications {#specifications}

- **Receiver:**
- **Constellations:**
- **Bands:**
- **Protocol:**
- **Update rate:**
- **Position accuracy:**
- **Heading accuracy:**                                    (heading receivers)
- **Compass:**
- **Barometer:**
- **Other:**                                               (safety switch, buzzer, LED)
- **Antenna:**
- **Interface:**
- **Input voltage:**
- **Current draw:**
- **Dimensions:**
- **Weight:**

## Where to Buy {#store}

## Receiver Configuration {#receiver_configuration}         (if the receiver itself has to be set up)

## Hardware Setup {#hardware_setup}

### Mounting {#mounting}

Mount the receiver with its arrow pointing towards the front of the vehicle, as far away from the flight controller and other electronics as possible.
For more information, see [Mounting a Compass](../assembly/mount_gps_compass.md).

### Pinouts {#pinouts}

### Wiring {#wiring}

Connect the receiver to the 10-pin `GPS1` port on flight controllers that use the [Pixhawk Connector Standard](https://github.com/pixhawk/Pixhawk-Standards/blob/master/DS-009%20Pixhawk%20Connector%20Standard.pdf) (the "Full GPS + Safety Switch Port").

## Firmware Support {#firmware_support}                     (if the protocol or driver isn't in every build)

## PX4 Configuration {#px4_configuration}

## LED Meanings {#led_meanings}                             (if present)

## Testing {#testing}

## Troubleshooting {#troubleshooting}                       (if present)

## Further Information {#further_information}
````

The Wiring text above is for a UART receiver on a Pixhawk-standard `GPS1` port; "Section checks" gives what DroneCAN and other connectors need in its place.

### Standard wording

**PX4 Configuration, u-blox on UART:**

```md
The receiver uses the u-blox protocol, which PX4 uses by default.
When it is connected to the `GPS1` port it is detected and configured automatically, and no parameters need to be set.
```

**PX4 Configuration, a protocol other than u-blox** (`<n>` and `<label>` from `GPS_1_PROTOCOL`; the "not auto-detected" clause for NMEA only):

```md
PX4 communicates with this receiver using the <protocol> protocol<, which is not auto-detected>.
Set [GPS_1_PROTOCOL](../advanced_config/parameter_reference.md#GPS_1_PROTOCOL) to `<n>` (`<label>`) and reboot the vehicle.

Note that <protocol> support is not included in firmware for boards with constrained flash.
```

**Secondary receiver:**

```md
To use the receiver as a secondary GPS, set [GPS_2_CONFIG](../advanced_config/parameter_reference.md#GPS_2_CONFIG) to the port it is connected to<, and [GPS_2_PROTOCOL](../advanced_config/parameter_reference.md#GPS_2_PROTOCOL) to `<n>`>, and reboot.
See [Secondary GPS Configuration (UART)](../gps_compass/index.md#secondary-gps-configuration-uart) for more information.
```

**RTK:**

```md
For RTK setup, see [RTK GNSS](../gps_compass/rtk_gps.md).
```

**Heading** (`<value>` `2` for a receiver with two antennas, `1` for the rover of a moving-base pair; `protocol-sources.md`, "Heading"):

```md
To use the receiver as a heading source:

1. Set [SENS_GNSS0_HDG](../advanced_config/parameter_reference.md#SENS_GNSS0_HDG) to `<value>` (`<Dual antenna | Moving base rover>`) in the receiver's slot.
2. Set the antenna positions relative to the vehicle's centre of gravity: <the main antenna in [SENS_GNSS0_OFFX/Y/Z](../advanced_config/parameter_reference.md#SENS_GNSS0_OFFX) and the auxiliary antenna in [SENS_GNSS0_AUXX/Y/Z](../advanced_config/parameter_reference.md#SENS_GNSS0_AUXX) | each receiver's antenna in its own slot's SENS_GNSSn_OFFX/Y/Z>.
3. Set bit 3 ("Dual antenna heading") of [EKF2_GPS_CTRL](../advanced_config/parameter_reference.md#EKF2_GPS_CTRL) (for example, set it to `15`).

See [Configuring GPS as Yaw/Heading Source](../gps_compass/rtk_gps.md#configuring-gps-as-yaw-heading-source) for more information.
```

Say which physical antenna is the main (primary) and which the auxiliary (secondary), since the heading's direction depends on it.

**DroneCAN:**

```md
Enable DroneCAN by setting [UAVCAN_ENABLE](../advanced_config/parameter_reference.md#UAVCAN_ENABLE) to `2` (`Sensors Automatic Config`), and reboot.
The GNSS and compass subscriptions ([UAVCAN_SUB_GPS](../advanced_config/parameter_reference.md#UAVCAN_SUB_GPS), [UAVCAN_SUB_MAG](../advanced_config/parameter_reference.md#UAVCAN_SUB_MAG)) are enabled by default.
For RTK, also set [UAVCAN_PUB_RTCM](../advanced_config/parameter_reference.md#UAVCAN_PUB_RTCM) to `1`, so that the flight controller forwards RTCM corrections to the receiver.
<For heading, set [SENS_GNSS0_ID](../advanced_config/parameter_reference.md#SENS_GNSS0_ID) to the node's ID and set up heading as above; [UAVCAN_SUB_GPS_R](../advanced_config/parameter_reference.md#UAVCAN_SUB_GPS_R), which carries the heading, is on by default.>

For more information, see [DroneCAN > GPS](../dronecan/index.md#gps).
```

**Antenna position:**

```md
Set the position of the antenna relative to the vehicle's centre of gravity using [SENS_GNSS0_OFFX](../advanced_config/parameter_reference.md#SENS_GNSS0_OFFX), [SENS_GNSS0_OFFY](../advanced_config/parameter_reference.md#SENS_GNSS0_OFFY) and [SENS_GNSS0_OFFZ](../advanced_config/parameter_reference.md#SENS_GNSS0_OFFZ).
```

**Testing:**

```md
In the [QGroundControl MAVLink Console](../debug/mavlink_shell.md#qgroundcontrol-mavlink-console), run `gps status` to see the protocol, fix type and number of satellites, or `listener sensor_gnss` to see the published data.
<For RTK, `fix_type` is `5` for an RTK float solution and `6` for RTK fixed.>
<For heading, `listener vehicle_gnss_heading` shows the heading the estimator uses.>
```

### In common with other hardware pages

Where a section means the same as one on a flight-controller or rangefinder page, it has the same heading and the same anchor as `px4-board-doc-review`'s and `px4-rangefinder-doc-review`'s templates, so links and readers carry over.
Keep them identical when any of the templates changes.

| Heading | Shared with |
| --- | --- |
| `## Specifications {#specifications}` | Both, in the same position (directly after the opening, before Where to Buy), with the labels they share: **Input voltage:**, **Current draw:**, **Dimensions:**, **Weight:**, in the same `- **Label:** value` form |
| `## Where to Buy {#store}` | Both |
| `## Hardware Setup {#hardware_setup}`, `### Mounting {#mounting}`, `### Pinouts {#pinouts}`, `### Wiring {#wiring}` | The rangefinder template, with the same levels |
| `## Firmware Support {#firmware_support}` | The rangefinder template's meaning: whether the driver is in a board's firmware, and how to add it |
| `## PX4 Configuration {#px4_configuration}`, `## Testing {#testing}`, `## Troubleshooting {#troubleshooting}`, `## Further Information {#further_information}` | The rangefinder template; Further Information also the board template |
| `## Receiver Configuration {#receiver_configuration}` | The rangefinder template's `## Sensor Configuration {#sensor_configuration}`, renamed for receivers |
| Version badge, hero image, explicit anchors on every skeleton heading | Both, same form |

## Page-wide checks

| ID | Check | Severity if failed |
| --- | --- | --- |
| G-P1 | Headings are exactly as in the skeleton, including the explicit anchor. A heading with the right meaning but different words, level or anchor (`## Configuration`, `## Wiring and Connections`, `## Hardware Specifications`, `## See Also`, `## Purchase`) is reported with the exact heading as the suggestion. When the suggestion changes a heading's level, say where the headings that follow it go. | `style` |
| G-P2 | Sections are in skeleton order. Report the first out-of-order section only. | `minor` |
| G-P3 | No `TODO`, `TBD` or placeholder text or URL anywhere on the rendered page, and no heading with nothing under it. | `bug` |
| G-P4 | No leftover HTML comments holding guidance or notes to self. A section holding only a `<!-- placeholder ... -->` stub is reported as the missing content it stands in for. | `style` |
| G-P5 | Every image is local: `../../assets/hardware/gps/<folder>/<file>`, in a folder named for the manufacturer or product, the file name lower case. No image loaded from a URL, and no `<img>` tag where Markdown image syntax will do. Every image has alt text naming what it shows ("Pinout" alone doesn't). | `style`; a URL image is `bug` |
| G-P6 | Every referenced image exists in the PR or the repository (on a local branch, is tracked or staged, not just on disk). | `bug` |
| G-P7 | Flight-controller port names are in code style and written as printed on the board (`GPS1`, `GPS2`, `CAN1`), the same way everywhere on the page. Module pin names in a pinout table stay plain. | `style` |
| G-P8 | Every skeleton heading on the page has its explicit anchor, as "Anchors" below gives it. A heading that isn't in the skeleton needs no anchor. | `style` |
| G-P9 | Adding or changing an anchor on an existing page doesn't break links to it: every link to the old slug elsewhere in `docs/en/` and on the page itself is updated in the same PR. | `bug` per link left broken |
| G-P10 | Each fact is given the same way everywhere it appears: the receiver, capability and connection in the opening, Specifications, Supported Models, and the device-table row agree. | `bug` |
| G-P11 | Every parameter is named in full and linked to `../advanced_config/parameter_reference.md#<NAME>` where it's first used in each section, and the link text names the same parameter as the anchor. | `style`; a link whose text and anchor name different parameters is `bug` |
| G-P12 | Two pages (or two sections) that show the same image use one shared file, not byte-identical copies. | `minor` |
| G-P13 | Store and product links carry no search or tracking parameters (`ref=`, `crid=`, `qid=`, `utm_*`): use the product's canonical URL (`https://www.amazon.com/dp/<ASIN>`). | `minor` |
| G-P14 | **File name.** A new RTK receiver page under `docs/en/gps_compass/` is named `rtk_gps_<manufacturer>_<product>.md`, lower case, words joined by underscores, as its siblings are (`rtk_gps_freefly.md`, `rtk_gps_holybro_unicore_um982.md`, `rtk_gps_trimble_mb_two.md`). The suggestion gives the new name and every link to update (`SUMMARY.md`, the `rtk_gps.md` row and any other page linking it). Don't report an existing page: renaming one breaks links from translations and outside sites. | `style` |

### Stubs for missing sections

When a skeleton section is missing, the report suggests a stub the author can paste in: the heading with its anchor, then a placeholder comment saying what goes there and pointing at good examples.

```md
## PX4 Configuration {#px4_configuration}

<!-- placeholder
NMEA receiver: GPS_1_PROTOCOL must be set to 6 (NMEA is never auto-detected). Use the standard wording in the template. RTK: link rtk_gps.md.
Good examples: rtk_gps_holybro_unicore_um982.md#px4-configuration, rtk_gps_trimble_mb_two.md#configuration
-->
```

- **What goes there**: one or two lines, filled with this receiver's own values from the facts worksheet wherever the source gives them (protocol value, Kconfig key, parameter names), and naming what only the manufacturer can supply otherwise (pinout, supply voltage, dimensions).
  Where the standard wording above applies, the stub is that wording, filled in, not a placeholder.
- **Good examples**: two or three pages from "Example sections" below, preferring a comparator page when it has a good version of the section. Links are page-relative, and the anchor must exist on that page: check it before citing.
- **Order**: stubs go where the skeleton puts them, one block per run of adjacent missing sections, keyed to the line it goes after.
- **Leave out** a section marked *(if present)* unless the facts show it applies.

#### Example sections

Good current versions of each section, as starting points for the "Good examples" line.
Re-check them occasionally: pages get rewritten, and several have known problems (`existing-page-issues.md`).

| Section | Examples |
| --- | --- |
| Specifications | `ark_dan_gps.md#hardware-specifications`, `../dronecan/ark_rtk_gps.md#hardware-specifications` |
| Pinouts | `ark_dan_gps.md#pinout`, `gps_smartap.md#pinout-and-connections` |
| Wiring (UART) | `gps_locosys_hawk_a1.md#wiring-and-connections` |
| Wiring (DroneCAN) | `../dronecan/ark_rtk_gps.md#wiring` |
| PX4 Configuration (non-u-blox) | `rtk_gps_holybro_unicore_um982.md#px4-configuration`, `rtk_gps_trimble_mb_two.md#configuration` |
| PX4 Configuration (DroneCAN) | `../dronecan/ark_rtk_gps.md#flight-controller-setup` |
| Heading | `rtk_gps.md#configuring-gps-as-yaw-heading-source`, `rtk_gps_holybro_unicore_um982.md#enable-gps-heading-yaw`, `u-blox_f9p_heading.md#setup` |
| LED Meanings | `../dronecan/ark_rtk_gps.md#led-meanings`, `septentrio_mosaic-go.md#led-status` |

Check each anchor at the base SHA before citing it: several of these pages use default slugs that change with the heading text.

### Anchors

Skeleton headings carry an explicit anchor, so links to the sections every GNSS page shares survive rewording and translation.

- **Skeleton headings** use the anchor shown in the skeleton, exactly.
  `{#store}` is an established short form and must not be "corrected".
- **Any other heading** doesn't need an anchor, and a missing one is not a finding.
  An anchor the author does give it is made from its text: lower case, words joined by underscores, punctuation and parenthetical qualifiers dropped.
- **Per-connection sub-sections** (G-W5, G-A9) take the parent's anchor as a prefix: `### UART {#wiring_uart}`, `### DroneCAN {#px4_configuration_dronecan}`.
- **Separate anchor tags**: an `<a id="..."></a>` on its own line just before a heading is `style`; the suggestion moves the id into the heading as `{#...}`.
- **Unique on the page**: two headings with the same anchor are `bug`.
- **Hyphenated explicit anchors** are `style`: PX4 explicit anchors use underscores.
  Links *to* the shared GNSS pages use their default hyphenated slugs (`#secondary-gps-configuration-uart`), since those headings have no explicit anchors; don't report those.

To find links to an old slug before accepting a changed anchor (G-P9), search from `docs/en/`: `grep -rn "<page>.md#<old-slug>" --include=*.md .` and `grep -n "](#<old-slug>)" <page>.md`.

## Family pages

| ID | Check | Severity |
| --- | --- | --- |
| G-M1 | `## Supported Models {#supported_models}` directly after the opening, as one table with a row per product: `Model` (linked), `Receiver`, `Capability` (GNSS, RTK, heading), `Connection`, and `Notes`. | `style` |
| G-M2 | Every product the page names is in the table, with its own receiver, capability and connection. | `style` |
| G-M3 | Discontinued products are in a `::: details Discontinued` block after the table, in a table with the same columns. | `style` |
| G-M4 | **Shared content is written once, and differences are never left implicit.** Where products differ in protocol, connection, wiring, configuration or capability, the page says which product gets which. | `bug` when a reader can't tell which instruction applies to their product |
| G-M5 | A product that needs a substantially different setup has its own page, linked from the table and nested under the family page in `SUMMARY.md`. | `style` |

## Section checks

### Opening

| ID | Check | Severity |
| --- | --- | --- |
| G-O1 | One H1, `# <Manufacturer> <Product> <GPS / RTK GPS / GNSS>`, naming the manufacturer as the manufacturer spells it and the product the same way as the `SUMMARY.md` entry and the device-table row. Qualifiers the manufacturer uses (bands, `L1/L5`) are allowed, but sibling pages from one manufacturer use the same pattern. | `style` |
| G-O2 | `<Badge type="tip" text="..." />` directly under the H1, only when the receiver needs firmware support newer than the latest stable release (a new protocol, a new heading or RTK path, a new node board), naming the first release with it: `main (PX4 vX.Y)` for one not yet released, where `vX.Y` is the version `docs/en/releases/main.md` says `main` is heading for. A receiver supported by existing firmware gets no badge. | `minor` if missing, `bug` if it names the wrong release |
| G-O3 | The first paragraph names the manufacturer and product, links the product page, and gives the bands or receiver, the capability (GNSS, RTK, dual-antenna or moving-base heading), and the connection. Marketing claims ("ideal upgrade", "centimetre-level in seconds") are kept to what the manufacturer facts back. | `bug` if wrong, `style` if the capability or connection is missing |
| G-O4 | A hero photo of the receiver, after the opening paragraph, stored locally (G-P5). | `style` |
| G-O5 | A list of applications or features in the opening, when there is one, has a lead-in sentence. | `minor` |
| G-O6 | A note under the hero image when PX4 support has a significant limit the reader must know before buying (no heading in PX4 though the receiver computes it; RTK float only), linked to where it's explained. | `bug` if the page implies support PX4 doesn't have |
| G-O7 | A discontinued product has ` (Discontinued)` in the H1, `<Badge type="info" text="Discontinued" />` under it, and a `::: warning` saying it's no longer available and, if stock exists, where. | `style` |
| G-O8 | When the manufacturer sells the receiver in interface variants (UART and CAN versions), the page says which variant each section documents, and Where to Buy says which to order when the store offers the choice. | `bug` if the page's setup only works for one variant and nothing says so, otherwise `style` |

### Specifications {#specifications}

| ID | Check | Severity |
| --- | --- | --- |
| G-S1 | A list in the `- **Label:** value` form, colon inside the bold, in the skeleton's order, each one the manufacturer gives. A page can add a label the list doesn't have (**Time to first fix:**, **RTK convergence:**, **Operating temperature:**, **Ingress protection:**, **NDAA compliant:** when the manufacturer claims it), in the same form. A flat marketing list (`## Features`) in place of Specifications is one finding on its heading line, with the restructured list written out below the tables, keeping every fact. | `style` if missing |
| G-S2 | Each value matches the manufacturer material the page links. A receiver, compass or barometer part no manufacturer document names is left out (`shared.md`, "If it can't be proven, it isn't asserted"). | `bug` |
| G-S3 | **Protocol:** names what the receiver outputs to PX4 (`u-blox UBX`, `NMEA 0183`, `Unicore`, `Septentrio SBF`), matching the protocol the PX4 Configuration section sets. | `bug` if wrong, `style` if missing |
| G-S4 | Units carry a space and ranges use an en dash with the unit once (`47 mm`, `4.75–5.25 V`, `10 Hz`, `115200 baud`). Labels the board template also has are spelled as it spells them: **Input voltage:**, **Current draw:**, **Dimensions:**, **Weight:**. | `style` |
| G-S5 | A vendor feature PX4 doesn't use or support (a proprietary command set, an output mode, a configuration app, base-station mode with another ground station) is marked where it's listed, as `(not supported on PX4)` or with a sentence saying what PX4 does instead. | `style` |
| G-S6 | A compass or barometer is listed with whether PX4 uses it: say so when PX4 doesn't start a driver for the part by default, and what enables it (`protocol-sources.md`, "Compass, barometer and LEDs"). | `style`; `bug` if the page relies on a part PX4 doesn't use |

### Where to Buy {#store}

| ID | Check | Severity |
| --- | --- | --- |
| G-B1 | A link to where each product can be bought (manufacturer store or resellers), without tracking parameters (G-P13). A discontinued product says so here instead. | `style`; a placeholder link is `bug` (G-P3) |

### Receiver Configuration {#receiver_configuration} (if present)

Settings made on the receiver itself, with the manufacturer's tool, or by updating its firmware.

| ID | Check | Severity |
| --- | --- | --- |
| G-C1 | Present when the receiver has to be changed from its factory state to work with PX4: an output protocol or message set, a baud rate outside what the driver probes, a heading or RTK mode. Names the tool, links it, and gives each setting and its value. | `bug` if PX4 can't use the receiver as shipped and the page doesn't say what to change |
| G-C2 | For a DroneCAN node: what firmware it runs (PX4 node, AP_Periph, vendor), how it's updated, the PX4 firmware target when it's a PX4 node (`<vendor>_<board>_default`, for a board directory that exists), and a link to [PX4 DroneCAN Firmware](../dronecan/px4_cannode_fw.md) when it runs PX4. | `style`; `bug` for a target that doesn't exist |
| G-C3 | Node parameters (the `CANNODE_*` set, or the AP_Periph or vendor parameters) are named as the node firmware names them, with a link to how to set them ([QGC Cannode Parameter Configuration](../dronecan/index.md#qgc-cannode-parameter-configuration)), and never given as flight-controller parameters. | `bug` if a parameter is attributed to the wrong firmware |

### Hardware Setup {#hardware_setup}

| ID | Check | Severity |
| --- | --- | --- |
| G-H1 | `### Mounting {#mounting}`: which way the receiver faces (the arrow on the case, when there is one), distance from other electronics, a clear view of the sky, and a link to [Mounting a Compass](../assembly/mount_gps_compass.md). For a dual-antenna or moving-base receiver, the antenna separation and orientation the manufacturer requires. | `style` if missing; `bug` if a heading receiver gives no antenna separation |
| G-N1 | `### Pinouts {#pinouts}`: the connector type and a table of pin, signal and level, or a pinout image with the same content. A connector that fully follows the Pixhawk standard can say so and link it instead of a table (`protocol-sources.md`, "Pixhawk GPS connector"). | `bug` when a non-standard connector has no pinout |
| G-N2 | A claim that the connector follows the Pixhawk standard is true pin by pin. | `bug` if not |
| G-W1 | `### Wiring {#wiring}` names the flight-controller port to use: for UART, the standard sentence (the 10-pin `GPS1` port), or the port and how to configure it when the connector isn't Pixhawk-standard; for DroneCAN, a `CAN` port, a link to [CAN Wiring](../can/index.md#wiring), and termination. | `style` if missing, `bug` if wrong |
| G-W2 | **Power**: the supply voltage the receiver needs and whether the flight-controller port can supply it; a receiver needing a separate supply or a 3.3 V level says so prominently. | `bug` if it contradicts the manufacturer, `style` if missing |
| G-W3 | Using `GPS2` or any port other than `GPS1` says the port must be configured (G-A3); the 6-pin `GPS2` port has no safety switch, buzzer or LED pins. | `bug` if it says the port works without configuration |
| G-W4 | A moving-base pair says how the two receivers connect to each other and to the flight controller, and links [RTK GPS Heading with Dual u-blox F9P](../gps_compass/u-blox_f9p_heading.md) for u-blox pairs. | `style` |
| G-W5 | A receiver with more than one connection has one `####` sub-section per connection under Wiring (`#### UART {#wiring_uart}`, `#### DroneCAN {#wiring_dronecan}`). | `style` |

Mounting, Pinouts and Wiring can be one `## Hardware Setup` section with no sub-headings when the whole of it is a few lines, as long as G-H1, G-N1 and G-W1 to G-W2 are covered.

### Firmware Support {#firmware_support} (if present)

Needed when the receiver's protocol or driver isn't in every build.
The values come from the facts worksheet (`protocol-sources.md`, "In firmware").

| ID | Check | Severity |
| --- | --- | --- |
| G-F1 | **A protocol other than u-blox**: says the protocol isn't included on boards with constrained flash. The one-sentence note from the standard wording, in PX4 Configuration, is enough; a full section names the key (`CONFIG_GPS_<PROTOCOL>=y`), how to check a board (`boards/<vendor>/<board>/default.px4board`), and how to add it and [build the firmware](../dev_setup/building_px4.md). | `style` if missing; `bug` if the page says every board supports it |
| G-F2 | **Septentrio**: the section exists, names `CONFIG_DRIVERS_GNSS_SEPTENTRIO=y`, says it's only in boards that set it (not most), how to check, and how to add it. | `bug` if missing |
| G-F3 | **DroneCAN**: the flight controller needs `CONFIG_DRIVERS_UAVCAN=y`, which most boards have; a line is enough. | `minor` |

### PX4 Configuration {#px4_configuration}

| ID | Check | Severity |
| --- | --- | --- |
| G-A1 | **Protocol and port** (UART): for u-blox, the standard sentence (detected automatically, nothing to set); for any other protocol, `GPS_1_PROTOCOL` and its value, with reboot (standard wording). "Plug and play" or "no configuration" only for a protocol PX4 finds with the parameters at their defaults (`protocol-sources.md`, "Protocol and detection"). | `bug` if wrong or missing |
| G-A2 | **Baud rate**: says nothing needs setting when the protocol probes the receiver's rate (`SER_GPS1_BAUD` defaults to Auto); gives the `SER_<port>_BAUD` value or the receiver setting (G-C1) when it doesn't. A baud value is a number, not "115200 8N1". | `bug` if wrong, `style` if a needless or malformed value |
| G-A3 | **Secondary receiver**: the standard wording, with `GPS_2_CONFIG` (which has no default port) and `GPS_2_PROTOCOL` when the protocol isn't u-blox. | `style` if missing; `bug` if it says a secondary receiver needs no configuration |
| G-A4 | **RTK** (RTK receivers): the standard link to [RTK GNSS](../gps_compass/rtk_gps.md); for DroneCAN, `UAVCAN_PUB_RTCM` (and the node's `CANNODE_SUB_RTCM` when it isn't set by the node's defaults). | `bug` for DroneCAN without the correction publication; `style` otherwise |
| G-A5 | **Heading** (heading receivers): `SENS_GNSSn_HDG` with the value for this receiver, the antenna positions (`SENS_GNSSn_OFFX/Y/Z`, and `SENS_GNSSn_AUXX/Y/Z` for two antennas on one receiver), `SENS_GNSSn_ID` where the slot isn't the instance order, the heading-fusion bit of `EKF2_GPS_CTRL`, which antenna is main and which auxiliary, and the link to the shared heading section (standard wording; `protocol-sources.md`, "Heading"). Never present for a receiver whose heading PX4 doesn't use, and never naming a removed offset parameter (`GPS_YAW_OFFSET`, `EKF2_GPS_YAW_OFF`, `SEP_YAW_OFFS`, `SEP_PITCH_OFFS`). | `bug` if wrong, missing, incomplete, or given for a receiver without usable heading |
| G-A6 | **DroneCAN**: the standard wording: `UAVCAN_ENABLE` with a value that enables sensors, the subscriptions (noting they're on by default), and the link to [DroneCAN > GPS](../dronecan/index.md#gps). A parameter set "to ensure" an effect has that effect in the source. | `bug` if wrong or missing |
| G-A7 | **Antenna position**: the `SENS_GNSS0_OFF*` parameters (standard wording), or a link to [Mounting a Compass > Position](../assembly/mount_gps_compass.md#position). | `style` |
| G-A8 | Reboot after any parameter the source marks `reboot_required` (all the port, protocol and DroneCAN ones). | `style` |
| G-A9 | A receiver with more than one connection has one `###` sub-section per connection under PX4 Configuration (`### DroneCAN {#px4_configuration_dronecan}`), in the same order as under Wiring. | `style` |
| G-A10 | Steps that must be done in order are a numbered list. | `minor` |
| G-A11 | The configuration is on the page. A link to the manufacturer's manual is fine as further reading, labelled as a manual, but never in place of the PX4 steps; a manual written for another autopilot is never the PX4 configuration. | `bug` if the page's only configuration is a link |
| G-A12 | **Septentrio**: `SEP_PORT1_CFG` set to the port, with `GPS_1_CONFIG` set to `0` (Disabled) when the port is `GPS1`; heading with `SENS_GNSSn_HDG` and the antenna positions (and `SEP_HARDW_SETUP` `1` for two receivers); a link to [Septentrio GNSS Receivers](../gps_compass/septentrio.md) for the rest. | `bug` if wrong or missing |

### LED Meanings {#led_meanings} (if present)

| ID | Check | Severity |
| --- | --- | --- |
| G-E1 | A table, `LED colour`, `Status indicator` (or `State`), `Description`, one row per LED or state, each description a sentence. An I2C LED driver part or address named is one PX4 starts (`protocol-sources.md`, "Compass, barometer and LEDs"). | `style`; `bug` if the driver or address is wrong |

### Testing {#testing}

| ID | Check | Severity |
| --- | --- | --- |
| G-T1 | Says how to confirm the receiver works: `gps status` (or `septentrio status`) and `listener sensor_gnss` in the MAVLink console, or the GPS indicator in _QGroundControl_; for RTK, the RTK fix types; for heading, `listener vehicle_gnss_heading`. | `style` if missing |
| G-T2 | Every command, option, topic and message named exists (`protocol-sources.md`, "Commands", "Topics"). | `bug` |

### Troubleshooting {#troubleshooting} (if present)

| ID | Check | Severity |
| --- | --- | --- |
| G-X1 | One `###` per problem, named for the symptom. Commands and parameters named exist. "No GPS detected" covers the protocol setting for a receiver that isn't u-blox; for a heading receiver, PX4's "GPS heading not used: set ..." warnings are worth covering. | `bug` if a command or parameter doesn't exist |

### Further Information {#further_information}

| ID | Check | Severity |
| --- | --- | --- |
| G-I1 | Links the manufacturer's current manual or datasheet, and the product page, each labelled for what it is. | `style`; `bug` if the link is dead |
| G-I2 | Every link labelled as instructions ("Wiring instructions", "Configuration instructions") leads to that content, not to a download page whose document lacks it. | `style` |

## Listings

Where a GNSS page has to be listed; `completeness.md` applies these.

| ID | Check | Severity |
| --- | --- | --- |
| G-L1 | An entry in `docs/en/SUMMARY.md` under `[GNSS (GPS)](gps_compass/index.md)` for a non-RTK receiver or `[RTK GNSS](gps_compass/rtk_gps.md)` for an RTK one, with the H1's product name as link text (` (CAN)` appended for a DroneCAN product), in alphabetical order by manufacturer among the current products. A discontinued product has a `✘ ` prefix and sits after the current ones. | `bug` if missing, `style` for form or order |
| G-L2 | A row in exactly one device table: `gps_compass/index.md` (`Device`, `GPS`, `Compass`, `CAN`, `Buzzer / SafeSw / LED`, `Notes`) for a non-RTK receiver, or `gps_compass/rtk_gps.md` (`Device`, `GPS`, `Compass`, `DroneCAN`, `GPS Yaw`, `PPK`) for an RTK one, every cell filled the way its neighbours fill them. | `bug` if missing, `style` for form |
| G-L3 | The row is in alphabetical order by device name. A discontinued product follows the table's own statement about discontinued devices. | `style` |
| G-L4 | The row agrees with the page and the source (G-P10): `GPS` the receiver as the manufacturer names it, or `✓` when no document names it; `Compass` the part, `✓`, or `✘`; `CAN`/`DroneCAN` only for a DroneCAN product; `GPS Yaw` only for a receiver that publishes heading; `Buzzer / SafeSw / LED` matching the hardware. Count header cells to check which column a value sits in. | `bug` |
| G-L5 | When the receiver's protocol isn't u-blox, the sentences that list the protocols PX4 supports (`gps_compass/index.md`, the opening and the "Supported GNSS" section; `rtk_gps.md`, "Supported Devices") name it. | `style` |
| G-L6 | A DroneCAN receiver is listed under [Supported Hardware](../dronecan/index.md#supported-hardware) in `docs/en/dronecan/index.md`. | `style` |
| G-L7 | A dual-F9P heading product is listed in `u-blox_f9p_heading.md` ("Supported Devices"); a Septentrio product in `septentrio.md`. | `style` |
