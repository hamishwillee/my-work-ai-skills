# Protocol sources

Where each claim on a GNSS page can be checked in the PX4 source, and how to read it.
Read the files at the PR's head SHA, and the protocol implementations at the submodule commit the head records.

Source says what PX4 *does* with the receiver, not everything the receiver *can do*.
A page claim with no source counterpart (a supply voltage, a pin order, an accuracy figure) is checked against manufacturer material or left as a question; a page claim the source *contradicts* is a `bug`.

The values quoted below were read at PX4-Autopilot `origin/main` `d551d33` (22 September 2026), with `src/drivers/gps/devices` at `928062a`.
They are a map, not evidence: re-read every value you cite at the head SHA, since parameters, defaults and counts change.

## Where the source is

| Connection | Source |
| --- | --- |
| UART, `gps` driver | `src/drivers/gps/gps.cpp` (detection, injection, modes, heading offset, usage block), `params.yaml` (protocol and u-blox parameters), `module.yaml` (`GPS_1_CONFIG`, `GPS_2_CONFIG`, the start command), `Kconfig` (which protocols are built), and the protocol implementations in the submodule `src/drivers/gps/devices/src/` (`ubx.cpp`, `nmea.cpp` (NMEA and Unicore), `ashtech.cpp`, `emlid_reach.cpp`, `mtk.cpp`, `femtomes.cpp`). |
| UART, Septentrio | `src/drivers/gnss/septentrio/` (`septentrio.cpp`, `module.yaml` with `SEP_PORT1_CFG` and every `SEP_*` parameter, `Kconfig`). The `gps` driver has no SBF protocol. |
| DroneCAN | Flight controller: `src/drivers/uavcan/sensors/gnss.cpp` (the GNSS bridge) and `src/drivers/uavcan/uavcan_params.yaml`. Node, when it runs PX4: `src/drivers/uavcannode/` (`uavcannode_params.yaml`, `Publishers/GnssFix2.hpp`, `Subscribers/RTCMStream.hpp`) and the node's board, `boards/<vendor>/<board>/` (`default.px4board`, `init/rc.board_defaults`, `init/rc.board_sensors`). An AP_Periph or closed node has no source here: its parameters come from its vendor's documentation. |
| Estimator and selection | `src/modules/ekf2/params_gnss.yaml` (`EKF2_GPS_CTRL`, `EKF2_GPS_YAW_OFF`), `src/modules/ekf2/EKF2.cpp`, `src/modules/sensors/vehicle_gps_position/module.yaml` (`SENS_GPS_MASK`, `SENS_GPS_PRIME`, `SENS_GPS0_OFFX`...). |
| Compass, barometer, LEDs | `ROMFS/px4fmu_common/init.d/rc.sensors` and `rcS`, and the board's `rc.board_sensors`. |
| Serial ports | `Tools/serial/generate_config.py` (port tags, values, default ports and baud rates) and `Tools/serial/serial_params.c.jinja` (`SER_<TAG>_BAUD`). |

## GNSS facts worksheet

The main agent fills this in once per connection, in Scope, and passes it to every lens.
Each value carries the file and line it came from, so a lens can cite it as evidence without re-reading.
Take line numbers from each file on its own (`grep -n` on that file), never from several files printed together.
A value the files don't settle is written `unknown` with what was searched, never guessed.

**A comment is not proof.**
Record what the code does, not what a comment or parameter description says it does.
For example, the `GPS_YAW_OFFSET` description mentions Septentrio, but the `septentrio` driver reads `SEP_YAW_OFFS` and never `GPS_YAW_OFFSET`.

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
| RTCM injection; fix types reported (RTK float and fixed) | | |
| Heading: published by this protocol, how, and which offset parameter applies | | |
| Other driver parameters the page names or should (u-blox mode, constellations, `SEP_*`) | | |
| DroneCAN: `UAVCAN_ENABLE` values; subscriptions and their defaults; `UAVCAN_PUB_RTCM`, `UAVCAN_PUB_MBD` | | |
| DroneCAN node: firmware (PX4 board, AP_Periph, vendor); node parameters and board defaults; start line | | |
| Compass and barometer: does PX4 start a driver for the module's parts on an external bus by default | | |
| LED driver started by default; safety switch and buzzer | | |
| Commands and options; topics | | |
| Module reference anchor | | |
| First release (for the badge) | | |

