# Driver sources

Where each claim on a rangefinder page can be checked in the PX4 source, and how to read it.
Read the files at the PR's head SHA.

Driver source says what PX4 *does* with the sensor, not everything the sensor *can do*.
A page claim with no source counterpart (a supply voltage, a pin order) is checked against manufacturer material or left as a question; a page claim the source *contradicts* is a `bug`.

## Where the source is

| Connection | Source |
| --- | --- |
| Serial, I2C, PWM | The driver directory, `src/drivers/distance_sensor/<driver>/` (some sit one level down: `sony/`, `broadcom/afbrs50/`). Find it from the page: the parameter it names (`grep -rn "SENS_PTGL100_CFG" src/drivers/distance_sensor`) or the command it runs. |
| DroneCAN | `src/drivers/uavcan/sensors/rangefinder.cpp` and `src/drivers/uavcan/uavcan_params.yaml` on the flight-controller side. The sensor itself runs its own firmware; when that's PX4 (an ARK node), its board directory under `boards/` and the driver it starts are evidence too. |
| MAVLink | `handle_message_distance_sensor` in `src/modules/mavlink/mavlink_receiver.cpp`. |

One page can use several drivers (the LightWare page uses `lightware_laser_i2c` and `lightware_laser_serial`; Lidar-Lite uses `ll40ls` and `ll40ls_pwm`): fill in the worksheet once per driver.

## Rangefinder facts worksheet

The main agent fills this in once per driver, in Scope, and passes it to every lens.
Each value carries the file and line it came from, so a lens can cite it as evidence without re-reading.
Take line numbers from each file on its own (`grep -n` on that file), never from several files printed together.
A value the files don't settle is written `unknown` with what was searched, never guessed.

**A comment is not proof.**
Record what the code does, not what a comment says it does.
This matters most where a driver detects the hardware version and sets limits from it: a comment such as "v1 and v3 don't have the unit id register" is the author's belief about the hardware, and can be wrong.
Record the condition the code tests ("hardware version register > 0 and unit id > 0 → 35 m"), and, where the manufacturer facts list the sensor's registers or identification, check which branch a given model would really take.
If the two disagree, the worksheet says the limit for that model is unverified, gives the possible values, and the disagreement goes below the tables as a firmware question.

| Fact | Value | Source (file:line) |
| --- | --- | --- |
| Driver directory and command name | | |
| Driver's own Kconfig key | | |
| In the common set (`COMMON_DISTANCE_SENSOR` selects it) | yes / no | |
| Boards setting the common-set key (count of all `default.px4board`) | | |
| Boards setting the driver's own key (list) | | |
| Started by a board itself (`rc.board_sensors`) | | |
| Connection (serial / I2C / PWM / DroneCAN / MAVLink) | | |
| Enabling parameter, its values and default | | |
| Start line (the `serial_config` command or the `rc.sensors` block) | | |
| Baud rate; set by the driver on the port; set by the driver on the sensor | | |
| Driver transmits to the sensor | yes / no | |
| I2C address; external bus only | | |
| Models (parameter value → model → min/max range) | | |
| Range limits published (min, max) | | |
| Field of view; sensor type | | |
| Orientation (parameter, default, or fixed) | | |
| Update rate | | |
| Other parameters (name, values, default, reboot required) | | |
| Topic published (`distance_sensor` / `obstacle_distance`) | | |
| Commands and options | | |
| Module reference anchor | | |

## Lookup table

