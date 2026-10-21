# Existing GNSS page issues

A work list of problems on GNSS pages that were already in `docs/en/` when this skill was written, for fixing in separate docs PRs.
It is **not** a source of truth: no lens reads it, and nothing here is cited as evidence in a review.

Snapshot from a survey of PX4-Autopilot `origin/main` at `d551d33`, 21 October 2026.
Line numbers are as of that commit and will drift.
Most items have not been verified individually (those citing `src/` or `boards/` lines were checked against the source at that commit): check each before fixing it, and delete an item once it's fixed upstream.

## Configuration that won't work as written

- **NMEA receivers described as plug and play.** `rtk_gps_datagnss_nano_hrtk.md` (output listed at :52, "plug and play" at :104) and `rtk_gps_gem1305.md` (:57, :109) list NMEA-only output, which PX4 never auto-detects. They need `GPS_1_PROTOCOL` = `6`, unless the vendor confirms the receivers also output UBX.
- **"Plug-n-play on GPS2".** `ark_dan_gps.md`, `ark_sam_gps.md` and `ark_sam_gps_mini.md` (around :42–43). `GPS_2_CONFIG` has no default port (it is `0`, Disabled: `src/drivers/gps/module.yaml:6` has no `default:`, and `Tools/serial/generate_config.py:264` sets `default_port = 0`), so a receiver on `GPS2` needs it set.
- **`SER_GPS2_BAUD` without `GPS_2_CONFIG`.** `rtk_gps_locosys_r1.md:48` and `rtk_gps_locosys_r2.md:70`. Also `rtk_gps_locosys_r1.md:50` shows `SER_GPS2_BAUD` but links `#SER_GPS1_BAUD`.
- **Femtomes protocol not given.** `rtk_gps_fem_mini2.md:49` doesn't say to set `GPS_1_PROTOCOL` = `5` (Femtomes isn't the default), nor the heading-fusion setting.
- **Heading fusion on receivers without heading.** `dronecan/ark_gps.md:92`, `dronecan/holybro_m8n_gps.md:94`, `dronecan/ark_rtk_gps_l1_l2.md:85` and `dronecan/ark_x20_rtk_gps.md:88` tell the reader to set `EKF2_GPS_CTRL` bit 3. `dronecan/ark_rtk_gps.md:85` says it unconditionally. The conditional wording in `dronecan/index.md:196` is the right model.
- **`SENS_GPS_MASK` = 7 "to ensure heading is published".** `dronecan/ark_rtk_gps.md:86`, `ark_rtk_gps_l1_l2.md:86`, `ark_x20_rtk_gps.md:89`, `ark_g5_rtk_heading_gps.md:100`. 7 is the default, and the stated effect is unsupported. `SENS_GPS_PRIME`'s own description says it has no effect while blending is on, which contradicts `ark_rtk_gps.md:87`, `:142` and `:161`.
- **Missing `UAVCAN_PUB_RTCM`** (off by default) on the RTK DroneCAN pages `dronecan/ark_g5_rtk_gps.md`, `dronecan/ark_g5_rtk_heading_gps.md` and `dronecan/holybro_h_rtk_zed_f9p_gps.md`.
- **Contradictory `UAVCAN_ENABLE`.** `dronecan/holybro_h_rtk_zed_f9p_gps.md:113` sets `1`, contradicting `2` at `:76`. At `:116` the link text says `EKF2_GPS_YAW_OFF` but the anchor is `#GPS_YAW_OFFSET`.
- **Septentrio heading.** `septentrio.md:113-123` says heading "works automatically" and never mentions heading fusion in `EKF2_GPS_CTRL`.
- **`GPS_YAW_OFFSET` for DroneCAN.** `dronecan/index.md:231` tells users to set `GPS_YAW_OFFSET` on the flight controller, but only the serial `gps` driver reads it; for a node sending `RelPosHeading` the flight controller applies `EKF2_GPS_YAW_OFF` (`EKF2.cpp:2637-2643`), and a PX4 node needs `GPS_YAW_OFFSET` set on the node.
- **Serial port claims.** `peripherals/serial_configuration.md:71` says there's no feedback about conflicting ports, but `rc.serial_port.jinja:14` prints "Conflicting config" on non-constrained boards; `:86-87` says GPS detects the baud rate automatically, but MTK is fixed at 38400 and Femtomes tries only 115200.
- **Wrong firmware targets.** `dronecan/ark_x20_rtk_gps.md:67-68`, `:138` give `ark_can-rtk-gps_*`, but the board is `boards/ark/x20-gps`. The L1 L5 page may also be wrong; confirm with ARK.
- **ARK G5 Heading parameter names.** `dronecan/ark_g5_rtk_heading_gps.md:108-138`: `SEP_OFFS_YAW`, `SEP_OFFS_PITCH` and `SEP_OUT_RATE` are ARK node firmware parameters, close to but not the same as PX4's `SEP_YAW_OFFS`, `SEP_PITCH_OFFS` and `SEP_OUTP_HZ`. Say whose they are.
- **No PX4 configuration at all.** `gps_cuav_neo_3.md`, `gps_holybro_m8n_m9n.md`, `dronecan/ark_teseo_gps.md`, `dronecan/ark_mosaic__rtk_gps.md` (stub), `rtk_gps_hex_hereplus.md`. `rtk_gps_cuav_c-rtk2.md:101` gives a vendor link only.

