# PX4 parameter description standard

The checkable rules a parameter description is reviewed against.
Each rule has an ID (`S1`, `L4`, ...) for findings to cite.

## Where this comes from

- The six-point spec in the description of [PX4-Autopilot#27758](https://github.com/PX4/PX4-Autopilot/pull/27758), the tracking PR for trimming parameter descriptions.
  This is the published standard, and the rules below restate it.
- Maintainer review of that PR and of [#28850](https://github.com/PX4/PX4-Autopilot/pull/28850), its first split-off batch.
  Rules drawn from review rather than from the spec say so and link the comment.
- `validation/module_schema.yaml` (the YAML schema) and `src/lib/parameters/px4params/markdownout.py` (the parameter reference generator), for what the tooling enforces and how text renders.

If the #27758 description has changed since this file was written, the PR wins: re-read it and report the difference.

## Where the text is shown, and why length matters

A parameter's `short`, `long`, and option labels (`values:` for an enum, `bit:` for a bitmask) end up in three places:

- **The ground station.** QGroundControl shows `short` as the parameter's title, `long` below it, and each option label in the value dropdown.
  Newlines in `long` reach QGC unchanged.
- **The docs [parameter reference](https://docs.px4.io/main/en/advanced_config/parameter_reference).** The generator writes `short` (adding a full stop if it doesn't end with one), then `long`, then the option list, as markdown.
  A single newline in markdown is a space, so a multi-line `long` is joined into one paragraph there.
- **Flash.** `parameters.json.xz` is compiled into ROMFS on every board without `CONFIG_BOARD_CONSTRAINED_FLASH`, where it costs flash on boards that are short of it.
  xz compresses repetition, so wording already used elsewhere in the metadata costs almost nothing, and new wording costs full price.

The metadata is also translated on Crowdin ([PX4 Metadata](https://docs.px4.io/main/en/advanced/px4_metadata)), so every changed string discards its existing translations.
That's why a correct string is left alone rather than reworded for taste.

## Short description (`short`)

- **S1.** One line, at most 70 characters.
  The schema enforces this, so a violation fails `Tools/validate_yaml.py`.
- **S2.** Terse and clear: says what the parameter is or controls, as a phrase rather than a sentence.
  No "This parameter...", and no restated type such as "(integer bitmask)" or "(enum)", which the metadata already carries.
- **S3.** Change `short` only when it's wrong, unclear, or repeats the type (spec rule 1).
  A correct `short` reworded for taste is churn: it costs review time and discards translations.
- **S4.** When one qualifier in `short` would make `long` unnecessary, put it there and delete `long`.
  Review: "Module spin direction" → "Module spin direction and mode", "[then maybe you can drop long](https://github.com/PX4/PX4-Autopilot/pull/27758#discussion_r3511155276)"; "Max velocity in Velocity mode" → "Max velocity at full throttle when VTQ_CONTROL_MODE is Velocity", "[and maybe then remove long](https://github.com/PX4/PX4-Autopilot/pull/27758#discussion_r3511136247)".
- **S5.** A dependency on another parameter names that parameter in full, and a mode names its controlling parameter and value, as "when VTQ_CONTROL_MODE is Velocity" rather than "in Velocity mode".
  [Review](https://github.com/PX4/PX4-Autopilot/pull/27758#discussion_r3511146626): "drawing a line to other params to work out what mode you're in is hard - linking via param name helps."
  A partial or informal name is a wrong name: [review](https://github.com/PX4/PX4-Autopilot/pull/27758#discussion_r3511073930) corrected `DISARM_TRIGGER` to `VTQ_DISARM_TRIG`.
- **S6.** No abbreviation the reader can't expand from context.
  [Review](https://github.com/PX4/PX4-Autopilot/pull/27758#discussion_r3510988641): "Number of IFCI CVs in use" → "Number of IFCI control variables in use", because "CVs" "can't be inferred".

## Long description (`long`)

- **L1.** `long` holds only what `short`, `unit`, `min`/`max`, `default`, `increment`, `decimal`, `reboot_required` and the option labels don't already say.
  Delete it if nothing is left (spec rule 1).
- **L2.** Never restate `short`, in the same words or others.
- **L3.** Never re-list the options, numbered or not (spec rule 2).
  Per-option detail goes where O1 and O2 below put it.
  "By default, ..." is a restatement when the default is in `default:` or a label already says "(default)".
- **L4.** Keep every fact that affects configuration (spec rule 3):
  - behaviour: what the value does, and what special values do ("Set to 0 to disable.", "Negative values are ignored")
  - conditions: when it applies ("Only applies to SD card logging", "at log start (not boot)")
  - dependencies: other parameters it needs or interacts with, by name
  - limits: ranges, ordering constraints ("must be higher than the critical threshold"), or anything `min`/`max` don't express
  - warnings and safety notes, which keep their `WARNING:` lead
  - the unit, when there is no `unit:` field
  - physics or rationale only where it changes the value a reader picks: "roughly proportional to blade area seen side-on; much higher for ducted rotors" stays, the momentum-transfer mechanism behind it goes
- **L5.** Cut everything else (spec rule 3): restatements, "This parameter...", "Note that...", "It is recommended...", "allows you to...", examples that repeat the rule, and physics or rationale that doesn't change the value you pick.
  An example that shows something the rule doesn't (a non-obvious special case) is a fact, and stays.
- **L6.** Use the stock phrases (spec rule 4): "Set to 0 to disable.", "Set to -1 to disable.", "Only used when X is enabled." and "e.g.", and refer to parameters by name.
  Where sibling parameters say the same thing (`EKF2_BCOEF_X` and `EKF2_BCOEF_Y`), they say it in the same words, since the repeat compresses to almost nothing.
- **L7.** A unit belongs in `unit:` when the schema allows it (`validation/module_schema.yaml` lists the allowed units).
  Prose units are for a parameter with no allowed unit, or none set.
  A well-understood short form is fine in prose: [review](https://github.com/PX4/PX4-Autopilot/pull/28850#discussion_r4127637802) changed "amperes" to "amps", "Accept well understood shortenings of units".
- **L8.** A rewrite that compresses two conditions into one must stay true to the code.
  `BAT${i}_I_OVERWRITE` merged "Negative values are ignored" and "0 disables the overwrite" into "Set to 0 or less to disable.", which is right because `battery.cpp` applies it only when `_params.i_overwrite > FLT_EPSILON`.
- **L9.** When option labels use an abbreviation or a coined term, `long` explains it once: "MAVL 1 is the lower MAVLink instance." (`COM_RC_IN_MODE`), "Automatic Config adds dynamic node ID allocation and firmware update." (`UAVCAN_ENABLE`).

## Option labels (`values:` and `bit:`)

- **O1.** A few words of per-option detail go in the option's label, in parentheses (spec rule 2): "RC only (requires RC calibration)", "Debug (debug_*.msg topics)".
  Detail moved into a label is still a claim about the code, so it's checked like any other (L4).
- **O2.** More detail than fits in a label goes in `long`, as one `Label: effect.` line per option, where `Label` is the option's label text exactly as `values:` or `bit:` has it (spec rule 2).
  `MPC_THR_CURVE` writes "Rescale to estimate: ..." because its label is "Rescale to estimate", not the older prose name "Rescale to hover thrust estimate".
- **O3.** A label addition still reads on its own.
  [Review](https://github.com/PX4/PX4-Autopilot/pull/27758#discussion_r3511107106): `VTQ_CONTROL_MODE` compressed three sentences per mode into "Voltage (constant; set VTQ_MAX_VOLTS)" and "Velocity (closed-loop; set VTQ_MAX_VELOCITY; know propeller)", and that "feels like data loss. It wasn't very clear before and it is less so now."
  When the detail won't survive being cut to a few words, use O2 instead.
- **O4.** A label keeps its option's meaning and its key: never renumber or drop an option while rewording.
  Labels are shown in a dropdown, so keep a parenthetical to about six words.

## Wording and YAML form

- **W1.** Plain words in `long` (spec rule 5); `short` and labels may be phrases.
  `long` may open with a noun phrase naming what the parameter models, as "Bluff body drag along the forward/reverse axis, which scales with speed squared.", since that is the terse form the spec asks for.
  A fragment is a problem only when it's ambiguous: when the reader can't tell what a clause attaches to, what "it" refers to, or whether a name is a parameter.
  No invented abbreviations, and no symbols used as words: `v²`, `<=`, `->`, `&`, or "/" meaning "or".
  Established acronyms (RC, ESC, IMU, EKF2, GCS, SITL, SD) and units written as units (`m/s`) are fine.
- **W2.** Prose is one paragraph in a plain or quoted YAML scalar (spec rule 6).
  A plain or quoted scalar may wrap across several source lines, because YAML folds those into one line.
  A `|` literal block keeps every newline, so a `|` block wrapped mid-sentence shows broken lines in QGC.
  Newlines belong only between per-option lines (O2), in a `|-` block.
- **W3.** Each per-option line in a `|-` block is a sentence ending in a full stop, because the docs page joins the lines into one paragraph and only the full stops keep the options apart there.
- **W4.** A scalar containing `: ` (such as `WARNING: ...`) is quoted, or YAML reads it as a mapping.
- **W5.** Multi-instance descriptions keep their `${i}` placeholders.
- **W6.** Spelling follows the [PX4 docs style guide](https://docs.px4.io/main/en/contribute/docs#style-guide): British English, except industry-standard software terms and names.
  Much existing parameter text is American; only flag spelling in text this PR wrote.