| Page claim | Source | What to look for |
| --- | --- | --- |
| **Command name** | `CMakeLists.txt`, the `*_main.cpp` or driver `.cpp` | `MAIN <name>` in `CMakeLists.txt`; `PRINT_MODULE_USAGE_NAME("<name>", "driver")`. This is what the page runs (`ptgl100 status`) and the module reference anchor. |
| **Kconfig key** | `Kconfig` in the driver directory | `menuconfig DRIVERS_DISTANCE_SENSOR_<X>` gives the board key `CONFIG_DRIVERS_DISTANCE_SENSOR_<X>=y`. The menuconfig path is **Drivers > Distance sensors**. |
| **In firmware** | `src/drivers/distance_sensor/Kconfig`, `boards/**/*.px4board` | See "In firmware" below. |
| **Serial port parameter** | `module.yaml` | `serial_config:` → `port_config_param.name` (`SENS_<X>_CFG`). The `command:` line is what runs at boot, with every option it passes (`-R p:SENS_PTGL100_ROT`). Port values come from `Tools/serial/generate_config.py`: `0` is disabled, `102` is `TELEM 2`, `202` is `GPS 2`. |
| **Baud rate** | the driver `.cpp`/`.hpp` | A `B115200`-style constant with `cfsetispeed`/`cfsetospeed`, or `_uart.setBaudrate(...)`. It can depend on the model (`lightware_laser_serial` uses 9600 below model 5 and 115200 from it) or be probed (`sony_asdt1` tries 921600 then 115200). When the driver sets the port's rate, the user doesn't set `SER_<port>_BAUD`. Whether the driver also sets the *sensor's* rate is separate: look for a baud command written to the sensor. If there's none, the sensor must already be at the driver's rate, and the page has to say so (R-C1). |
| **Driver transmits** | the driver `.cpp` | A `write(` to the port (a start-measurement or configuration command) means both TX and RX must be wired. A driver that only reads needs the sensor's TX alone. |
| **I2C enabling parameter** | `parameters.yaml` or `params.yaml` | `SENS_EN_<X>`, with its `values:` (often the model list) and `default:`. |
| **I2C start line** | `ROMFS/px4fmu_common/init.d/rc.sensors` | `if param compare -s SENS_EN_<X> 1` / `param greater -s SENS_EN_<X> 0`, then `<driver> start -X`. `-X` means external buses only. A board can also start a driver itself in `boards/<vendor>/<board>/init/rc.board_sensors`. |
| **I2C address** | the driver `.hpp`/`_main.cpp` | `cli.i2c_address = <X>_BASEADDR`, `PRINT_MODULE_USAGE_PARAMS_I2C_ADDRESS(0x..)`. Addresses in source are 7-bit. A `set_address` command or an address scan means it can be changed. |
| **PWM pins** | `rc.sensors`, board `board_config.h` | `ll40ls_pwm` starts after `pwm_input`; the capture pin is fixed per board (`PWMIN` definitions). |
| **Models detected at run time** | the driver's `probe()` or `init()` | Where there is no model parameter, the driver reads version or identity registers and branches on them. Write down each branch as its tested condition and the limits it sets, and treat the model named in a comment beside it as unconfirmed ("A comment is not proof", above). |
| **Models** | the model parameter in `parameters.yaml`/`module.yaml`, and the `switch` on it in the driver | Each `values:` entry is a model the driver supports for that connection. The two LightWare drivers have *different* lists and numbering (`SENS_EN_SF1XX` for I2C, `SENS_EN_SF0X` for serial), so check each model against the driver for the connection the page gives it. |
| **Range** | the driver `.cpp`/`.hpp` | `set_min_distance(...)` / `set_max_distance(...)`, or `report.min_distance`/`max_distance`, per model where there's a `switch`. These are the limits the estimator is given: a reading outside them is treated as out of range. A comment beside them often gives the datasheet figure when the driver narrows it (`// Datasheet: 0.17m`). |
| **Field of view, type** | the driver `.cpp` | `set_fov(...)` (radians), `set_hfov`/`set_vfov`; `set_rangefinder_type(distance_sensor_s::MAV_DISTANCE_SENSOR_LASER / _ULTRASOUND / _RADAR / _INFRARED)`. No `set_fov` call means the field of view is published as unknown. |
| **Orientation** | `module.yaml`, the usage block | An orientation parameter (`SENS_<X>_ROT`, `SF1XX_ROT`) and its default (`25` is downward, `24` upward, `0` forward). A `-R` option in the usage block with no parameter passed to it in the `serial_config` command or `rc.sensors` line means the direction is fixed at the option's default when the driver is started the normal way. |
| **Update rate** | the driver `.cpp`/`.hpp` | `ScheduleOnInterval(...)`, a `*_MEASURE_INTERVAL` or `*_CONVERSION_INTERVAL` constant, or a rate parameter. A poll interval is how often the driver looks for data, not the sensor's output rate; only cite it against a page claim about how often PX4 publishes. |
| **Other parameters** | `module.yaml`, `parameters.yaml`, `params.yaml` | Every definition under `parameters:`, with `values:`, `default:` and `reboot_required:`. |
| **Topic** | the driver `.hpp` | A `PX4Rangefinder` member publishes `distance_sensor`, sent over MAVLink as `DISTANCE_SENSOR`. A `uORB::Publication<obstacle_distance_s>` publishes `obstacle_distance` (`OBSTACLE_DISTANCE`), used only by Collision Prevention (`lightware_sf45_serial`, `sony_asdt1`). |
| **Commands** | the usage block, and the command dispatch in the `*_main.cpp` | `PRINT_MODULE_USAGE_COMMAND*` and `PRINT_MODULE_USAGE_PARAM_*` list the documented commands and options, and `PRINT_MODULE_USAGE_DEFAULT_COMMANDS()` adds `stop` and `status`. The usage block can be incomplete, so also read the dispatch (`strcmp(argv[...], "status")`): a command handled there works even when the usage block and module reference don't list it (`ulanding_radar status`). |
| **First release** (for the badge, R-O2) | git history | The first release tag containing the commit that added the driver: `git log --diff-filter=A --format=%H -- <driver dir or its earlier path> \| tail -1`, then `git tag --contains <sha> \| grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' \| sort -V \| head -1`. Count patch releases too: the TFmini driver first shipped in `v1.7.3`, not `v1.8.0`, so its badge is `PX4 v1.7`. The badge names the major and minor version only. Drivers have moved (`src/drivers/ulanding` → `src/drivers/distance_sensor/ulanding_radar`), so follow the path back. |
| **Module reference anchor** | `docs/en/modules/modules_driver_distance_sensor.md` | The page is generated from the usage blocks; the anchor is the command name with underscores as hyphens (`#lightware-laser-i2c`). For a driver added in the same PR the section won't exist until the reference is regenerated after merge: check the command name instead, and note the pending anchor below the tables rather than reporting it. |
| **DroneCAN: enabling** | `src/drivers/uavcan/uavcan_params.yaml` | `UAVCAN_ENABLE` (`2` is "Sensors Automatic Config", `3` adds ESCs), `UAVCAN_SUB_RNG` (off by default, reboot required). |
| **DroneCAN: range** | `src/drivers/uavcan/sensors/rangefinder.cpp` | Min and max come from `UAVCAN_RNG_MIN` and `UAVCAN_RNG_MAX`, not from the sensor, so the page must give this sensor's values. Type, field of view and orientation come from the node's messages. Signal quality is 100 for a valid reading and 0 otherwise, which is why DroneCAN pages set `EKF2_RNG_QLTY_T`. |
| **MAVLink** | `src/modules/mavlink/mavlink_receiver.cpp` | Range limits, type and orientation come from the `DISTANCE_SENSOR` message. The page gives the `MAV_X_CONFIG` port and the `SER_<port>_BAUD` rate, which nothing sets automatically. |
| **Estimator parameters** | `src/modules/ekf2/params_range_finder.yaml` | The `EKF2_RNG_*` names a page mentions exist, and a value it recommends is within range. |

