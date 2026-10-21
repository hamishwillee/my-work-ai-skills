# Protocol sources

Where each claim on a GNSS page can be checked in the PX4 source, and how to read it.
Read the files at the PR's head SHA, and the protocol implementations at the submodule commit the head records.

Source says what PX4 *does* with the receiver, not everything the receiver *can do*.
A page claim with no source counterpart (a supply voltage, a pin order, an accuracy figure) is checked against manufacturer material or left as a question; a page claim the source *contradicts* is a `bug`.

The values quoted below were read at PX4-Autopilot upstream `main` `b8b689d` (20 October 2026), with `src/drivers/gps/devices` at `f6f5c2d`.
They are a map, not evidence: re-read every value you cite at the head SHA, since parameters, defaults and counts change.
GNSS changed a lot in late September 2026 (GPS renamed to GNSS in topics and sensor parameters, blending removed, heading moved to its own topic with all heading-offset parameters removed): a PR whose base predates that describes a different firmware, so check which side of it the base is on.

**Read the PX4 upstream, not a fork.**
A reviewer's clone often has `origin` pointing at their own fork, whose `main` can be weeks old.
Use the remote whose URL is `github.com/PX4/PX4-Autopilot` (`git -C <clone> remote -v`), and fetch it before reading.

## Where the source is

| Connection | Source |
| --- | --- |
| UART, `gps` driver | `src/drivers/gps/gps.cpp` (detection, modes, usage block), `params.yaml` (protocol and u-blox parameters), `module.yaml` (`GPS_1_CONFIG`, `GPS_2_CONFIG`, the start command), `Kconfig` (which protocols are built), correction injection in `src/lib/gnss/correction_injector.{h,cpp}`, and the protocol implementations in the submodule `src/drivers/gps/devices/src/` (`ubx.cpp`, `nmea.cpp` and `unicore.cpp` (NMEA and Unicore), `ashtech.cpp`, `emlid_reach.cpp`, `mtk.cpp`, `femtomes.cpp`). `sbf.cpp` is in the submodule but not built. |
| UART, Septentrio | `src/drivers/gnss/septentrio/` (`septentrio.cpp`, `module.yaml` with `SEP_PORT1_CFG` and every `SEP_*` parameter, `Kconfig`). The `gps` driver has no SBF protocol. |
| DroneCAN | Flight controller: `src/drivers/uavcan/sensors/gnss.cpp` (position), `src/drivers/uavcan/sensors/gnss_relative.cpp` (`RelPosHeading`, the DroneCAN heading path), `sensor_bridge.cpp` (which subscriptions start), and `src/drivers/uavcan/uavcan_params.yaml`. Node, when it runs PX4: `src/drivers/uavcannode/` (`uavcannode_params.yaml`, `Publishers/GnssFix2.hpp`, `Publishers/RelPosHeading.hpp`, `Subscribers/RTCMStream.hpp`) and the node's board, `boards/<vendor>/<board>/` (`default.px4board`, `init/rc.board_defaults`, `init/rc.board_sensors`). An AP_Periph or closed node has no source here: its parameters come from its vendor's documentation. |
| Selection, heading and offsets | `src/modules/sensors/vehicle_gps_position/`: `module.yaml` (`SENS_GNSS_PRIME`, `SENS_GNSSn_ID`, `SENS_GNSSn_OFFX/Y/Z`, `SENS_GNSSn_DELAY`, `GNSS_CHECK`, `GNSS_REQ_*`), `params_heading.yaml` (`SENS_GNSSn_HDG`, `SENS_GNSSn_AUXX/Y/Z`), `VehicleGPSPosition.cpp`, `GnssHeadingBaseline.hpp`, `GnssSelector.cpp`. |
| Estimator | `src/modules/ekf2/params_gnss.yaml` (`EKF2_GPS_CTRL`, `EKF2_GPS_YAW_RST`), `src/modules/ekf2/EKF2.cpp`. |
| Compass, barometer, LEDs | `ROMFS/px4fmu_common/init.d/rc.sensors` and `rcS`, and the board's `rc.board_sensors`. |
| Serial ports | `Tools/serial/generate_config.py` (port tags, values, default ports and baud rates), `Tools/serial/serial_params.c.jinja` (`SER_<TAG>_BAUD`), `Tools/serial/rc.serial_port.jinja` (port conflicts). |

