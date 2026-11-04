# Board sources

Where each claim on a flight-controller page can be checked in `boards/<vendor>/<board>/`, and how to read it.
Paths below are relative to the board directory.
Read the files at the PR's head SHA.

Board source says what PX4 *configures*, not everything the hardware *has*.
A connector the firmware doesn't use (an unpopulated header, a port reserved for another autopilot stack) won't appear in it.
So a page claim with no source counterpart is a question for the reviewer, not a `bug`; a page claim the source *contradicts* is a `bug`.

## Board facts worksheet

The main agent fills this in once, in Scope, from the files named in the lookup table, and passes it to every lens.
Each value carries the file and line it came from, so a lens can cite it as evidence without re-reading.
A value the files don't settle is written `unknown` with what was searched, never guessed.

| Fact | Value | Source (file:line) |
| --- | --- | --- |
| Build targets | | |
| Main processor (part, core, clock, flash, RAM) | | |
| PX4IO coprocessor | yes / no | |
| Serial ports (UART → `/dev/ttyS*` → label, flow control), including console and IO link | | |
| FMU outputs, capture channels, timer groups, DShot outputs, bidirectional DShot outputs | | |
| IO outputs | 8 / 0 / 8 on carriers that fit a PX4IO | |
| RC path(s): FMU UART, FMU PPM pin, PX4IO | | |
| RC wiring limits (single-wire, swap, shared PPM pin, inversion, Spektrum power); DSM bind pin and the connectors it reaches | | |
| RC drivers built; RC protocols enabled by default | | |
| IMUs, barometers, magnetometers (bus, internal/external, revision-specific) | | |
| Power inputs; monitor type and chips; enabled by default | | |
| I2C buses (external/internal), SPI buses, CAN buses | | |
| Ethernet, SD card, heater, OSD, USB | | |
| Differences from `boards/px4/<design>/` | | |
| Variant builds: what each `<variant>.px4board` changes from `default.px4board` that affects a page claim | | |
| Hardware variants, their variant-only parts, and the first PX4 release with each part's driver | | |

## Lookup table