## In firmware

A driver gets into a board's firmware through either of two keys in the board's `.px4board` file, and the page's Firmware Support section (R-F1 to R-F10) has to say which apply.

| Key | What it builds | How to read it |
| --- | --- | --- |
| `CONFIG_DRIVERS_DISTANCE_SENSOR_<X>=y` | This driver alone | The `menuconfig DRIVERS_DISTANCE_SENSOR_<X>` symbol in the driver's own `Kconfig`. Every driver has one. |
| `CONFIG_COMMON_DISTANCE_SENSOR=y` | The common set | `menuconfig COMMON_DISTANCE_SENSOR` in `src/drivers/distance_sensor/Kconfig`; each `select DRIVERS_DISTANCE_SENSOR_<X>` line under it is a driver in the set. Only drivers in that list have this second key. |

Work out, and record in the worksheet:

- **Is the driver in the common set?**
  Read the `select` list at the head SHA every time: a PR adding a driver can add it to the list.
  At the time of writing it holds `lightware_laser_i2c`, `lightware_laser_serial`, `ll40ls`, `tf02pro`, `tfmini`, `ulanding_radar`, `vl53l0x` and `vl53l1x`.
- **How many boards set the common-set key?**
  `grep -rl "CONFIG_COMMON_DISTANCE_SENSOR=y" boards --include=default.px4board | wc -l` against `ls boards/*/*/default.px4board | wc -l` (86 of 124 in October 2026).
  That ratio is what backs "most boards" (R-F5); if it falls below about half, the standard sentence is no longer true and that goes below the tables.