## GNSS facts worksheet

The main agent fills this in once per connection, in Scope, and passes it to every lens.
Each value carries the file and line it came from, so a lens can cite it as evidence without re-reading.
Take line numbers from each file on its own (`grep -n` on that file), never from several files printed together.
A value the files don't settle is written `unknown` with what was searched, never guessed.

**A comment is not proof.**
Record what the code does, not what a comment, usage text or parameter description says it does.
For example, the `gps` usage text still says the secondary receiver "is currently not used by the rest of the system", but the sensors module selects it when the primary fails.

| Fact | Value | Source (file:line) |
| --- | --- | --- |
| Driver and protocol (`gps -p <x>`, `septentrio`, DroneCAN bridge) | | |
| `GPS_x_PROTOCOL` value for this protocol, and the default | | |
| Auto-detected (in the auto-detect list) | yes / no | |
| Protocol's Kconfig key and its default; constrained-flash boards leave it out | | |
| Boards building the driver (`CONFIG_DRIVERS_GPS`, `CONFIG_DRIVERS_GNSS_SEPTENTRIO`, `CONFIG_DRIVERS_UAVCAN`), count of all `default.px4board` | | |
| Primary port parameter and default (`GPS_1_CONFIG`, `SEP_PORT1_CFG`) | | |
| Secondary port parameter and default (`GPS_2_CONFIG`, `SEP_PORT2_CFG`) | | |
| Baud: `SER_<port>_BAUD` default; rates the protocol probes; rate it sets | | |
| RTCM injection (formats accepted); fix types reported (RTK float and fixed) | | |
| Heading: does this source publish `sensor_gnss_relative` heading; the `SENS_GNSSn_HDG` value that applies; which antenna positions | | |
| Other driver parameters the page names or should (u-blox mode, constellations, `SEP_*`) | | |
| DroneCAN: `UAVCAN_ENABLE` values; subscriptions and their defaults; `UAVCAN_PUB_RTCM`, `UAVCAN_PUB_MBD` | | |
| DroneCAN node: firmware (PX4 board, AP_Periph, vendor); node parameters and board defaults; start line | | |
| Compass and barometer: does PX4 start a driver for the module's parts on an external bus by default | | |
| LED driver started by default; safety switch and buzzer | | |
| Commands and options; topics | | |
| Module reference anchor | | |
| First release (for the badge) | | |

## Protocol and detection

