# Lens: source consistency

Does the page say what PX4 does with the receiver?

Most of a GNSS page restates settings that already exist in the source: which protocol value to set, whether PX4 finds the receiver by itself, which port it runs on, whether heading and RTK work, what a DroneCAN node publishes.
When the page and the source disagree, the reader sets a value that doesn't exist, waits for a receiver PX4 never detects, or enables heading fusion for a receiver whose heading PX4 doesn't use.
Work every checkable claim, not a sample.

Read `references/protocol-sources.md` in full before starting: it says which file answers which question.

This lens owns the *correctness* half of every `page-template.md` check: where a check's severity says "`bug` if wrong", you decide whether it's wrong.
Whether the content is *present* and in the right form is `completeness.md`'s job.
Cite the check ID alongside the source evidence (`G-A1; params.yaml:230 6: NMEA (generic)`).

## Method

1. **Start from the GNSS facts worksheet** (`protocol-sources.md`) the main agent filled in, and re-open a source file only to confirm a value you're about to cite or one the worksheet marks `unknown`.
   If you find a worksheet value wrong, report that and use the corrected value.
2. **List every checkable claim on the page** that falls in the lookup table: parameter names, values and defaults; the protocol; ports; baud rate; "plug and play" or "detected automatically"; heading and RTK support and the heading setup (`SENS_GNSSn_HDG`, antenna positions); Kconfig keys and firmware availability; DroneCAN subscriptions and node parameters; commands, options and topics; the compass, barometer and LED parts and whether PX4 uses them.
   Include the page's device-table row and any other listing in scope.
3. **Check each claim** against the file the lookup table names, and record the file and line whatever the outcome.
4. **Check the other direction**: what the source requires that the page doesn't say (a protocol value that has to be set, a subscription that's off by default, a heading offset parameter).
5. **For a family page, do steps 2 to 4 once per product**, against the connection and protocol the page gives that product.

## Rules

### Protocol and detection

This is where GNSS pages most often go wrong, so work it first.

- The protocol the page names (or implies, by naming a chip) matches the manufacturer facts' output protocol.
  A page that names none, for a receiver whose protocol isn't u-blox, is `bug` (G-A1): the reader can't configure it.
- The `GPS_x_PROTOCOL` value the page gives exists in the enum and means that protocol, by number and label.
- **"Plug and play", "detected automatically", "no configuration needed"** need the receiver's protocol to be found with the parameter at its default.
  With the default `1` (u-blox) only UBX is tried; other protocols need either the matching value or `0` (auto-detect), and NMEA is never auto-detected, so an NMEA receiver needs `6` whatever else is set (`protocol-sources.md`, "Protocol and detection").
  A plug-and-play claim for a receiver that doesn't meet this is `bug` (G-A1).
- A page that tells the reader to set the protocol for a u-blox receiver isn't wrong, but setting it to `0` slows detection: `minor`.
- When the protocol is left out of constrained-flash builds, the page says so (G-F1); a page that implies every board supports it is `style`, or `bug` when the page's own example board is constrained.

### Ports and baud rate

- The port the page names for the primary receiver matches `GPS_1_CONFIG`'s default, or the page says how to set it.
- **Secondary GPS**: a receiver offered on `GPS2` (or any port other than the one `GPS_1_CONFIG` defaults to) needs `GPS_2_CONFIG` set, since it has no port by default (check its default in the worksheet).
  "Plug and play on GPS2" is `bug` (G-A3).
  A `SER_GPS2_BAUD` instruction alone is `bug` too: that parameter doesn't appear until the port is assigned.
- A baud rate the page tells the reader to set is one the protocol needs: UBX configures the receiver and probes the port, so a fixed `SER_GPSx_BAUD` for a u-blox receiver is unnecessary (`minor`), and a value given with framing ("115200 8N1") isn't a parameter value (`style`).
  For a protocol that only probes some rates, a receiver whose default rate is outside them needs the page to say how to set the receiver or the port (G-C1): `bug` when the manufacturer facts show such a default and the page says nothing.
- Port names and their parameter values (`GPS 1` is `201`) match the serial configuration values.

### RTK

- A page that says the receiver supports RTK needs the protocol to inject corrections and to report the RTK fix (`protocol-sources.md`, "RTK").
- For UART receivers, the page links [RTK GNSS](../gps_compass/rtk_gps.md) for the ground-station side rather than inventing its own steps.
- For DroneCAN receivers, RTK needs the flight controller to publish corrections to the node: `UAVCAN_PUB_RTCM`, which is off by default.
  An RTK DroneCAN page that doesn't say to enable it, and doesn't say the node is configured some other way, is `bug` (G-A6).
