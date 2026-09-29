# Worked examples

How [PX4-Autopilot#28850](https://github.com/PX4/PX4-Autopilot/pull/28850) rewrote 14 parameter descriptions to the standard, and what that shows a reviewer to look for.
It was merged after review, cut the description text by 54% (9705 → 4441 characters), and passed `Tools/validate_yaml.py`, so it's the calibration point for what a good rewrite looks like.
Rule IDs refer to `description-standard.md`.

## How the PR approached it

- **Only descriptions and labels changed.** No default, range, type or key moved, so the review is purely about text.
  A rewrite PR that also changes metadata needs that change checked separately.
- **`short` left alone unless it repeated the type.** Only `SDLOG_PROFILE` changed its `short`, dropping "(integer bitmask)" (S2, S3).
  `BAT${i}_SOURCE` kept its trailing full stop and `SDLOG_MODE` its title case, since neither is wrong.
- **Option lists deleted from `long`, detail moved into labels.** `UAVCAN_ENABLE`, `COM_RC_IN_MODE` and `SDLOG_PROFILE` each re-listed every option in `long` (L3).
  The detail that wasn't already in a label went into it, in parentheses (O1):

  | Parameter | Label before | Label after |
  | --- | --- | --- |
  | `COM_RC_IN_MODE` | RC only | RC only (requires RC calibration) |
  | `COM_RC_IN_MODE` | RC or MAVLink keep first | RC or MAVLink keep first until reboot |
  | `SDLOG_PROFILE` | Estimator replay (EKF2) | Estimator replay (EKF2, full rate) |
  | `SDLOG_PROFILE` | Debug | Debug (debug_*.msg topics) |

- **Longer option detail became `Label: effect.` lines** using the exact label text (O2, W3), in a `|-` block (W2):

  ```yaml
  long: |-
    Rescale to estimate: stick is rescaled linearly so center stick gives the hover thrust estimate.
    No rescale: stick maps 1:1 to thrust; useful with very low hover thrust, where rescaling distorts the curve and makes the upper half sensitive.
    Rescale to parameter: as Rescale to estimate, but uses MPC_THR_HOVER; with MPC_THR_HOVER 0.5 same as No rescale.
  ```

- **What was left of `long` explains the labels' vocabulary**, rather than the options one by one (L9).
  `UAVCAN_ENABLE` went from a four-line option list to "Automatic Config adds dynamic node ID allocation and firmware update."
- **Stock phrases replaced bespoke ones** (L6): "Set this parameter to zero to turn off the bluff body drag model for this axis" → "Set to 0 to disable for this axis."; "when enabled by the EKF2_DRAG_CTRL parameter" → "Only used when EKF2_DRAG_CTRL is enabled."
  `EKF2_BCOEF_X` and `EKF2_BCOEF_Y` share every sentence but the axis name.
- **Warnings kept, just tightened** (L4): `EKF2_RNG_CTRL` still opens with `WARNING:` and keeps the advice to use `MPC_ALT_MODE` instead, the conditional-mode thresholds, and the vertical-takeoff constraint.
- **Physics kept only where it guides the value** (L4, L5): `EKF2_MCOEF` kept "scales with speed, not speed squared", "roughly proportional to blade area seen side-on" and "much higher for ducted rotors", and dropped the momentum-transfer mechanism.
- **Examples that repeat the rule dropped** (L5): `SDLOG_ROTATE`'s "a value of 90 means at least 10% of disk is always kept free" is just the definition of a percentage limit; `SDLOG_MISSION`'s "choose geotagging mode to only log data required for geotagging" restates its option label.
- **Restated defaults dropped** (L3): `SDLOG_MODE`'s "By default, logging is started when arming the system" was already the label "when armed until disarm (default)".
- **Two conditions merged into one, true to code** (L8): `BAT${i}_I_OVERWRITE`'s "Negative values are ignored" and "The default value of 0 disables the overwrite" became "Set to 0 or less to disable.", which matches `battery.cpp` applying it only when `i_overwrite > FLT_EPSILON`.

## Before and after

`BAT${i}_SOURCE`, 858 → 332 characters: every option's meaning survives, the boilerplate and the option-by-option "If the value is set to..." framing don't.

```yaml
# before
long: |
    This parameter controls the source of battery data. The value 'Power Module / Analog'
    means that measurements are expected to come from either analog (ADC) inputs
    or an I2C power monitor (e.g. INA226). Analog inputs are voltage and current
    measurements read from the board's ADC channels, typically from an onboard
    voltage divider and current shunt, or an external analog power module.
    I2C power monitors are digital sensors on the I2C bus.
    If the value is set to 'External' then the system expects to receive MAVLink
    or CAN battery status messages, or the battery data is published by an external driver.
    If the value is set to 'ESCs', the battery information are taken from the esc_status message.
    This requires the ESC to provide both voltage as well as current (via ESC telemetry).
# after
long: |-
    Power Module / Analog: board ADC inputs (onboard or external analog power module) or an I2C power monitor (e.g. INA226).
    External: MAVLink or CAN battery status messages, or an external driver.
    ESCs: esc_status from ESC telemetry; requires voltage and current.
```

The "before" also shows the W2 problem the standard exists to fix: a `|` block wrapped mid-sentence, which QGC displays with a line break after "'Power Module / Analog'".

`SDLOG_MODE`, 432 → 228 characters: one sentence survives, because it's the only one that says something the labels don't.

```yaml
# before
long: 'Determines when to start and stop logging. By default, logging is started
  when arming the system, and stopped when disarming. Note: The logging start/end
  points that can be configured here only apply to SD logging. The mavlink
  backend is started/stopped independently of these points.'
# after
long: Only applies to SD card logging; MAVLink logging starts and stops independently.
```

## What review changed, and what it could still have caught

- Review changed "amperes" to "amps" in `BAT${i}_I_OVERWRITE` ([comment](https://github.com/PX4/PX4-Autopilot/pull/28850#discussion_r4127637802)), establishing that a well-understood unit short form is fine (L7).
- That same parameter states its unit in prose ("this value in amps") with no `unit:` field, although the schema allows `A`.
  Under L7 that's a `minor` suggestion to add `unit: A` and drop "in amps".
- The PR moved the old `long`'s bit descriptions for `SDLOG_PROFILE` into the labels, including "Thermal calibration (high-rate raw IMU and baro)" and "Sensor comparison (low-rate raw IMU, baro and mag)".
  Both are wrong: `logged_topics.cpp` logs the same four topics (accel, baro, gyro and mag) at the same 100 ms interval for both bits.
  The error predates the PR, but moving a claim into a label gives it more prominence, so a moved claim is checked against the code like new text (L4, O1).
  Found by this skill's first run on the PR.
- `UAVCAN_ENABLE`'s old text said mode 3 "also sets the motor control outputs to UAVCAN"; the new text relies on the label "Sensors and Actuators (ESCs) Automatic Config" to carry that.
  That's the kind of borderline drop the facts lens should list as dropped-by-design rather than flag, since the label does say it.

## Lessons from the tracking PR's review

[#27758](https://github.com/PX4/PX4-Autopilot/pull/27758) is the full rewrite that #28850 was split from, and its review found the ways a trim goes too far.
Each became a rule in `description-standard.md`:

- Compressing option detail into cryptic label fragments ("know propeller", "constant") loses the meaning (O3).
- Referring to a mode without naming the parameter that selects it makes the reader hunt for it (S5).
- Informal or truncated parameter names in text are wrong names (S5).
- Unexpandable abbreviations ("CVs") trade clarity for a few bytes (S6).
- A qualifier moved into `short` can make `long` unnecessary (S4).

The same review also recorded the trade-off behind the whole exercise: most of the time `short` is enough, and the full text is always in the docs parameter reference, but a trim that "throws away some information" isn't acceptable just to save flash.
The reviewer's summary on #28850: "There is certainly no need for all that verbage and the duplicated text for values. I imagine the tough bit is not stripping that down too much."
