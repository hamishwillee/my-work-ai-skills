# Updating a page

How to bring an existing GNSS page up to the template, one approved change at a time.
Read by the main agent only, when the reviewer asks for a page to be updated, fixed or restructured rather than reviewed.

This is the one mode that edits files in the clone, and only the changes the reviewer approves.
Everything else in this skill stays read-only.

## Before the first suggestion

1. **Have a review to work from.**
   If the page hasn't just been reviewed in this conversation, run the review first (`SKILL.md`, Workflow) in the **existing page** form, and show its report.
   The findings are the work list.
2. **Check where the edits will land.**
   `git -C <clone> status --short` and `git -C <clone> branch --show-current`.
   Say which branch the edits go on, and stop to ask if the page already has uncommitted changes you didn't make.
3. **Have the manufacturer facts** (`shared.md`, "Manufacturer facts") filled in, from the product page and the current manual.
   Most of what an old page lacks (receiver, protocol, pinout, power, mounting, specifications) is there and nowhere else.

## One suggestion at a time

Work down the page in skeleton order (`page-template.md`), one section per suggestion, then the listings.
Fixes that are the same on two pages (an RTK and a non-RTK version, a family's model pages) are one suggestion covering both, when the reviewer is working on both.
A usual run:

1. Version badge
2. Opening paragraph (receiver or bands, capability, connection)
3. Hero image and any top-of-page notes
4. Specifications, including features PX4 doesn't use
5. Where to Buy
6. Receiver Configuration, if it applies
7. Hardware Setup: Mounting, Pinouts, Wiring
8. Firmware Support, if it applies
9. PX4 Configuration: protocol and port, secondary receiver, RTK, heading, DroneCAN
10. LED Meanings
11. Testing
12. Troubleshooting, if the page has it
13. Further Information
14. `SUMMARY.md`, the device-table row, the protocol sentences, then any other listing

Fold a trivial fix on an adjacent line (an image's alt text, a missing space) into the suggestion next to it, and say so.

Each suggestion gives, in this order:

- **Where**: the section and line, and a count of where this sits in the run ("Suggestion 4").
- **Current** text, when something is being replaced or removed.
- **Proposed** text, in full, as it will appear in the file, using the template's standard wording wherever the template has it.
- **Evidence** for every fact in it: the source file and line, or the manufacturer document and section.
  Follow `shared.md`, "Verification": a manufacturer figure read through `WebFetch` is fetched twice before it goes on the page.
- **Points to decide**: every judgement call in the proposal, each with the alternative.
  Typical ones: the manufacturer and the source give different figures; a vendor feature PX4 doesn't use (keep it marked, or drop it); a part number no document names; a vendor link to keep as "user manual" or drop.

Then ask for approval and stop.
Where `AskUserQuestion` is available, give the proposal as a preview and the alternatives as options, with the recommended one first.
Apply the edit only after the reviewer answers, exactly as approved, and confirm it in one line before the next suggestion.
If the reviewer changes the proposal in their answer ("append '(not supported on PX4)'"), check any fact their change asserts against the source before applying it, and say what you found.

**If it can't be proven, it isn't asserted** (`shared.md`).
When the information for a section can't be found (no purchase link, no pinout in any manufacturer document), leave the section or the value out, and say what was searched.
The reviewer can supply a fact from their own knowledge, and then it goes in on their say-so.
Add the gap to the questions for the manufacturer, unless the product is discontinued.

**Unproven claims already on the page** are proposed for removal in the suggestion for their section, each named as a point to decide, since the reviewer may know them to be true.
A reviewer can also choose to leave one for the author; record it as a question for the manufacturer.

**Images.**
Compress new or changed images with the project's own tool if the reviewer has one (ask, or use what their notes name), not an ad hoc converter.
When two pages use byte-identical image files, propose one shared file, check with `grep -rl <name> <clone>/docs --include=*.md` that only these pages use the old names, and remind the reviewer that the new file has to be added to git.

## Diagrams

When a pinout or wiring image is wrong, altered, or for another model, propose replacing it with a diagram drawn for this page rather than leaving the page with none.

- **Draw only what the approved text says.**
  The diagram is a picture of the pinout or wiring table: the same pins, the same connections, nothing extra.
  Draw it after the table for that section is approved, and say that it depicts wiring you haven't tested.
- **SVG**, in the page's assets folder, named `<product>_<connection>_wiring.svg`, with a `<title>` and `<desc>` that say in words what is connected to what, a white background so it reads in both light and dark themes.
- **Check it by rendering it** to PNG (`cairosvg` in a scratch virtual environment, or `rsvg-convert`) and looking at it.
- **Leave the old image files in place** unless the reviewer says to delete them: translated pages still reference them until the next translation sync.

## Previewing the page

Offer a live preview when the page has diagrams or large tables, or when the reviewer asks to see it.

- Start the docs site from the clone's `docs/` directory in the background: `node_modules/.bin/vitepress dev . --port <port> --host 127.0.0.1` (the `docs:dev` script in `docs/package.json`).
- Wait for the "Local:" line in its output and take the base path from it: the page is at `<that URL>en/gps_compass/<page>.html`.
  Confirm the page returns 200 before giving the reviewer the link.
- If the clone has no `docs/node_modules`, say so and ask before installing.
- Stop the server when the work is finished.

## What turns up along the way

Reading the manual and the source closely surfaces things that aren't page edits.
Keep a running list and give it with the suggestion that turned it up, then again in full at the end:

- **Questions for the manufacturer** (never for a discontinued product): what no source settles (receiver chip, compass and barometer parts, dimensions, default output).
- **Driver observations**: where the receiver outputs something the driver doesn't parse, or the manufacturer requires something the driver doesn't do.
  These are never page findings.
- **Shared pages left stale** by the change (a protocol list, the DroneCAN hardware list).
- **Contacts**: who could review the page or answer the questions (`shared.md`, "Finding who to ask").

Draft each question or observation as a review comment for the reviewer to post, addressed to a named handle and anchored to the specific line of the diff it's about (`SKILL.md`, Report, "Comment drafts").
Never post one yourself, and never name anyone in a commit message or PR description.

## Finishing

1. **Format check.**
   Run the docs formatter over the edited files (`docs/node_modules/.bin/prettier --check <files>`), and fix what it reports.
   A table whose widest cell changed is re-padded throughout; say so, since the diff then touches every row.
2. **Link check** over the edited files with the project's checker (`npx markdown_link_checker_sc -r .. -d docs -e en -i assets -u docs.px4.io -f <list.json>`, run from `docs/`).
3. **Say what wasn't done**: sections skipped, facts left unverified, files left untracked.
4. **Offer** to re-run the review on the result, and to commit and open a pull request.
5. **Committing and the PR**, only when the reviewer asks.
   Stage only the files this run edited or created, including new images, never whatever else is dirty in the clone.
   Use the clone's own `commit` and `pr` skills when it has them (`.claude/skills/` in PX4-Autopilot); their rules on commit format, sign-off and AI disclosure are the project's and take precedence over any default.
   For PX4-Autopilot that means `docs(gps): ...`, `git commit -s`, an `Assisted-by: <tool>:<model-id>` trailer, and no `Co-Authored-By` or "generated with" line.
6. **After the PR is open**, give the comment drafts again with the line each attaches to, for the reviewer to post.