| `GPS_x_PROTOCOL` | Protocol | Kconfig key (default) | Auto-detected | Baud when `SER_<port>_BAUD` is `0` (Auto) | Heading used by PX4 |
| --- | --- | --- | --- | --- | --- |
| `0` | Auto detect | | | | |
| `1` (default) | u-blox UBX | `GPS_UBX` (`y`) | yes | probes 9600–921600, then configures the receiver (115200 for M8 and newer, or `GPS_UBX_BAUD1`) | yes: the rover of a moving-base pair (`GPS_UBX_MODE` `1`/`3`), and dual-antenna X20 (NAV-DAHEADING) when not in a moving-base setup |
| `2` | MTK | `GPS_MTK` (`!BOARD_CONSTRAINED_FLASH`) | yes | fixed 38400 | no |
| `3` | Ashtech / Trimble | `GPS_ASHTECH` (`!BOARD_CONSTRAINED_FLASH`) | yes | probes 9600–115200, then sets 115200 | no (the receiver's `$GPHDT` is no longer used) |
| `4` | Emlid Reach | `GPS_EMLIDREACH` (`!BOARD_CONSTRAINED_FLASH`) | yes | 57600, 115200 or 230400 | no |
| `5` | Femtomes | `GPS_FEMTOMES` (`!BOARD_CONSTRAINED_FLASH`) | yes | 115200 only | no (no longer used) |
| `6` | NMEA (generic, includes Unicore) | `GPS_NMEA` (`!BOARD_CONSTRAINED_FLASH`) | **never** | tries the configured rate, then 9600–230400 | Unicore `UNIHEADINGA` only; `$xxHDT` is not used |

What follows for the page:

- **The default (`1`) tries only u-blox.**
  A u-blox receiver on `GPS1` needs nothing set; `gps_compass/index.md` says the ports are "plug-n-play for u-blox modules (only)".
- **Auto-detection (`0`) tries u-blox, MTK, Ashtech, Emlid and Femtomes**, each only if built (`gps.cpp`, `kAutoDetectModes`).
  A receiver using one of those works with `0` or its own value; with the default `1` it isn't found, so the page has to say what to set.
- **NMEA is never auto-detected** (`gps.cpp`: "NMEA is excluded because it can produce false-positive detections"; `Kconfig` `GPS_NMEA` help: "must be selected explicitly via GPS_x_PROTOCOL").
  An NMEA or Unicore receiver needs `GPS_1_PROTOCOL` = `6`.
- **A protocol not built into the firmware** makes the driver fall back to auto-detection with a warning ("unsupported by this build, using auto-detection").
  Every protocol except u-blox is left out of boards that set `CONFIG_BOARD_CONSTRAINED_FLASH=y` (24 of 125 `default.px4board` files in October 2026, mostly CAN nodes and small FPV boards), so its page needs the Firmware Support note (G-F1).
  Count them at the head: `grep -rl "CONFIG_BOARD_CONSTRAINED_FLASH=y" boards --include=default.px4board | wc -l` against `ls boards/*/*/default.px4board | wc -l`.
- **The protocol for the secondary receiver is `GPS_2_PROTOCOL`**, with the same values.

**Command line.**
`gps start -p` accepts `ubx`, `mtk`, `ash`, `eml`, `fem` and `nmea` (`gps.cpp`, the `-p` parsing); anything else fails with "unknown protocol".
There is no `sbf`: a Septentrio receiver uses the `septentrio` driver.

## Ports and baud rate

- `GPS_1_CONFIG` defaults to the board's `GPS1` port (value `201`), or `0` (Disabled) on a board with no port tagged `GPS1` (`module.yaml`, `generate_config.py`).
- `GPS_2_CONFIG` has **no default port: it is `0` (Disabled)**, so a secondary receiver needs it set; one board (`mro/ctrl-zero-classic`) sets it in its `rc.board_defaults`.
- The baud parameter is `SER_<TAG>_BAUD` (`SER_GPS1_BAUD`, `SER_GPS2_BAUD`), default `0` (Auto); it appears only once a driver is assigned to the port.
  There is no `GPS_x_BAUD` parameter.
- All port parameters are `reboot_required`.
- Port values follow `generate_config.py`: `201` is `GPS 1`, `202` is `GPS 2`, `102` is `TELEM 2`.
- Two drivers on one port: the first to claim it wins and the other is skipped (`rc.serial_port.jinja`), which is why the Septentrio setup sets `GPS_1_CONFIG` to `0` when `SEP_PORT1_CFG` uses `GPS1`.

## RTK

- **Correction injection works for every protocol** on the `gps` driver: `gnss::CorrectionInjector` (`src/lib/gnss/correction_injector.h`) reads `rtcm_corrections` (from MAVLink `GPS_RTCM_DATA` or DroneCAN `RTCMStream`) and `rtcm_moving_baseline`, and writes the frames to the receiver from the serial port's work queue.
  Protocols other than u-blox accept RTCM3 only; u-blox also accepts SPARTN and UBX (`gps.cpp`).
  u-blox modes `1` and `5` take no injected corrections (the base feeds the rover on UART2), and mode `3` takes only the moving-baseline stream.
  The Septentrio driver uses the same injector.
- **RTK fix reporting**: u-blox NAV-PVT carrier solution gives 5 (float) or 6 (fixed); NMEA GGA quality 5 gives 5 and quality 4 gives 6; Emlid maps its own states (`nmea.cpp`, `ubx.cpp`, `emlid_reach.cpp`; constants in `msg/SensorGnss.msg`).
  A receiver whose output doesn't carry an RTK state can't show an RTK fix in PX4, whatever it computes.
- **DroneCAN**: the flight controller sends corrections to the node only when `UAVCAN_PUB_RTCM` is `1` (default `0`), and a moving-base pair over CAN needs `UAVCAN_PUB_MBD` / `UAVCAN_SUB_MBD`; a PX4 node subscribes when its `CANNODE_SUB_RTCM` is `1` (default `0`, set by RTK nodes' `rc.board_defaults`).
- The base station is set up from the ground station, not by PX4 (`rtk_gps.md`, "RTK Connection Process"); a claim that the receiver can be used as a base is checked against the manufacturer facts and that page, not against PX4's source.

## Heading

PX4 uses GNSS heading through one path: the receiver's heading is published on `sensor_gnss_relative`, the sensors module checks it against the configured antenna baseline and publishes `vehicle_gnss_heading`, and EKF2 fuses it.
Every heading-offset parameter has been removed and is not migrated (`GPS_YAW_OFFSET`, `EKF2_GPS_YAW_OFF`, `SEP_YAW_OFFS`, `SEP_PITCH_OFFS`; `docs/en/releases/main.md`, the upgrade notes): the offset is computed from the antenna positions.

For heading to be used, all of these are needed:

- [EKF2_GPS_CTRL](../advanced_config/parameter_reference.md#EKF2_GPS_CTRL) bit 3 ("Dual antenna heading"); the default is `7`, so the usual instruction is "set to `15`".
- [SENS_GNSSn_HDG](../advanced_config/parameter_reference.md#SENS_GNSS0_HDG) in the slot of the receiver that reports heading: `1` (`Moving base rover`) or `2` (`Dual antenna`). The default is `0` (Disabled).
- The antenna positions: [SENS_GNSSn_OFFX/Y/Z](../advanced_config/parameter_reference.md#SENS_GNSS0_OFFX) (for a moving-base pair, in both receivers' slots), and for a dual-antenna receiver the auxiliary antenna's [SENS_GNSSn_AUXX/Y/Z](../advanced_config/parameter_reference.md#SENS_GNSS0_AUXX).
  The configured baseline must be at least 5 cm, and the reported baseline length within 20% of it (`GnssHeadingBaseline.hpp`).
- The slot matched to the receiver: [SENS_GNSSn_ID](../advanced_config/parameter_reference.md#SENS_GNSS0_ID) when it isn't the instance order (always for DroneCAN; instance order is "only reliable for serial GPS").

The shared page [Configuring GPS as Yaw/Heading Source](../gps_compass/rtk_gps.md#configuring-gps-as-yaw-heading-source) gives this as a table; device pages link it.
When a slot's heading can't be used, PX4 warns "GPS heading not used: set SENS_GNSSn_HDG" or "GPS heading not used: set the antenna positions" (`VehicleGPSPosition.cpp`): good Troubleshooting content.
Boards that don't build `EKF2_GNSS_YAW` (some small FPV boards) have no `SENS_GNSSn_HDG` at all.

| Source | Publishes heading | `SENS_GNSSn_HDG` |
| --- | --- | --- |
| u-blox moving base (`GPS_UBX_MODE` `1`/`3` on the rover, `2`/`4` on the base) | the rover, from NAV-RELPOSNED, when carrier-fixed, valid, and baseline < 10 m | `1` in the rover's slot; `OFF*` of both receivers |
| u-blox X20 dual antenna | NAV-DAHEADING, when not in a moving-base setup | `2`; `OFF*` main antenna, `AUX*` auxiliary |
| Unicore (NMEA `6`) | `UNIHEADINGA`, the bearing from primary to secondary antenna | `2`; `OFF*` primary, `AUX*` secondary |
| Septentrio, one receiver, two antennas | AttEuler, with fixed ambiguities | `2` |
| Septentrio, two receivers (`SEP_HARDW_SETUP` `1`) | the moving-base vector | `1` |
| DroneCAN `RelPosHeading` | as the node sends it; the bridge runs when `UAVCAN_SUB_GPS_R` is `1` (default) | `1` or `2` in the slot whose `SENS_GNSSn_ID` is the node's |
| Ashtech/Trimble, Femtomes, NMEA `$xxHDT`, MTK, Emlid | none used by PX4 | none |

- A PX4 CAN node always publishes `RelPosHeading`; heading in its `Fix2` message is ignored.
  For an AP_Periph or vendor node, whether it sends the raw baseline bearing (what PX4 now expects) or one with its own offset applied can't be settled from PX4 source: ask the manufacturer.
- A receiver that computes heading PX4 doesn't use (Trimble MB-Two, Femtomes, a receiver sending only `$xxHDT`) is, for PX4, not a heading receiver: a page that sets up heading for it is the `bug` case (G-A5), and its heading feature is one PX4 doesn't support (G-S5).

## DroneCAN

| Parameter | Default | Notes |
| --- | --- | --- |
| `UAVCAN_ENABLE` | `0` | `1` sensors manual config, `2` sensors automatic config, `3` sensors and actuators; reboot required |
| `UAVCAN_SUB_GPS` | `1` | already on |
| `UAVCAN_SUB_GPS_R` | `1` | already on; the DroneCAN heading path (`RelPosHeading`) |
| `UAVCAN_SUB_MAG` | `1` | already on |
| `UAVCAN_SUB_BARO` | `0` | needed only to use a node's barometer |
| `UAVCAN_PUB_RTCM` | `0` | needed for RTK |
| `UAVCAN_PUB_MBD`, `UAVCAN_SUB_MBD` | `0` | moving baseline over CAN |

PX4 node parameters (`uavcannode_params.yaml`): `CANNODE_NODE_ID` (`0`, dynamic allocation), `CANNODE_TERM` (`0`), `CANNODE_SUB_RTCM`, `CANNODE_SUB_MBD`, `CANNODE_PUB_MBD` (all `0` by default, set by RTK nodes' board defaults), `CANNODE_PUB_BAR` and `CANNODE_PUB_MAG` (`1`).
A parameter name a board file sets that isn't defined anywhere (`CANNODE_GPS_RTCM` on `freefly/can-rtk-gps`) is a firmware observation, never something to copy onto a page.
Flight-controller firmware no longer embeds node firmware; nodes are updated from the SD card (`docs/en/releases/main.md`).

## Selection and antenna position

- [SENS_GNSS_PRIME](../advanced_config/parameter_reference.md#SENS_GNSS_PRIME): default `-1` (Auto); `0` the main serial receiver, `1` the secondary serial receiver, `2`–`127` a DroneCAN node ID.
  With Auto, the moving base of a configured moving-base pair is primary; otherwise a receiver passing the strict checks is preferred, then one with RTK fixed.
- There is no blending (`SENS_GPS_MASK` and `SENS_GPS_TAU` are gone).
  When the primary fails `GNSS_CHECK` or stops publishing, the other receiver is used.
- Antenna positions are `SENS_GNSS0_OFFX`, `SENS_GNSS0_OFFY`, `SENS_GNSS0_OFFZ` (and `SENS_GNSS1_*`), matched to receivers by `SENS_GNSSn_ID`.
  The old `SENS_GPS*` and `EKF2_GPS_POS_*` names are migrated, but shouldn't appear on a new page.
- MAVLink `GPS_RAW_INT` is the primary receiver and `GPS2_RAW` the other; they don't follow the selection.

## Compass, barometer and LEDs

- **External compasses** are probed on external I2C when `SENS_EXT_I2C_PRB` is `1` (the default), in `rc.sensors`: `ist8310`, `ist8308`, `iis2mdc`, `lis3mdl`, `qmc5883l`, `qmc5883p`, `rm3100`, `bmm350`, `hmc5883`, `ak09916`, `icm20948_i2c_passthrough`.
  Read the list at the head: a part not in it (in October 2026, `mmc5983ma` and `bmm150`) isn't started on a module unless a board starts it.
- **External barometers**: none is started by default.
  `spl06` and `spa06` start only when `SENS_EN_SPL06` or `SENS_EN_SPA06` is set.
  A module's barometer is therefore unused by PX4 on a UART receiver unless it's one of those and the parameter is set; say so rather than implying it works (G-S6).
  On a DroneCAN node, the node publishes it (`CANNODE_PUB_BAR`) and the flight controller uses it only with `UAVCAN_SUB_BARO` set.
- **LED drivers** started on external I2C in `rcS`: `rgbled`, `rgbled_ncp5623c`, `rgbled_lp5562`, `rgbled_is31fl3195`.
- **Buzzer**: `tone_alarm`, on the flight controller; the GPS connector's buzzer pin is driven by the flight controller.
- **Safety switch**: started per board (`safety_button` in `rc.board_defaults`), and safety is off by default: [COM_SAFETY_MODE](../advanced_config/parameter_reference.md#COM_SAFETY_MODE) defaults to `0` (Always off); `1` switch or MAVLink, `2` physical switch only, `3` MAVLink only.
  A page saying the module's safety switch must be pressed before arming is wrong unless it says to set `COM_SAFETY_MODE`.

## Pixhawk GPS connector

[DS-009 Pixhawk Connector Standard](https://github.com/pixhawk/Pixhawk-Standards/blob/master/DS-009%20Pixhawk%20Connector%20Standard.pdf) defines the 10-pin "Full GPS + Safety Switch Port" (`GPS1` on most Pixhawk-standard boards) and the 6-pin "Basic GPS Port" (`GPS2`), which has no safety switch, LED or buzzer pins.
`gps_compass/index.md` ("Pixhawk Standard Connectors") says which port is which and that "the ports are generally plug-n-play for u-blox modules (only)", but doesn't give the pin order.

To check a module's pinout claimed to follow the standard, read the pin table from the standard itself (extract the PDF as `shared.md` says), or from the `GPS1` pinout on a Pixhawk-standard board's page (`docs/en/flight_controller/pixhawk6x.md` or another current FMUv6 page), and compare pin by pin.
A flight controller's table names TX and RX from the controller's side and a module's names them from the module's side, so the module's RX sits on the controller's TX pin: don't report that as a swap.
Note the module's signal levels too: a UART at 2.8 V or 5 V rather than 3.3 V is worth stating on the page (G-W2).

## Lookup table

| Page claim | Source | What to look for |
| --- | --- | --- |
| **Protocol value, default** | `params.yaml` | `GPS_1_PROTOCOL` / `GPS_2_PROTOCOL` `values:` and `default:`. |
| **Detected automatically** | `gps.cpp` | The auto-detect list and its comment; `Kconfig` help for `GPS_NMEA`. "Protocol and detection" above says what the page must say. |
| **In firmware** | `src/drivers/gps/Kconfig`, `boards/**/default.px4board` | The protocol's key and its default; count the boards ("In firmware" below). |
| **Port** | `module.yaml`, `generate_config.py` | `GPS_1_CONFIG` default `GPS1`, `GPS_2_CONFIG` no default (`0`), port values. |
| **Baud** | `serial_params.c.jinja`, protocol `.cpp` | `SER_<TAG>_BAUD` default `0`; the rates each protocol probes (table above). |
| **u-blox options** | `params.yaml`, `ubx.cpp` | `GPS_UBX_MODE` (moving-base rover and base, rover with static base, UART2 output modes, Galileo HAS), `GPS_UBX_BAUD2` (applied only in some modes), `GPS_UBX_RATE` (forced to 5 Hz in moving-base modes), `GPS_UBX_DYNMODEL`, `GPS_1_GNSS` (constellations; u-blox only), `GPS_UBX_PPK`, `GPS_UBX_CFG_INTF`. |
| **Heading** | `ubx.cpp`, `nmea.cpp`, `septentrio.cpp`, `gnss_relative.cpp`, `params_heading.yaml`, `VehicleGPSPosition.cpp`, `params_gnss.yaml`, `EKF2.cpp` | "Heading" above. |
| **RTK** | `correction_injector.h`, `gps.cpp`, protocol `.cpp`, `uavcan_params.yaml`, `uavcannode_params.yaml` | "RTK" above. |
| **Selection, antenna position** | `vehicle_gps_position/module.yaml`, `VehicleGPSPosition.cpp` | "Selection and antenna position" above. |
| **Septentrio** | `src/drivers/gnss/septentrio/module.yaml`, `Kconfig` | `SEP_PORT1_CFG` (default `0`), `SEP_PORT2_CFG`, `SEP_HARDW_SETUP`, `SEP_AUTO_CONFIG` (default on), `SEP_OUTP_HZ`, `SEP_CONST_USAGE`; `DRIVERS_GNSS_SEPTENTRIO` `default n` (25 of 125 `default.px4board` files in October 2026). There are no Septentrio offset parameters any more. |
| **DroneCAN** | `uavcan_params.yaml`, `uavcannode_params.yaml`, node board files | "DroneCAN" above. Firmware targets for a PX4 node are `<vendor>_<board>_default` (and `_canbootloader`) for a board directory that exists. |
| **Compass, barometer, LEDs, safety** | `rc.sensors`, `rcS`, `commander_params.yaml` | "Compass, barometer and LEDs" above. |
| **Commands** | `gps.cpp` usage block, `septentrio.cpp` usage block | `gps start`, `stop`, `status`, `reset cold\|warm\|hot`; `-p` values; `septentrio status`. |
| **Topics** | `msg/SensorGnss.msg`, `msg/VehicleGnss.msg`, `msg/VehicleGnssHeading.msg` | `sensor_gnss` (per receiver; `listener sensor_gnss`), `vehicle_gnss` (the selected receiver), `sensor_gnss_relative` (heading from the receiver), `vehicle_gnss_heading` (heading the estimator uses), `rtcm_corrections`, `rtcm_moving_baseline`, `satellite_info` with `GPS_SAT_INFO`. The old names `sensor_gps`, `vehicle_gps_position` and `gps_inject_data` are gone. MAVLink: `GPS_RAW_INT`, `GPS2_RAW`, `GPS_RTCM_DATA`. |
| **Module reference anchor** | `docs/en/modules/modules_driver.md` | `#gps` and `#septentrio`. The `uavcan` and `uavcannode` modules have no section. |
| **First release** (for the badge, G-O2) | git history, `docs/en/releases/main.md` | The first release tag containing the commit that added the protocol or feature the page needs: `git log --diff-filter=A --format=%H -- <file>`, then `git tag --contains <sha> \| grep -E '^v1\.[0-9]+\.0$' \| sort -V \| head -1`. Protocol files live in the submodule, so map its commit back to the parent commit that bumped it. A feature only on `main` takes the version `releases/main.md` says `main` is heading for (PX4 v2.0 in October 2026). |

## In firmware

| Key | What it builds | How to read it |
| --- | --- | --- |
| `CONFIG_DRIVERS_GPS=y` | The `gps` driver, with u-blox always | 113 of 125 `default.px4board` files in October 2026; the boards without it are CAN nodes that aren't GNSS, IO boards and a few others. |
| `CONFIG_GPS_<PROTOCOL>=y` | One protocol | Defaults to `!BOARD_CONSTRAINED_FLASH`, so a board has it unless it's constrained or turns it off (`# CONFIG_GPS_NMEA is not set`). |
| `CONFIG_DRIVERS_GNSS_SEPTENTRIO=y` | The `septentrio` driver | `default n`; count the boards that set it. |
| `CONFIG_DRIVERS_UAVCAN=y` | DroneCAN on the flight controller | 75 of 125 in October 2026; count it the same way. |
| `CONFIG_EKF2_GNSS_YAW` | GNSS heading in the estimator, and with it `SENS_GNSSn_HDG` | Default on; a few small FPV boards turn it off. |

Work out, and record in the worksheet:

- **Is the protocol in most firmware?**
  u-blox always; any other protocol on every board except the constrained-flash ones.
  Name the constrained boards only when the page's example board is one of them; otherwise "boards with constrained flash" is enough, with a link to the board's configuration file as the way to check.
- **Which boards build the Septentrio driver?**
  `grep -rl "CONFIG_DRIVERS_GNSS_SEPTENTRIO=y" boards --include=default.px4board`.
- **Does a CAN node's board exist, and what does it start?**
  `ls boards/<vendor>/<board>`, its `rc.board_sensors` `gps start` line (`-p` must be a value the parser accepts), and its `rc.board_defaults`.

## Receivers and their pages

A starting map for choosing comparators; confirm each row at the base SHA before relying on it.
`existing-page-issues.md` lists known problems on many of these pages: don't use a page as a comparator for a section it gets wrong.

| Page | Connection | Protocol | Capability | Exemplar for |
| --- | --- | --- | --- | --- |
| `gps_compass/ark_dan_gps.md` | UART | u-blox | GNSS | page skeleton, Pixhawk pinout table (not its GPS2 claim) |
| `gps_compass/gps_locosys_hawk_a1.md` | UART | u-blox | GNSS | primary and secondary parameter tables, LEDs (not its I2C pin order) |
| `gps_compass/gps_smartap.md` | UART | u-blox | GNSS | compact pinout and specifications |
| `gps_compass/globalsat_bd_100m_gps.md` | UART | NMEA | GNSS | NMEA protocol configuration, features PX4 doesn't use (after PR 28969) |
| `gps_compass/globalsat_bd_100k_gps.md` | UART | NMEA | RTK | NMEA RTK configuration (after PR 28969) |
| `gps_compass/rtk_gps_holybro_unicore_um982.md` | UART | NMEA (Unicore) | RTK heading | protocol, baud, heading with `SENS_GNSSn_HDG`, RTK |
| `gps_compass/rtk_gps_trimble_mb_two.md` | UART | Ashtech/Trimble | RTK (PX4 doesn't use its heading; the page says so) | protocol value, baud, power warning |
| `gps_compass/rtk_gps_fem_mini2.md` | UART | Femtomes | RTK | (missing its protocol value) |
| `gps_compass/rtk_gps_holybro_h-rtk-f9p.md`, `rtk_gps_cuav_c-rtk-9ps.md` | UART | u-blox | RTK, dual F9P moving base | moving-base pairs, with `u-blox_f9p_heading.md` |
| `gps_compass/septentrio_mosaic-go.md`, `septentrio_asterx-rib.md` | UART-Septentrio | SBF | RTK, heading variants | connector and LED tables; configuration delegated to `septentrio.md` |
| `dronecan/ark_gps.md` | DroneCAN, PX4 node | u-blox | GNSS | non-RTK PX4 node page (not its heading line) |
| `dronecan/ark_rtk_gps.md` | DroneCAN, PX4 node | u-blox | RTK, moving base | the most complete DroneCAN page: node and flight-controller parameters, RTK, firmware, `SENS_GNSSn_HDG` (not its unconditional heading line) |
| `dronecan/holybro_h_rtk_zed_f9p_gps.md` | DroneCAN, AP_Periph | u-blox | RTK heading | AP_Periph node pattern (not its `UAVCAN_ENABLE` values) |
| `dronecan/ark_g5_rtk_gps.md`, `ark_g5_rtk_heading_gps.md` | DroneCAN, vendor | SBF | RTK, heading | vendor-firmware node pattern |