## Protocol and detection

| `GPS_x_PROTOCOL` | Protocol | Kconfig key (default) | Auto-detected | Baud when `SER_<port>_BAUD` is `0` (Auto) | Heading |
| --- | --- | --- | --- | --- | --- |
| `0` | Auto detect | | | | |
| `1` (default) | u-blox UBX | `GPS_UBX` (`y`) | yes | probes 9600–921600, then configures the receiver (115200 for M8 and newer, or `GPS_UBX_BAUD1`) | yes, in moving-base modes (`GPS_UBX_MODE`) and on dual-antenna X20 (NAV-DAHEADING) |
| `2` | MTK | `GPS_MTK` (`!BOARD_CONSTRAINED_FLASH`) | yes | fixed 38400 | no |
| `3` | Ashtech / Trimble | `GPS_ASHTECH` (`!BOARD_CONSTRAINED_FLASH`) | yes | probes 9600–115200, then sets 115200 | yes (`$GPHDT`) |
| `4` | Emlid Reach | `GPS_EMLIDREACH` (`!BOARD_CONSTRAINED_FLASH`) | yes | 57600, 115200 or 230400 | no |
| `5` | Femtomes | `GPS_FEMTOMES` (`!BOARD_CONSTRAINED_FLASH`) | yes | 115200 only | only when the receiver reports heading type 6 |
| `6` | NMEA (generic, includes Unicore) | `GPS_NMEA` (`!BOARD_CONSTRAINED_FLASH`) | **never** | tries the configured rate, then 9600–230400 | yes (`$xxHDT`, Unicore `UNIHEADINGA`) |

What follows for the page:

- **The default (`1`) tries only u-blox.**
  A u-blox receiver on `GPS1` needs nothing set.
- **Auto-detection (`0`) tries u-blox, MTK, Ashtech, Emlid and Femtomes**, each only if built (`gps.cpp`, `kAutoDetectModes`).
  A receiver using one of those works with `0` or its own value; with the default `1` it isn't found, so the page has to say what to set.
- **NMEA is never auto-detected** (`gps.cpp`: "NMEA is excluded because it can produce false-positive detections"; `Kconfig` `GPS_NMEA` help: "must be selected explicitly via GPS_x_PROTOCOL").
  An NMEA or Unicore receiver needs `GPS_1_PROTOCOL` = `6`.
- **A protocol not built into the firmware** makes the driver fall back to auto-detection with a warning ("unsupported by this build, using auto-detection").
  Every protocol except u-blox is left out of boards that set `CONFIG_BOARD_CONSTRAINED_FLASH=y` (23 of 123 `default.px4board` files in September 2026, mostly CAN nodes and small FPV boards), so its page needs Firmware Support (G-F1).
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

- **Correction injection works for every protocol** on the `gps` driver: it reads `rtcm_corrections` (from MAVLink `GPS_RTCM_DATA` or DroneCAN `RTCMStream`) and writes the frames to the receiver (`gps.cpp`, `handleInjectDataTopic`, `injectRtcmFrames`).
  The Septentrio driver does the same in its own code.
- **RTK fix reporting**: u-blox NAV-PVT carrier solution gives 5 (float) or 6 (fixed); NMEA GGA quality 5 gives 5 and quality 4 gives 6; Emlid maps its own states (`nmea.cpp`, `ubx.cpp`, `emlid_reach.cpp`; constants in `msg/SensorGps.msg`).
  A receiver whose output doesn't carry an RTK state can't show an RTK fix in PX4, whatever it computes.
