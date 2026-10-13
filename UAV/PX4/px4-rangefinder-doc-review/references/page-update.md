# Updating a page

How to bring an existing rangefinder page up to the template, one approved change at a time.
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
   Most of what an old page lacks (pinout, power, mounting, specifications) is there and nowhere else.

## One suggestion at a time

Work down the page in skeleton order (`page-template.md`), one section per suggestion, then the listings.
A usual run:

1. Version badge
2. Opening paragraph (always with the range; the span across models on a family page)
3. Hero image and any top-of-page notes
4. Specifications
5. Where to Buy
6. Sensor Configuration, if it applies
7. Hardware Setup: Mounting, Pinouts, Wiring
8. Firmware Support
9. PX4 Configuration
10. Testing
11. Troubleshooting and Developer Information, if the page has them
12. Further Information
13. `rangefinders.md` row and summary, then any other listing

Fold a trivial fix on an adjacent line (an image's alt text, a missing space in a container) into the suggestion next to it, and say so.

Each suggestion gives, in this order:

- **Where**: the section and line, and a count of where this sits in the run ("Suggestion 4").
- **Current** text, when something is being replaced or removed.
- **Proposed** text, in full, as it will appear in the file, using the template's standard wording wherever the template has it.
- **Evidence** for every fact in it: the driver file and line, or the manufacturer document and section.
  Follow `shared.md`, "Verification": a manufacturer figure read through `WebFetch` is fetched twice before it goes on the page.
- **Points to decide**: every judgement call in the proposal, each with the alternative.
  Typical ones: the manufacturer and the driver give different figures; a manufacturer label doesn't match a template label; a figure is your own conversion; something was dropped as marketing; a link has a revision number in it.

Then ask for approval and stop.
Apply the edit only after the reviewer answers, exactly as approved, and confirm it in one line before the next suggestion.

**If it can't be proven, it isn't asserted** (`shared.md`).
When the information for a section can't be found (no purchase link, no pinout in any manufacturer document), leave the section or the value out, and say what was searched.
A section built from guesses is worse than a missing one: this page is what someone wires a sensor from.
The reviewer can supply a fact from their own knowledge, and then it goes in on their say-so.
Add the gap to the questions for the manufacturer, unless the product is discontinued.

**Unproven claims already on the page** are proposed for removal in the suggestion for their section, each named as a point to decide, since the reviewer may know them to be true.

## Diagrams

When a wiring image is wrong, altered, or for another model, propose replacing it with a diagram drawn for this page rather than leaving the page with none.

- **Draw only what the approved text says.**
  The diagram is a picture of the wiring table: the same pins, the same connections, nothing extra.
  Draw it after the table for that section is approved, and say that it depicts wiring you haven't tested.
- **One diagram per connection**, placed in that connection's wiring sub-section above its table.
- **SVG**, in the page's assets folder, named `<product>_<connection>_wiring.svg`, with a `<title>` and `<desc>` that say in words what is connected to what.
  Use the same layout and style for every diagram on a page: sensor on the left with its pins numbered and named as in the pinout, the flight controller and any supply on the right, wires in the manufacturer's wire colours, unconnected pins shown as such, and a white background so it reads in both light and dark themes.
- **Put values on the diagram**, not "see text": a reader looking at a resistor wants its value there.
  Where the page gives alternatives, give both and let the text explain which is which.
- **Check it by rendering it.**
  Convert the SVG to a PNG (`cairosvg` in the scratch virtual environment, or `rsvg-convert`) and look at the result for overlapping labels and for lines that appear to join where they only cross.
- **Show it before it counts as approved**: open the rendered image for the reviewer, or give the preview URL.
- **Leave the old image files in place** unless the reviewer says to delete them: translated pages still reference them until the next translation sync.

## Previewing the page

Offer a live preview when the page has diagrams or large tables, or when the reviewer asks to see it.

- Start the docs site from the clone's `docs/` directory in the background: `node_modules/.bin/vitepress dev . --port <port> --host 127.0.0.1` (the `docs:dev` script in `docs/package.json`).
- Wait for the "Local:" line in its output and take the base path from it: the page is at `<that URL>en/sensor/<page>.html`, and an asset at `<that URL>assets/...`.
  Confirm the page returns 200 before giving the reviewer the link.
- If the clone has no `docs/node_modules`, say so and ask before installing; linking another clone's `node_modules` is quicker, and is never committed.
- The server reloads as edits are applied. Say that it stops when the session ends, and stop it yourself when the work is finished.

## What turns up along the way

Reading the manual and the driver closely surfaces things that aren't page edits.
Keep a running list and give it with the suggestion that turned it up, then again in full at the end:

- **Questions for the manufacturer** (never for a discontinued product; `shared.md`, "Discontinued products"): what no source settles (NDAA status, which interface variant a store unit ships as, whether a newer model or connection works with the driver).
- **Driver observations**: where the driver doesn't do what the manufacturer says an integrator must (`source-consistency.md`, "What the manufacturer requires").
  These are never page findings.
- **Contacts**: who could review the page or answer the questions (`shared.md`, "Finding who to ask").

Draft each as a review comment for the reviewer to post, addressed to a named handle and anchored to the specific line of the diff it's about (`SKILL.md`, Report, "Comment drafts").
Never post one yourself, and never name anyone in a commit message or PR description: whether to raise something, and with whom, is the reviewer's decision, and they may know that a contributor has left the project.
The PR description states what changed and nothing else.

## Finishing

1. **Format check.**
   Run the docs formatter over the edited files if the clone has it (`docs/node_modules/.bin/prettier --check <files>`), and fix what it reports.
2. **Say what wasn't done**: sections skipped, facts left unverified, checks not run (the link checker, a re-review).
3. **Offer** to re-run the review on the result, and to commit and open a pull request.
4. **Committing and the PR**, only when the reviewer asks.
   Stage only the files this run edited, never whatever else is dirty in the clone.
   Use the clone's own `commit` and `pr` skills when it has them (`.claude/skills/` in PX4-Autopilot); their rules on commit format, sign-off and AI disclosure are the project's and take precedence over any default.
   For PX4-Autopilot that means `docs(sensor): ...`, `git commit -s`, an `Assisted-by: <tool>:<model-id>` trailer, and no `Co-Authored-By` or "generated with" line.
   The sign-off certifies changes the reviewer has seen, which is another reason every edit is approved first.
5. **After the PR is open**, give the comment drafts again with the line each attaches to, for the reviewer to post.
