# Lens: source consistency

Does the page say what the driver does?

Most of a rangefinder page restates settings that already exist in the driver: the parameter that enables it, the baud rate, the models it knows, the range it reports.
When the page and the driver disagree, the reader sets a parameter that doesn't exist, wires a sensor the driver can't talk to, or trusts a range PX4 won't use.
Work every checkable claim, not a sample.

Read `references/driver-sources.md` in full before starting: it says which file answers which question.

This lens owns the *correctness* half of every `page-template.md` check: where a check's severity says "`bug` if wrong", you decide whether it's wrong.
Whether the content is *present* and in the right form is `completeness.md`'s job.
Cite the check ID alongside the source evidence (`R-A1; module.yaml:5 name: SENS_PTGL100_CFG`).

## Method

1. **Start from the rangefinder facts worksheet** (`driver-sources.md`) the main agent filled in, and re-open a source file only to confirm a value you're about to cite or one the worksheet marks `unknown`.
   If you find a worksheet value wrong, report that and use the corrected value.
2. **List every checkable claim on the page** that falls in the lookup table: parameter names and values, defaults, baud rate, I2C address, models, range, field of view, orientation, update rate, Kconfig key, firmware availability, commands and options, topics and MAVLink messages.
   Include the page's `rangefinders.md` row and summary, and any other listing in scope.
3. **Check each claim** against the file the lookup table names, and record the file and line whatever the outcome.
4. **Check the other direction**: what the driver has that the page doesn't mention (a parameter, a model, a second connection, an orientation option).
5. **For a family page, do steps 2 to 4 once per model**, against the driver for the connection the page gives that model.

## Rules

### Enabling the sensor

- The enabling parameter the page names is the driver's (`SENS_<X>_CFG` from `serial_config`; `SENS_EN_<X>` from the parameter file), spelled exactly, and any value the page gives for it exists and means what the page says.
- A value given by label and number (`TELEM 2` (`102`)) has the right number for the label.
- The page's connection is one the driver has: a page offering I2C for a serial-only driver is `bug`.
- For DroneCAN, the `UAVCAN_RNG_MIN` and `UAVCAN_RNG_MAX` values are the sensor's range as the page and manufacturer give it, and the `UAVCAN_ENABLE` value is one that enables sensors.
- A page that says a reboot isn't needed for a parameter marked `reboot_required` is `bug`.

### Firmware support

Check the Firmware Support section, and anything the opening says about availability, against the worksheet's "In firmware" rows (`driver-sources.md`):

- Each key the page gives exists: the driver's own key is its `Kconfig` symbol with the `CONFIG_` prefix and `=y`, and the common-set key is given only when the `select` list has the driver (R-F4).
- "Most boards", "usually present in firmware", or no firmware note at all, needs the driver in the common set.
  If it isn't, that's `bug` (R-F5, R-O6): the parameter won't appear.
- A page saying the driver is *not* in most firmware when it is in the common set is `bug` too: it sends the reader off to build firmware they already have.
- Every board the page names as including the driver sets its own key, or sets the common-set key when the driver is in the set (R-F5).
  A board that sets the key and isn't named is `style`.
- The way to check and the way to add it are right: the file is `default.px4board`, and the menu path is **Drivers > Distance sensors** (R-F6, R-F7).
- What the page says about starting the driver matches the start line: enabled by parameter, or started by a named board (R-F8).
- For a page with several drivers, each connection is paired with the right driver and keys (R-F9).

### Serial settings

- A baud rate on the page is the driver's, for the model it's given for.
- "No need to set the baud rate" needs the driver to set the port's rate itself.
- When the driver expects a rate and never sends the sensor a command to change it, the page has to say the sensor must be at that rate, and how to check or set it (R-C1).
  Saying nothing is `bug` only when manufacturer material shows a different factory default; otherwise `style`.
- A claim that only RX is needed is `bug` when the driver writes to the sensor.

### I2C

- The address on the page is the driver's 7-bit address.
- A page that sends the reader to an internal bus is `bug` when the start line has `-X`.

### Models and range

