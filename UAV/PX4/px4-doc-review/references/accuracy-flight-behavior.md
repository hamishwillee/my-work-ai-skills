# Accuracy lens: flight behavior

Covers the **flight-behavior** category from the routing table in `shared.md`: flight modes (and their per-vehicle-type variants), features, configuration pages, actuators, tuning/advanced-config, and the flight-stack/concept pages that explain how PX4 flies.

These pages describe firmware *behaviour*: what a parameter does, what a mode does by default, what happens when.
The firmware source in the same repo is the ground truth — lean on sources-of-truth item 2 in `shared.md` (and item 1 whenever the PR itself touches source) more than any other category does.

## Parameter claims

- A parameter name mentioned in prose (not via the `{​{ param }}` include, which is metadata-generated and out of scope) checked against `PARAM_DEFINE_*` in `src/**` on the base branch: does it exist, is it spelled/cased correctly.
- A stated default value, unit, or range checked against the same `PARAM_DEFINE_*` call.
  A default that doesn't match source is `bug` — a reader will tune against a number that isn't real.
- A parameter described as affecting one vehicle type when its `PARAM_DEFINE_*` group or the module that reads it says otherwise.

## Mode and feature behaviour

- A claim about what a flight mode does by default, what triggers a mode switch, or what a failsafe does: checked against the code that implements it (the mode's class in `navigator` or `flight_mode_manager`, the failsafe logic in `commander`), read as Validating the docs against the code in `shared.md` describes, and against the module's `PRINT_MODULE_*` description text.
  A precise claim ("switches to Land after 3 failed GPS fixes") needs that code as its evidence.
  A general one ("stabilises the vehicle") can't be wrong in detail, so raise it only when the code shows a case it leaves out that changes what the reader should expect, such as a condition under which the mode behaves differently.
- The parameters a behaviour depends on: when the code reads a parameter that changes the described behaviour and the page doesn't mention it, that's `style`, or `bug` when the page's description is wrong for a non-default setting a reader is likely to use.
- A code/CLI snippet showing a command, flag, or config file syntax: checked that the command still exists and takes that syntax, the same way the developer lens checks code samples.

## Cross-vehicle-type consistency

This category has the heaviest sibling structure in the whole doc set: `flight_modes` / `flight_modes_fw` / `flight_modes_mc` / `flight_modes_rover` / `flight_modes_vtol`, and the equivalent `config_*` and `features_*` families.
When a PR changes one variant:

- Check whether the same claim exists, worded differently or identically, in the sibling pages for other vehicle types, and whether the change should logically apply there too.
  Don't demand the PR update every sibling — flag it as a note for the reviewer's judgement, not a `bug`, unless the unedited sibling now flatly contradicts the edited one.
- A behaviour genuinely specific to one vehicle type doesn't need to match its siblings; the concern is only an unexplained, likely-unintentional divergence.

## What this lens doesn't cover

Wiring, physical specs, and part identity belong to the hardware lens even when a flight-behavior page mentions a specific flight controller or sensor in passing.
Build tooling, module architecture, and non-flight developer APIs belong to the developer lens.