- A base-station claim ("can be used as a base") is checked against the manufacturer facts and against what PX4 does with a base (it doesn't configure a non-u-blox receiver as a base).

### Heading

- A page that tells the reader to enable heading fusion ([EKF2_GPS_CTRL](../advanced_config/parameter_reference.md#EKF2_GPS_CTRL) bit 3, value `15` from the default `7`, or any value with that bit) needs a receiver and protocol that publish heading (`protocol-sources.md`, "Heading").
  Telling the reader to set it for a single-antenna receiver is `bug` (G-A5).
- Heading needs `SENS_GNSSn_HDG` in the heading receiver's slot, with the value for this kind of receiver, and the antenna positions (`protocol-sources.md`, "Heading"); for DroneCAN also `SENS_GNSSn_ID` set to the node's ID and `UAVCAN_SUB_GPS_R` left on.
  A heading setup missing any of these is `bug` (G-A5): PX4 drops the heading and warns.
- A page naming `GPS_YAW_OFFSET`, `EKF2_GPS_YAW_OFF`, `SEP_YAW_OFFS` or `SEP_PITCH_OFFS` as a PX4 setting names a parameter that no longer exists: `bug`.
  The exception is a note telling the reader to set an older PX4 CAN node's own `GPS_YAW_OFFSET` to `0` (`dronecan/index.md`).
- A receiver whose heading PX4 doesn't use (Ashtech/Trimble, Femtomes, NMEA `$xxHDT`) set up as a heading source is `bug`.
- A link's text and anchor name the same parameter (G-P11).
- Antenna separation and orientation requirements match the manufacturer facts, and for u-blox moving-base pairs the shared page `u-blox_f9p_heading.md`.

### DroneCAN

- The `UAVCAN_ENABLE` value given enables sensors (`2` or `3`), and a page that gives two different values without saying why is `bug`.
- Subscriptions the page tells the reader to enable are ones that exist; telling them to enable one that's already on by default isn't wrong, but saying it's required when it's the default is `minor`.
- A parameter the page sets "to ensure" an outcome is checked: a value with a stated effect the source doesn't show (`SENS_GNSS_PRIME` set to the moving base's node ID "so heading works", when Auto, the default, already makes a configured moving base primary and selection doesn't gate heading) is `bug`, since it tells the reader something about how PX4 works that isn't true.
- A parameter that no longer exists (`SENS_GPS_MASK`, `SENS_GPS_PRIME`, `SENS_GPS0_OFFX`, `EKF2_GPS_POS_X`) is `bug` on a new page; old names are migrated, but a reader can't find them.
- Node parameters (`CANNODE_*`, `GPS_UBX_MODE` on the node) exist in the node firmware the GNSS facts give: PX4 cannode parameters for a PX4 node, the node vendor's for AP_Periph or closed firmware.
  A PX4 parameter name used for an AP_Periph node is `bug`.
- Firmware targets named for updating a PX4 node exist under `boards/` and are the node's own board.

### Firmware support

Check the Firmware Support section, and anything the opening says about availability, against the worksheet's "In firmware" rows:

- Each Kconfig key the page gives exists, with `CONFIG_` and `=y`.
- A protocol or driver left out of some builds (constrained flash, or not in most boards' configuration) has a page that says so; a page saying it is in every build when it isn't is `bug` (G-F1).
- The Septentrio driver's key and board count are right, and the page doesn't imply the `gps` driver handles a Septentrio receiver in SBF mode.

### Compass, barometer, LEDs and safety switch

- A compass, barometer or LED driver the page or its table row names is backed by the manufacturer facts (`shared.md`, "If it can't be proven, it isn't asserted").
  An unsourced part is not a finding but goes below the tables as unproven, and the row should use `✓`.
- When the page says the module has a compass or barometer, check whether PX4 starts a driver for that part on an external bus by default (`protocol-sources.md`, "Compass, barometer and LEDs").
  A part PX4 doesn't start by default, presented as if it simply works, is `style` (G-S6); presented as required for something ("uses the barometer for altitude") it's `bug`.
- A safety switch, buzzer or LED claimed to work with PX4 needs the standard GPS1 connector pins (`protocol-sources.md`, "Pixhawk GPS connector") or a driver PX4 starts for it.
  Safety is off by default (`COM_SAFETY_MODE` `0`), so a page that says the switch must be pressed before arming has to say how to enable it.

### Features PX4 doesn't use

A vendor feature list on the page (`shared.md`, "Manufacturer facts") that names something PX4 doesn't use or support, with nothing saying so, is `style` (G-S5): the reader assumes PX4 supports what the page lists.
Check each feature that implies PX4 behaviour (a proprietary command set, a configuration protocol, an output mode, an RTK base mode) against the source.

### Commands, topics and messages

- Every command and option the page shows is in the driver's usage block (`gps status`, `gps start -p <protocol>`); a `-p` value the parser doesn't accept is `bug`.
- The uORB topic and MAVLink message the page names are the ones published (`protocol-sources.md`, "Topics"): `sensor_gnss`, not `sensor_gps`.
- The module reference link uses the right anchor.

### Physical specifications and wiring

Input voltage, current, dimensions, weight, connector and pin order aren't in the source, except where the page claims the Pixhawk GPS connector.
Check them against the manufacturer facts, against the same figures elsewhere on the page, and a claimed Pixhawk-standard pinout against the standard pin by pin.
A figure the manufacturer facts contradict is `bug`.
A figure they don't cover is not a finding; return it as an unproven claim for the notes below the tables.
Where the facts are marked `not read`, every wiring claim on the page is unverified: say that once below the tables rather than once per claim.

### Wiring images

Check what each pinout, wiring or connector image shows (`shared.md`, "Wiring images") against the page's tables and text, against the other images on the page, and against the manufacturer facts, pin by pin.
Report a disagreement on the line the image is referenced from.

### Links to manufacturer material

- A link labelled as wiring, mounting or configuration instructions has to lead to that content; a vendor page holding only a download of a manual with no such section is `style` (G-I2), and configuration given only as such a link is `bug` (G-A11).
- A manual written for another autopilot (ArduPilot `GPS1_TYPE`, Mission Planner screens) is never the page's PX4 configuration.
- The manual the page links is the current one in the manufacturer facts (G-I1).

## Severity

A claim the source contradicts is `bug`.
Something the source requires that the page doesn't say is `bug` when the receiver won't work without it (a protocol value, a port for a secondary receiver, an RTCM publication), and `style` otherwise.
A claim you can't check against any source is not a finding.

## What this lens doesn't cover

Page form and shared wording (`sibling-comparison.md`), required content and listings (`completeness.md`), and prose (`px4-doc-review`).