- Every model the page lists for a connection has a value in that connection's model parameter, or is detected by the driver (R-M2); every parameter value the page quotes matches the model beside it (R-M4).
- The range on the page, in the Supported Models table, and in the `rangefinders.md` row matches `set_min_distance` and `set_max_distance` for that model.
- **When they differ**, look at manufacturer material before deciding:
  - the manufacturer agrees with the driver: the page is wrong, `bug`;
  - the manufacturer agrees with the page: the page is right about the sensor but the reader should know PX4 uses a narrower range, so it's `style` with both figures as the suggestion (R-S3), and the driver's limit goes below the tables as a firmware question;
  - nothing sources the page's figure: `bug`.
- A field of view, sensor type or update rate on the page matches the driver where the driver sets one.

### Orientation

- An orientation parameter the page names exists, and the default the page gives is its default.
- A page telling the reader to mount the sensor facing forward or upward needs the driver to take an orientation; if the direction is fixed (`driver-sources.md`, "Orientation"), that's `bug`.
- A page for a `distance_sensor` driver that offers it for Collision Prevention needs an orientation parameter; a page for an `obstacle_distance` driver that offers it for terrain following or landing is `bug` (R-O4).

### Other parameters

- Every parameter the page names exists in the driver's parameter files (or in `uavcan_params.yaml`, `params_range_finder.yaml`), with the values and default the page gives.
- A driver parameter the page never mentions is `style` (R-A3).

### Commands, topics and messages

- Every command and option the page shows is in the driver's usage block; `status` needs the driver to have one (R-T3).
- A device path in an example (`-d /dev/ttyS1`) is described as an example for a named board, not as the path.
- The uORB topic and MAVLink message the page names are the ones the driver publishes.
- The module reference link uses the driver's command name (`driver-sources.md`, "Module reference anchor").

### Developer Information

- A statement about the driver's behaviour (what it rejects, how it retries, which protocol version it speaks) is checked against the source like any other claim (R-D4).
  If you can't find it in the source, it goes below the tables as unverified, not as a finding.

### Physical specifications and wiring

Input voltage, current, dimensions, weight, pin order and connector type aren't in the driver.
Check them against the manufacturer facts (`shared.md`), and against the same figures elsewhere on the page.
A figure the manufacturer facts contradict is `bug`.
A figure they don't cover is not a finding; return it as an unproven claim for the notes below the tables, along with any other statement on the page that neither the driver nor the manufacturer facts back.
Where the facts are marked `not read`, every wiring claim on the page is unverified: say that once below the tables rather than once per claim.

### Wiring images

Check what each wiring, pinout or connector image shows (`shared.md`, "Wiring images") against the page's tables and text, against the other images on the page, and against the manufacturer facts, claim by claim: pin numbers, wire colours, component values, which pin goes to which port.
Report a disagreement on the line the image is referenced from.

### Variants and links

- When the manufacturer facts show the sensor ships as one interface variant or another, the page's setup is checked against the variant it claims to document, and a page that doesn't say which is reported under R-O9.
- The manual and datasheet the page links are compared with the current ones in the manufacturer facts (R-I2).
- A model in the same line that the page doesn't mention (a "Pro" or longer-range version) is not a finding: whether the driver supports it goes below the tables as a question for the manufacturer.

### What the manufacturer requires

Compare what the manufacturer tells an integrator they must do with what the driver does: reject readings below a signal-quality threshold, wait for a warm-up, ignore a blind zone, use a particular rate.

- Where the driver doesn't do it, that is a firmware question below the tables, never a finding on the page, with the manufacturer's sentence and the driver line that shows the gap.
  Name who last worked on that part of the driver, so the report can draft the comment.
- Where the driver's output frame handling differs from the manufacturer's frame format, the same.
- If the page promises behaviour that depends on it ("erroneous readings are filtered"), that claim is checked like any other and is `bug` when the driver doesn't.

## Severity

A claim the driver source contradicts is `bug`.
A model, parameter or connection the driver has that the page never mentions is `style`.
A claim you can't check against any source is not a finding.

## What this lens doesn't cover

Page form and shared wording (`sibling-comparison.md`), required content and listings (`completeness.md`), and prose (`px4-doc-review`).
