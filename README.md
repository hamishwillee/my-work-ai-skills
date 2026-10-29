# My work AI skills

Claude Code skills for my work, organized by domain.

## Structure

- `UAV/` — skills related to uncrewed aerial vehicles.
  - `PX4/` — skills for the PX4-Autopilot project.
  - `MAVLink/` — skills for the MAVLink protocol.

## Current skills

- [`UAV/PX4/px4-doc-review`](UAV/PX4/px4-doc-review) — editorial review of PX4-Autopilot documentation pull requests.
- [`UAV/PX4/px4-uorb-review`](UAV/PX4/px4-uorb-review) — editorial review of uORB message (.msg) documentation in PX4-Autopilot pull requests.
- [`UAV/PX4/px4-param-review`](UAV/PX4/px4-param-review) — review of PX4-Autopilot parameter descriptions (short/long descriptions and option labels) against the project's description standard, checking rewrites for lost facts.
- [`UAV/PX4/px4-board-doc-review`](UAV/PX4/px4-board-doc-review) — review of flight-controller board documentation in PX4-Autopilot pull requests, against board source, sibling pages, and the board support guide.
- [`UAV/PX4/px4-rangefinder-doc-review`](UAV/PX4/px4-rangefinder-doc-review) — review of rangefinder (distance sensor) documentation in PX4-Autopilot pull requests, against driver source, sibling pages, and a page template shared by single-model and family pages.
- [`UAV/PX4/px4-gnss-doc-review`](UAV/PX4/px4-gnss-doc-review) — review of GNSS (GPS, RTK and RTK heading) receiver documentation in PX4-Autopilot pull requests, against the GPS driver and protocol source, sibling pages, and a page template shared by UART, Septentrio and DroneCAN receivers.
- [`UAV/MAVLink/mavlink-command-review`](UAV/MAVLink/mavlink-command-review) — editorial review of mavlink-devguide pages documenting individual MAV_CMD commands or message fields.
- [`UAV/MAVLink/mavlink-xml-review`](UAV/MAVLink/mavlink-xml-review) — review of MAVLink XML message definition changes for wire compatibility, placement and lifecycle, definition quality, message design and downstream impact.
- [`UAV/MAVLink/mavlink-toolchain-review`](UAV/MAVLink/mavlink-toolchain-review) — execution-first review of mavlink/mavlink toolchain changes (check scripts, doc generator, workflows, build, pymavlink bumps), proving each fix against base and head.