## Firmware observations (not page fixes)

- `boards/ark/septentrio-gps/init/rc.board_sensors:5` runs `gps start -p sbf`, but the `gps` `-p` parser accepts only `ubx`, `mtk`, `ash`, `eml`, `fem` and `nmea` (`gps.cpp:2010-2049`, "unknown protocol"), `sbf.cpp` isn't compiled, and the board doesn't enable the Septentrio driver. Raise with the board's maintainers.
- `boards/freefly/can-rtk-gps/init/rc.board_defaults:6` sets `CANNODE_GPS_RTCM`, which isn't defined anywhere (the parameter is `CANNODE_SUB_RTCM`).
- `src/drivers/gps/Kconfig:51` mentions the removed `gps_inject_data` topic.
- `GPS_1_PROTOCOL` has `max: 7` but `GPS_2_PROTOCOL` `max: 6` (`params.yaml:257`, `:277`), and the `GPS_YAW_OFFSET` description mentions Septentrio, whose driver reads `SEP_YAW_OFFS` instead.
- `boards/ark/teseo-gps` has no `default.px4board`, so there is no PX4 node firmware for the Teseo page to point at.

## Copy-paste drift between siblings

- `dronecan/holybro_m8n_gps.md:78`, `:97` say "ARK GPS".
- Intro or See Also points at the wrong product:
  - `ark_sam_gps_mini.md:3`, `:61` → SAM.
  - `dronecan/ark_rtk_gps_l1_l2.md:3`, `:167` → ARK RTK.
  - `dronecan/ark_g5_rtk_heading_gps.md:7`, `:150` → G5.
- `dronecan/ark_g5_rtk_gps.md:9`: the mosaic-G5 P3 text links a u-blox X20P URL.
- `rtk_gps_cuav_c-rtk.md:3` and `rtk_gps_cuav_c-rtk2.md:3`, `:113` link the 9Ps product page.
- Reused hero images: `rtk_gps_locosys_r1.md:31` and `rtk_gps_locosys_r2.md:29` use the Hawk A1 image; `dronecan/ark_g5_rtk_heading_gps.md:11` uses the G5 image.

## Stale statements

- `rtk_gps_cuav_c-rtk.md:24` says PX4 doesn't fully support a second GPS.
- `rtk_gps_freefly.md:70` says the CAN MCU is "for future", though `boards/freefly/can-rtk-gps` exists.
- `rtk_gps_fem_mini2.md:11` says the drivers are "under development".
- The protocol lists are incomplete:
  - `index.md:4`, `:20`, `:135` (Femtomes, SBF, and until PR 28969 NMEA, are missing).
  - `rtk_gps.md:17` lists only M8P, F9P and MB-Two.
  - `septentrio.md:3` lists only X5 and H.