| Page claim | Source | What to look for |
| --- | --- | --- |
| Build target(s) | `*.px4board` | `default.px4board` → `make <vendor>_<board>_default`; each `<variant>.px4board` → `make <vendor>_<board>_<variant>` |
| Variant builds | `<variant>.px4board` | A variant file lists only what it changes from `default.px4board`, so read each one in full. Record every change that affects a page claim: `CONFIG_DRIVERS_PX4IO=n` (the FMU outputs are labelled `MAIN`, not `AUX`, and there's no IO RC path), RC drivers, power monitor drivers, sensors, serial ports. Page claims about those then hold for the default firmware only (T-P11). |
| Main processor | `nuttx-config/nsh/defconfig` | `CONFIG_ARCH_CHIP_<PART>=y` (for example `CONFIG_ARCH_CHIP_STM32H753II=y`). Drop the two-character package suffix to get the model (`STM32H753`), then look it up in "Processors" below. An i.MX RT part has no internal flash: its code store is the external flash in `nuttx-config/scripts/script.ld` and the FlexSPI configuration. |
| PX4IO coprocessor | `src/board_config.h`, `default.px4board`, `extras/` | `PX4IO_SERIAL_DEVICE` (or `HAVE_PX4IO`, `PX4IO_DEVICE_PATH`) in `board_config.h`, `CONFIG_DRIVERS_PX4IO=y`, and usually `extras/px4_io-v2_default.bin`. A PX4IO is always an STM32F100 with 8 outputs. |
| IMUs, barometers, magnetometers | `init/rc.board_sensors`, `default.px4board` | The driver `start` lines in `rc.board_sensors` are what actually runs; `CONFIG_DRIVERS_IMU_*`, `_BAROMETER_*`, `_MAGNETOMETER_*` only say what's built. A sensor the page lists but no start line starts is `bug`, unless a generic probe (`i2c_launcher`, external-bus autostart) covers it and the page presents it as external. `-I` means internal bus, `-X` external; `-b <n>` is the bus number. A comment directly above a start line often names the connector (`# External compass on GPS1/I2C1`). |
| Sensor variants by hardware revision | `init/rc.board_sensors` | `ver hwtypecmp` / `ver hwbasecmp` blocks. A board whose source starts different sensors per revision needs the page to say which revision has which. |
| First PX4 release with a driver | git history of the driver directory | For a part only some hardware variants have (an extended-range IMU), find the first release tag whose tree has its driver directory: walk `git -C <clone> tag --sort=v:refname \| grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$'` and stop at the first tag where `git -C <clone> ls-tree -d --name-only <tag> src/drivers/<path>` prints the path (fetch tags first if the clone has none). Don't use `git tag --contains` on the commit that added the driver: drivers often reach a release by a cherry-pick with a different SHA, so it reports a later release (the IIM-42653 driver: v1.15.0 by `--contains`, v1.14.0 by tree). A release later than the page's badge needs stating (T-S7). Check that the manufacturer's docs or store page agree. |
| Serial port labels → `/dev/ttyS*` | `default.px4board`, `nuttx-config/nsh/defconfig` | `CONFIG_BOARD_SERIAL_<LABEL>="/dev/ttySn"` gives label → device (`TEL<n>` is the Kconfig spelling of `TELEM<n>`). The UART behind each device: take the enabled UARTs from the defconfig (`CONFIG_<CHIP>_USART1=y`, `..._UART4=y`, ...), sort them by "UART order" below, and number them from `ttyS0`. This is the method in `docs/en/hardware/serial_port_mapping.md`. |
| Debug/system console port | `nuttx-config/nsh/defconfig` | `CONFIG_<UART>_SERIAL_CONSOLE=y`. The console has no `CONFIG_BOARD_SERIAL_*` label; the page labels it as the debug console. |
| PX4IO link | `src/board_config.h` | `PX4IO_SERIAL_DEVICE "/dev/ttySn"`. It has no `CONFIG_BOARD_SERIAL_*` label either. When `CONFIG_BOARD_SERIAL_RC` names the same device, the IO also carries RC; check the reference board before treating it as a conflict (`source-consistency.md`). |
| Flow control on a port | `nuttx-config/include/board.h`, defconfig | Both `GPIO_<UART>_RTS` and `GPIO_<UART>_CTS` defined, or `CONFIG_<UART>_IFLOWCONTROL` / `_OFLOWCONTROL`. |
| RC wired to the FMU | `default.px4board`, `src/board_config.h` | `CONFIG_BOARD_SERIAL_RC="/dev/ttySn"` and `RC_SERIAL_PORT` name the FMU UART on the RC port; `GPIO_PPM_IN` / `HRT_PPM_CHANNEL` give the FMU a PPM capture pin. |
| RC wired to the PX4IO | PX4IO present | On a Pixhawk-style board the `RC IN` connector goes to the IO, which autodetects PPM, S.BUS/S.BUS2, DSM/DSM2/DSM-X, ST24 and SUMD (`docs/en/modules/modules_driver.md#px4io`); CRSF and GHST can't go through the IO. Board source can't show which connector the IO's RC input is routed to; the page has to say, and a board with both paths needs both described. |
| RC wiring that limits protocols | `src/board_config.h`, defconfig | `RC_SERIAL_SINGLEWIRE` / `RC_SERIAL_SINGLEWIRE_FORCE` (half-duplex on one pin), `RC_SERIAL_SWAP_RXTX`, `RC_SERIAL_PORT_SHARED_PPM_PIN_GPIO_RX` (PPM and serial RC share a pin), `RC_INVERT_INPUT` / `RC_SERIAL_INVERT_RX_ONLY` (S.BUS inversion), `SPEKTRUM_POWER` (DSM bind needs switchable receiver power; see "DSM bind pin"). No PPM capture pin means no PPM on the FMU. STM32F4 UARTs can't invert in hardware, so S.BUS on an F4 FMU port needs an inverter on the board. |
| DSM bind pin | `src/board_config.h` | `SPEKTRUM_RX_AS_GPIO_OUTPUT()` and `SPEKTRUM_OUT()` name the pin the bind pulses go out on. It's often the PPM input pin driven as an output (`GPIO_PPM_IN_AS_OUT`), not the RC UART's RX pin, so a DSM receiver on the serial RC connector may not be bindable from PX4 or _QGroundControl_. Which connectors that pin reaches isn't in board source: take it from the manufacturer's pinout or schematic, or raise it as a question. `SPEKTRUM_POWER` names the switchable receiver supply (for example `VDD_3V3_SPEKTRUM`), which the pinout shows on a particular pin of the RC connector. |
| RC protocols built in | `default.px4board` | `CONFIG_DRIVERS_RC_INPUT=y` builds `rc_input`, one driver that autodetects PPM, S.BUS, DSM, ST24, SUMD, CRSF and GHST (`RC_INPUT_PROTO`). `CONFIG_COMMON_RC=y` instead builds separate `crsf_rc`, `dsm_rc`, `ghst_rc` and `sbus_rc` drivers; individual `CONFIG_DRIVERS_RC_*_RC=y` lines build them one at a time. A protocol or port that needs a driver the board doesn't build (PPM, which needs `rc_input`, on a `CONFIG_COMMON_RC` board) is "not supported by the default firmware" (T-P11): a user can build it in. |
| RC protocols enabled by default | `init/rc.board_defaults`, driver `module.yaml` | `rc_input` runs on the port in `RC_PORT_CONFIG`, which defaults to the RC port (`src/drivers/rc_input/module.yaml`). The separate drivers run only on a port set in `RC_CRSF_PRT_CFG`, `RC_DSM_PRT_CFG`, `RC_GHST_PRT_CFG` or `RC_SBUS_PRT_CFG`; none has a default port, so a board enables one with `param set-default RC_<X>_PRT_CFG 300` in `rc.board_defaults` (`300` is the RC port, per `Tools/serial/generate_config.py`). With `CONFIG_COMMON_RC` and no such line, no FMU-side protocol is enabled by default. The PX4IO's protocols are always on. |
| FMU PWM output count | `src/board_config.h`, `src/timer_config.cpp` | The `initIOTimerChannel(...)` entries in `timer_config.cpp`, in order: the first is output 1. `DIRECT_PWM_OUTPUT_CHANNELS` counts these plus any capture channels, so it isn't the PWM output count when there are any. |
| Capture channels | `src/timer_config.cpp`, `src/board_config.h` | An `initIOTimerChannelCapture(...)` entry is a timer channel wired for capture (camera capture feedback, pulse measurement), usually on a pin named `FMU_CAP` in the `board_config.h` comments. It isn't an input-only pin as far as the firmware goes: `initIOTimerChannelCapture` is an alias of `initIOTimerChannel` (`platforms/nuttx/src/px4/stm/stm32_common/include/px4_arch/io_timer_hw_description.h`), it takes the next channel number after the PWM outputs, it's included in `DIRECT_PWM_OUTPUT_CHANNELS`, and actuator setup lists it as its own group, labelled _PWM Capture N_ (`Tools/module_config/output_groups_from_timer_config.py`). So count it separately: the page describes it as a capture channel, with its timer, rather than counting it as a PWM output or leaving it out. Because it's an ordinary timer channel, it can also be used as an extra PWM or OneShot output with any output function, and as DShot only if its timer has a DMA entry in `initIOTimer(...)`; the page says so (T-PWM1). Where the manufacturer's carrier or pinout routes it to a connector other than the PWM outputs (an `ADIO` or `CAP` port), the page says where. |
| IO (MAIN) output count | PX4IO present | 8. With a PX4IO the IO outputs are `MAIN` and the FMU outputs `AUX`; without one, the FMU outputs are the only outputs. Firmware built with `CONFIG_DRIVERS_PX4IO=y` labels the FMU outputs `AUX` in its parameters and actuator setup whether or not an IO is fitted: `CONFIG_BOARD_IO` defaults on with it (`Kconfig`), and `src/lib/parameters/CMakeLists.txt` then generates the parameters with `--board-with-io`. On a module whose PX4IO sits on the carrier board (a Pixhawk Autopilot Bus module such as ARKV6X), the IO outputs only exist on carriers that fit one. Check the manufacturer's carrier pages: ARK's own PAB carrier has no PX4IO, for example (`docs/en/flight_controller/ark_pab.md`). A variant built with `CONFIG_DRIVERS_PX4IO=n` labels the FMU outputs `MAIN` ("Variant builds"). |
| PWM timer groups | `src/timer_config.cpp` | Each `initIOTimerChannel(io_timers, {Timer::TimerN, Timer::ChannelM}, ...)` puts that output in timer N's group. Outputs sharing a timer must use the same protocol and rate. A capture channel's timer is listed in `io_timers[]` too, but it isn't a PWM output group. |
| DShot | `default.px4board`, `src/timer_config.cpp`, defconfig | `CONFIG_DRIVERS_DSHOT=y`, and a DMA entry on the timer (`initIOTimer(Timer::TimerN, DMA{DMA::IndexX})`); a timer without one can't do DShot. See "DShot by chip family" below. IO outputs never support DShot. |
| Bidirectional DShot | `src/timer_config.cpp`, defconfig | Needs DShot on the output and capture DMA on its timer channel; see "DShot by chip family". |
| Power inputs and monitoring | `src/board_config.h`, `init/rc.board_sensors`, `default.px4board` | `BOARD_NUMBER_BRICKS` (power inputs); `BOARD_HAS_NBAT_V` / `_I` (a `d` suffix means digital); the monitor drivers started in `rc.board_sensors` (`ina226`, `ina228`, `ina238`); `board_adc` for analog. When `rc.board_sensors` chooses between monitors by parameter (`SENS_EN_INA226`, ...), the one set with `param set-default` in `rc.board_defaults` is the default. Check the manufacturer's own power modules too (`docs/en/power_module/<vendor>_*.md`): one with a different monitor chip from the default needs its enabling parameters on the page (T-W6), and its driver built. |
| CAN buses | defconfig, `default.px4board` | `CONFIG_<CHIP>_FDCAN<n>=y` or `..._CAN<n>=y`; `CONFIG_DRIVERS_UAVCAN=y` |
| Ethernet | `default.px4board`, defconfig | `CONFIG_BOARD_ETHERNET=y`, `CONFIG_NET=y`. The speed isn't in board source; take it from the manufacturer. |
| SD card | defconfig, `src/board_config.h` | `CONFIG_MMCSD=y` means an SD or eMMC device. An eMMC reset or enable GPIO in `board_config.h` (`GPIO_EMMC_nRESET`) means soldered-down eMMC, not a removable slot; check the manufacturer before writing "MicroSD slot". |
| IMU heater | `default.px4board` | `CONFIG_DRIVERS_HEATER=y` |
| I2C buses, internal vs external | `src/i2c.cpp` | `initI2CBusExternal(n)` is on a connector; `initI2CBusInternal(n)` is on-board only |
| SPI buses | `src/spi.cpp` | One `initSPIBus(...)` per bus, with the devices on it. `initSPIBusExternal(...)` is an external bus; its `SPI::CS` and `SPI::DRDY` entries give the chip-select and data-ready counts. |
| Parameter storage | `src/mtd.cpp`, `src/spi.cpp` | The `px4_mtd_entry_t` with an `MTD_PARAMETERS` partition, and the device it's on (`SPIDEV_FLASH(n)` on an SPI bus, or an I2C EEPROM). The part is usually named in a comment beside it (`// FM25V02A ...`). No MTD parameters partition means parameters are stored in the processor's flash. |
| OSD | `default.px4board` | `CONFIG_DRIVERS_OSD*` |
| USB | defconfig | `CONFIG_USBDEV=y` |
| Board ID, flash size | `firmware.prototype` | `board_id`, `image_maxsize`; the page rarely states these, but when it does they must match |

## Processors

For T-S1 (`page-template.md`).
The page should give the part with its core, clock, flash and RAM; check them against this table, and check a model not listed here against its manufacturer datasheet.

| Model | Core | Clock | Flash | RAM |
| --- | --- | --- | --- | --- |
| STM32H743, STM32H753, STM32H747, STM32H757 | Arm Cortex-M7 | 480 MHz | 2 MB | 1 MB |
| STM32F765, STM32F767, STM32F777 | Arm Cortex-M7 | 216 MHz | 2 MB | 512 KB |
| STM32F427, STM32F437 | Arm Cortex-M4 | 168 MHz | 2 MB | 256 KB |
| STM32F405, STM32F407 | Arm Cortex-M4 | 168 MHz | 1 MB | 192 KB |
| MIMXRT1062 | Arm Cortex-M7 | 600 MHz | external | 1 MB |
| MIMXRT1176 | Arm Cortex-M7, plus a Cortex-M4 400 MHz secondary core | 1 GHz | external (64 MB on FMUv6X-RT) | 2 MB |
| STM32F100 (PX4IO) | Arm Cortex-M3 | 24 MHz | 64 KB | 8 KB |

## UART order

The order in which NuttX numbers enabled UARTs as `/dev/ttyS0`, `/dev/ttyS1`, ...:

| Chip family | Order |
| --- | --- |
| STM32H7, STM32F7 | USART1, USART2, USART3, UART4, UART5, USART6, UART7, UART8 |
| STM32F4 | USART1, USART2, USART3, UART4, UART5, USART6 |
| i.MX RT | LPUART1, LPUART2, ... LPUART11 |

Only enabled UARTs get a number: if USART2 isn't enabled, USART3 takes `ttyS1`.

## DShot by chip family

| Chip family | DShot | Bidirectional DShot |
| --- | --- | --- |
| STM32H7 | On any FMU output whose timer has a DMA entry | On DShot outputs whose timer channel has capture DMA: channels 1–4 of Timer1, 2, 3, 5 and 8; channels 1–3 of Timer4 (not CH4); channel 1 of Timer15, 16 and 17. Other DShot outputs can send bidirectional DShot but can't read eRPM telemetry back. |
| STM32F7, STM32F4 | Not supported by PX4, whatever `timer_config.cpp` says | Not supported |
| i.MX RT | On all FMU outputs | On all DShot outputs |

The capture map comes from `getTimerChannelDMAMap()` in `platforms/nuttx/src/px4/stm/<family>/include/px4_arch/hw_description.h`; if the page's claim disagrees with this table, check that source at the base SHA before reporting.

## Diffing against the reference design

When the board implements a reference design, compare its files with `boards/px4/<design>/` one file at a time, the reference at the base SHA and the new board at the head SHA:

```sh
diff <(git -C <clone> show <base-sha>:boards/px4/fmu-v6x/default.px4board) \
     <(git -C <clone> show <head-sha>:boards/<vendor>/<board>/default.px4board)
```

Do this at least for `default.px4board`, `nuttx-config/nsh/defconfig`, `src/board_config.h`, `src/timer_config.cpp` and `init/rc.board_sensors`.
Files that match the reference board describe identical behaviour, so the page should say the same as the reference design's pages about those areas.
Files that differ are the areas where the page has to describe *this* board rather than borrow text from a sibling, and they're where a copied paragraph goes wrong.
Record the differing areas in the worksheet's last row; `sibling-comparison.md` uses them.