- **Which boards set the driver's own key?**
  `grep -rl "CONFIG_DRIVERS_DISTANCE_SENSOR_<X>=y" boards --include=*.px4board`.
  Leave out test targets (`boards/px4/sitl/test.px4board`) when naming boards for the page.
  Map each to its page with `grep -l "<vendor>_<board>_default" docs/en/flight_controller/*.md`.
- **Does anything start it without a parameter?**
  `grep -rn "<driver> start" boards ROMFS`.
  Normally only the `serial_config` command or the `rc.sensors` block does, behind the enabling parameter (R-F8).

What the page then says:

- **In the common set**: both keys, "most boards", no top-of-page note.
- **Not in the common set**: the driver's own key only, the boards that set it, and the top-of-page note (R-O6).

For a DroneCAN sensor the flight controller needs `CONFIG_DRIVERS_UAVCAN=y` instead (75 of 124 `default.px4board` files in October 2026); count it the same way (R-F10).

## Drivers and their pages

A starting map for finding a page's driver and choosing comparators; confirm each row at the base SHA before relying on it.

| Driver | Page | Connection | Enabling parameter | Publishes |
| --- | --- | --- | --- | --- |
| `cm8jl65` | `sensor/cm8jl65_ir_distance_sensor.md` | Serial | `SENS_CM8JL65_CFG` | `distance_sensor` |
| `leddar_one` | `sensor/leddar_one.md` | Serial | `SENS_LEDDAR1_CFG` | `distance_sensor` |
| `lightware_grf_serial` | `sensor/grf_lidar.md` | Serial | `SENS_EN_GRF_CFG` | `distance_sensor` |
| `lightware_laser_i2c` | `sensor/sfxx_lidar.md` | I2C | `SENS_EN_SF1XX` | `distance_sensor` |
| `lightware_laser_serial` | `sensor/sfxx_lidar.md` | Serial | `SENS_SF0X_CFG`, model in `SENS_EN_SF0X` | `distance_sensor` |
| `lightware_sf45_serial` | `sensor/sf45_rotating_lidar.md` | Serial | `SENS_EN_SF45_CFG` | `obstacle_distance` |
| `ll40ls`, `ll40ls_pwm` | `sensor/lidar_lite.md` | I2C, PWM | `SENS_EN_LL40LS` | `distance_sensor` |
| `mb12xx` | `sensor/rangefinders.md` (section only) | I2C | `SENS_EN_MB12XX` | `distance_sensor` |
| `ptgl100` | `sensor/ptgl100.md` | Serial | `SENS_PTGL100_CFG` | `distance_sensor` |
| `sony_asdt1` | `sensor/sony_asdt1.md` | Serial | `SENS_ASDT1_CFG` | `obstacle_distance` |
| `teraranger` | `sensor/teraranger.md` | I2C | `SENS_EN_TRANGER` | `distance_sensor` |
| `tfmini` | `sensor/tfmini.md` | Serial | `SENS_TFMINI_CFG` | `distance_sensor` |
| `ulanding_radar` | `sensor/ulanding_radar.md` | Serial | `SENS_ULAND_CFG` | `distance_sensor` |
| `vl53l1x` | `sensor/rangefinders.md` (section only) | I2C | `SENS_EN_VL53L1X` | `distance_sensor` |
| `uavcan` rangefinder bridge | `dronecan/ark_dist.md`, `dronecan/ark_dist_mr.md`, `dronecan/smartmicro_t132.md`, `dronecan/avanon_laser_interface.md` | DroneCAN | `UAVCAN_SUB_RNG` | `distance_sensor` |

Drivers with no page (`gy_us42`, `mappydot`, `pga460`, `srf02`, `srf05`, `tf02pro`, `vl53l0x`) appear only in the module reference.