- **DroneCAN**: the flight controller sends corrections to the node only when `UAVCAN_PUB_RTCM` is `1` (default `0`), and a moving-base pair needs `UAVCAN_PUB_MBD` / `UAVCAN_SUB_MBD`; a PX4 node subscribes when its `CANNODE_SUB_RTCM` is `1` (default `0`, set by RTK nodes' `rc.board_defaults`).
- The base station is set up from the ground station, not by PX4 (`rtk_gps.md`, "RTK Connection Process"); a claim that the receiver can be used as a base is checked against the manufacturer facts and that page, not against PX4's source.

## Heading

- The estimator fuses GNSS heading only when [EKF2_GPS_CTRL](../advanced_config/parameter_reference.md#EKF2_GPS_CTRL) has bit 3 ("Dual antenna heading") set; the default is `7` (bits 0–2), so the usual instruction is "set to `15`".
- Which protocols publish heading, and how (`sensor_gps.heading`):

  | Source | Heading | Offset parameter |
  | --- | --- | --- |
  | u-blox, moving base (`GPS_UBX_MODE` `1`/`3` on the rover, `2`/`4` on the base) | NAV-RELPOSNED, when carrier-fixed and the baseline is valid | `GPS_YAW_OFFSET` |
  | u-blox X20 dual antenna | NAV-DAHEADING | `GPS_YAW_OFFSET` |
  | NMEA / Unicore | `$xxHDT`, Unicore `UNIHEADINGA` | `GPS_YAW_OFFSET` |
  | Ashtech / Trimble | `$GPHDT` | `GPS_YAW_OFFSET` |
  | Femtomes | when heading type is 6 | `GPS_YAW_OFFSET` |
  | Emlid, MTK | none | |
  | Septentrio | SBF AttEuler | `SEP_YAW_OFFS` and `SEP_PITCH_OFFS` (sent to the receiver); `SEP_HARDW_SETUP` `1` for moving base |
  | DroneCAN, `RelPosHeading` message | as the node sends it; the flight controller's GNSS bridge always subscribes | [EKF2_GPS_YAW_OFF](../advanced_config/parameter_reference.md#EKF2_GPS_YAW_OFF) on the flight controller (applied only when the message carries no offset) |
  | DroneCAN, PX4 node (`Fix2`) | as the node's own `gps` driver produces it | `GPS_YAW_OFFSET` set **on the node** |

- `GPS_YAW_OFFSET` is read only by the serial `gps` driver; setting it on the flight controller does nothing for a DroneCAN receiver.
- `UAVCAN_SUB_GPS_R` gates only the `sensor_gnss_relative` bridge, not heading.
- A single-antenna receiver that isn't half of a moving-base pair publishes no heading: enabling bit 3 for it is the `bug` case (G-A5).

## DroneCAN

| Parameter | Default | Notes |
| --- | --- | --- |
| `UAVCAN_ENABLE` | `0` | `1` sensors manual config, `2` sensors automatic config, `3` sensors and actuators; reboot required |
| `UAVCAN_SUB_GPS` | `1` | already on |
| `UAVCAN_SUB_GPS_R` | `1` | already on; relative position only |
| `UAVCAN_SUB_MAG` | `1` | already on |
| `UAVCAN_SUB_BARO` | `0` | needed only to use a node's barometer |
| `UAVCAN_PUB_RTCM` | `0` | needed for RTK |
| `UAVCAN_PUB_MBD`, `UAVCAN_SUB_MBD` | `0` | moving baseline over CAN |

PX4 node parameters (`uavcannode_params.yaml`): `CANNODE_NODE_ID` (`0`, dynamic allocation), `CANNODE_TERM` (`0`), `CANNODE_SUB_RTCM`, `CANNODE_SUB_MBD`, `CANNODE_PUB_MBD` (all `0` by default, set by RTK nodes' board defaults), `CANNODE_PUB_BAR` and `CANNODE_PUB_MAG` (`1`).
A parameter name a board file sets that isn't defined anywhere (`CANNODE_GPS_RTCM` on `freefly/can-rtk-gps`) is a firmware observation, never something to copy onto a page.

Selection between receivers: [SENS_GPS_PRIME](../advanced_config/parameter_reference.md#SENS_GPS_PRIME) (default `0`, the main serial GPS; `1` the secondary serial GPS; a DroneCAN node ID selects that node) has no effect while blending is active, and blending is controlled by [SENS_GPS_MASK](../advanced_config/parameter_reference.md#SENS_GPS_MASK) (default `7`).
Antenna position offsets are `SENS_GPS0_OFFX`, `SENS_GPS0_OFFY`, `SENS_GPS0_OFFZ` (and `SENS_GPS1_*`); the old `EKF2_GPS_POS_*` names are migrated and shouldn't appear on a new page.

## Compass, barometer and LEDs

- **External compasses** are probed on external I2C when `SENS_EXT_I2C_PRB` is `1` (the default), in `rc.sensors`: `ist8310`, `ist8308`, `iis2mdc`, `lis3mdl`, `qmc5883l`, `qmc5883p`, `rm3100`, `bmm350`, `hmc5883`, `ak09916`, `icm20948_i2c_passthrough`.
  Read the list at the head: a part not in it (in September 2026, `mmc5983ma` and `bmm150`) isn't started on a module unless a board starts it.
- **External barometers**: none is started by default.
  `spl06` and `spa06` start only when `SENS_EN_SPL06` or `SENS_EN_SPA06` is set.
  A module's barometer is therefore unused by PX4 on a UART receiver unless it's one of those and the parameter is set; say so rather than implying it works (G-S6).
  On a DroneCAN node, the node publishes it (`CANNODE_PUB_BAR`) and the flight controller uses it only with `UAVCAN_SUB_BARO` set.
- **LED drivers** started on external I2C in `rcS`: `rgbled`, `rgbled_ncp5623c`, `rgbled_lp5562`, `rgbled_is31fl3195`.
- **Buzzer**: `tone_alarm`, on the flight controller; the GPS connector's buzzer pin is driven by the flight controller.
- **Safety switch**: started per board (`safety_button` in `rc.board_defaults`), and the safety check is disabled by default (`CBRK_IO_SAFETY` default `22027`).
  A page saying the module's safety switch must be pressed before arming is wrong unless it says how to enable the safety check.

## Pixhawk GPS connector

[DS-009 Pixhawk Connector Standard](https://github.com/pixhawk/Pixhawk-Standards/blob/master/DS-009%20Pixhawk%20Connector%20Standard.pdf) defines the 10-pin "Full GPS + Safety Switch Port" (`GPS1` on most Pixhawk-standard boards) and the 6-pin "Basic GPS Port" (`GPS2`), which has no safety switch, LED or buzzer pins.
`gps_compass/index.md` ("Pixhawk Standard Connectors") says which port is which and that "the ports are generally plug-n-play for u-blox modules (only)", but doesn't give the pin order.

To check a module's pinout claimed to follow the standard, read the pin table from the standard itself (extract the PDF as `shared.md` says), or from the `GPS1` pinout on a Pixhawk-standard board's page (`docs/en/flight_controller/pixhawk6x.md` or another current FMUv6 page), and compare pin by pin.
A flight controller's table names TX and RX from the controller's side and a module's names them from the module's side, so the module's RX sits on the controller's TX pin: don't report that as a swap.

## Lookup table

| Page claim | Source | What to look for |
| --- | --- | --- |
| **Protocol value, default** | `params.yaml` | `GPS_1_PROTOCOL` / `GPS_2_PROTOCOL` `values:` and `default:`. |
| **Detected automatically** | `gps.cpp` | The auto-detect list and its comment; `Kconfig` help for `GPS_NMEA`. "Protocol and detection" above says what the page must say. |
| **In firmware** | `src/drivers/gps/Kconfig`, `boards/**/default.px4board` | The protocol's key and its default; count the boards ("In firmware" below). |
| **Port** | `module.yaml`, `generate_config.py` | `GPS_1_CONFIG` default `GPS1`, `GPS_2_CONFIG` no default (`0`), port values. |
| **Baud** | `serial_params.c.jinja`, protocol `.cpp` | `SER_<TAG>_BAUD` default `0`; the rates each protocol probes (table above). |
| **u-blox options** | `params.yaml` | `GPS_UBX_MODE` (heading and moving-base modes, rover with static base, UART2 output modes), `GPS_UBX_BAUD2` (applied only in some modes), `GPS_UBX_DYNMODEL`, `GPS_1_GNSS` (constellations; u-blox only), `GPS_UBX_PPK`, `GPS_UBX_CFG_INTF`. |
| **Heading** | protocol `.cpp`, `gps.cpp`, `params_gnss.yaml`, `EKF2.cpp`, `gnss.cpp` | "Heading" above. |
| **RTK** | `gps.cpp`, protocol `.cpp`, `uavcan_params.yaml`, `uavcannode_params.yaml` | "RTK" above. |
| **Septentrio** | `src/drivers/gnss/septentrio/module.yaml`, `Kconfig` | `SEP_PORT1_CFG` (default `0`), `SEP_PORT2_CFG`, `SEP_YAW_OFFS`, `SEP_PITCH_OFFS`, `SEP_HARDW_SETUP`, `SEP_AUTO_CONFIG` (default on), `SEP_OUTP_HZ`, `SEP_CONST_USAGE`; `DRIVERS_GNSS_SEPTENTRIO` `default n` (24 of 123 `default.px4board` files in September 2026). |
| **DroneCAN** | `uavcan_params.yaml`, `uavcannode_params.yaml`, node board files | "DroneCAN" above. Firmware targets for a PX4 node are `<vendor>_<board>_default` (and `_canbootloader`) for a board directory that exists. |
| **Compass, barometer, LEDs** | `rc.sensors`, `rcS` | "Compass, barometer and LEDs" above. |
| **Commands** | `gps.cpp` usage block, `septentrio.cpp` usage block | `gps start`, `stop`, `status`, `reset cold\|warm\|hot`; `-p` values; `septentrio status`. |
| **Topics** | `msg/SensorGps.msg` | `sensor_gps` (per receiver) and `vehicle_gps_position` (the selected or blended one), shown in the MAVLink console with `listener sensor_gps`; `satellite_info` with `GPS_SAT_INFO`; `rtcm_corrections`. `gps_inject_data` no longer exists. MAVLink: `GPS_RAW_INT`, `GPS2_RAW`, `GPS_RTCM_DATA`. |
| **Module reference anchor** | `docs/en/modules/modules_driver.md` | `#gps` and `#septentrio`. The `uavcan` and `uavcannode` modules have no section. |
| **First release** (for the badge, G-O2) | git history | The first release tag containing the commit that added the protocol or feature the page needs: `git log --diff-filter=A --format=%H -- <file>`, then `git tag --contains <sha> \| grep -E '^v1\.[0-9]+\.0$' \| sort -V \| head -1`. Protocol files live in the submodule, so map its commit back to the parent commit that bumped it. |

## In firmware

| Key | What it builds | How to read it |
| --- | --- | --- |
| `CONFIG_DRIVERS_GPS=y` | The `gps` driver, with u-blox always | 112 of 123 `default.px4board` files in September 2026; the boards without it are CAN nodes that aren't GNSS, IO boards and a few others. |
| `CONFIG_GPS_<PROTOCOL>=y` | One protocol | Defaults to `!BOARD_CONSTRAINED_FLASH`, so a board has it unless it's constrained or turns it off (`# CONFIG_GPS_NMEA is not set`). |
| `CONFIG_DRIVERS_GNSS_SEPTENTRIO=y` | The `septentrio` driver | `default n`; count the boards that set it. |
| `CONFIG_DRIVERS_UAVCAN=y` | DroneCAN on the flight controller | Count it the same way. |

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
| `gps_compass/rtk_gps_holybro_unicore_um982.md` | UART | NMEA (Unicore) | RTK heading | protocol, baud, heading and RTK configuration |
| `gps_compass/rtk_gps_trimble_mb_two.md` | UART | Ashtech/Trimble | RTK heading | protocol value, heading, power warning |
| `gps_compass/rtk_gps_fem_mini2.md` | UART | Femtomes | RTK heading | (missing its protocol value) |
| `gps_compass/rtk_gps_holybro_h-rtk-f9p.md`, `rtk_gps_cuav_c-rtk-9ps.md` | UART | u-blox | RTK, dual F9P heading | moving-base pairs, with `u-blox_f9p_heading.md` |
| `gps_compass/septentrio_mosaic-go.md`, `septentrio_asterx-rib.md` | UART-Septentrio | SBF | RTK, heading variants | connector and LED tables; configuration delegated to `septentrio.md` |
| `dronecan/ark_gps.md` | DroneCAN, PX4 node | u-blox | GNSS | non-RTK PX4 node page (not its heading line) |
| `dronecan/ark_rtk_gps.md` | DroneCAN, PX4 node | u-blox | RTK, moving base | the most complete DroneCAN page: node and flight-controller parameters, RTK, firmware (not its heading and `SENS_GPS_MASK` lines) |
| `dronecan/holybro_h_rtk_zed_f9p_gps.md` | DroneCAN, AP_Periph | u-blox | RTK heading | AP_Periph node pattern (not its `UAVCAN_ENABLE` values or yaw-offset link) |
| `dronecan/ark_g5_rtk_gps.md`, `ark_g5_rtk_heading_gps.md` | DroneCAN, vendor | SBF | RTK, heading | vendor-firmware node pattern |