- `rtk_gps.md:21` has the typo "discontined".

## Device tables

- **`rtk_gps.md` table:**
  - Rows 28–30, 38–39 and the Holybro rows are out of alphabetical order.
  - Rows 32 and 34 both list C-RTK2, and 34 links `c-rtk.md`.
  - Discontinued devices are listed (35, 49), despite the statement at :19.
  - Row 36 says Here3 "(M8N)" but its GPS column says M8P.
  - SIRIUS appears twice (37, 59).
  - The DroneCAN cell is blank for a DroneCAN product (48).
  - Row 61 gives Trimble MB-Two the GPS F9P and a compass, which the survey thinks are both wrong.
  - Row 29 marks the mosaic-X5 as yaw-capable, but it's single-antenna.
- **`index.md` table:**
  - It lists RTK devices: Hawk R1/R2 (47–48) and Emlid Reach (37).
  - The H rows (38–45) are unsorted.
  - Row 36 says "CubePilot Here2" where `SUMMARY.md` says "Hex Here2".
- **`dronecan/index.md` "Supported Hardware"** (:44–58) misses ARK Teseo, G5, G5 Heading, L1 L5, X20 and MOSAIC, and lists C-RTK2 as DroneCAN.

## SUMMARY.md

- The GNSS entries around lines 269–273 are unsorted.
- The `(CAN)` suffix is inconsistent: ARK TESEO and the G5 pages lack it.
- `✘` entries are placed inconsistently: mid-list (271), alphabetical (291), at the end (299).
- A topic page (281, u-blox heading) sits among the devices.
- "Femtones" in the title vs "Femtomes" in the driver and the vendor's domain.

## Headings, images and form

- `rtk_gps_cuav_c-rtk2.md:24` has a second H1.
- `gps_holybro_m8n_m9n.md:12` puts an H3 directly under the H1.
- `## Hardware setup` is lower case on `ark_dan_gps.md` and its siblings.
- `dronecan/holybro_h_rtk_zed_f9p_gps.md:74` nests "Enable DroneCAN" under "Firmware Setup".
- Wrong or missing alt text:
  - `rtk_gps_holybro_unicore_um982.md:5` has "HB-pmw3901-1".
  - `rtk_gps_holybro_h-rtk-f9p.md:43`, `:45` have their alt texts swapped.
  - `<img>` with no alt: `gps_hex_here2.md:17`, `gps_holybro_m8n_m9n.md:10`, `rtk_gps_cuav_c-rtk.md:6`, `rtk_gps_hex_hereplus.md:13`.
- Specifications given only as images: `rtk_gps_cuav_c-rtk-9ps.md:19`, `rtk_gps_holybro_h-rtk-f9p.md:49`, `rtk_gps_holybro_h-rtk-m8p.md:40`.
- `gps_locosys_hawk_a1.md:64-65` has SDA/SCL swapped relative to the Pixhawk standard (pin 4 SCL, pin 5 SDA), and `:74` defines PPS as "Precise Positioning Service".
- `rtk_gps_locosys_r1.md:60-70` gives a 9-pin table for a "6-pin" cable.
- Tracking query strings on marketplace links (`gps_cuav_neo_3x.md:40`, `rtk_gps_cuav_c-rtk.md:10-11`) and Septentrio tracking redirects.
- Vendor voice: `rtk_gps_fem_mini2.md:65` "contacting us", `septentrio_asterx-rib.md:3` "the leading worldwide supplier".
- Chip naming varies ("Ublox NEO M9N", "UBLOX", "UBlox"; should be u-blox). The DATAGNSS pages name only "CYNOSURE", while the table gives D10P/TAU951M.
- `rtk_gps_drotek_xl.md` is an orphan stub, not in `SUMMARY.md`.
