# mavlink-command-review

A Claude Code skill for editorial review of [mavlink-devguide](https://github.com/mavlink/mavlink-devguide) pages that document individual `MAV_CMD` commands or message fields — pages shaped like [`en/services/mission_item_detail.md`](https://github.com/mavlink/mavlink-devguide/blob/master/en/services/mission_item_detail.md): one section per command, a Params table, sometimes an Autopilot Support subsection.

It exists because of [mavlink-devguide#761](https://github.com/mavlink/mavlink-devguide/pull/761), where a commit labelled as a pure file reorganization also quietly changed what the text meant — a behavioural claim added with no source, a params table's stated scope silently widened, and a wrong claim deleted without comment. A reviewer only caught it by manually diffing the old and new files by hand. This skill automates that diff and adds the checks that would have caught the rest.

It checks every changed in-scope file for:

- **Accuracy.** Anything the MAVLink XML itself defines (a param's number, name, description, units, range) checked against the matching entry in `en/messages/*.md`, which mirrors the XML directly. Anything more specific — what a particular autopilot (ArduPilot, PX4) actually does — requires a citable source (a file/line in that project's own repo, a linked test, or a linked issue/PR discussion); uncited implementation claims are flagged, not silently accepted or silently deleted.
- **Change discipline.** Whether a wording change is hiding inside a commit or PR labelled as a pure move/reorg, and whether a new claim was bundled in with nothing distinguishing it from the surrounding mechanical change.
- **Style & terseness.** Match to the page's own existing terseness and to this repo's `CLAUDE.md` conventions (callout syntax, relative links, etc.), and that a new page's `SUMMARY.md` entry exists.

A specific, hard rule throughout: this skill never lets generated prose silently override the XML. If a doc claim and the XML disagree, the finding names both and states that resolving it means either fixing the prose to match the XML, or — if the XML is what's actually wrong — opening a fix against `mavlink/mavlink` itself. It never just picks a side.

The skill does not edit files or post comments to GitHub. It also runs a lightweight self-check mode while *drafting* a page (see "Using" below) — no PR needed for that.

Out of scope, deliberately: `en/messages/*.md` itself (generated, never hand-edited — touching it is a finding, not content to review) and protocol-level `en/services/*.md` prose that isn't about one command's own parameters (`mission.md`'s own body, `camera.md`, `ftp.md`, ...). A sibling skill for that content is planned but not yet written.

## Contents

- [Skill structure](#skill-structure)
- [Sources of truth](#sources-of-truth)
- [Installing](#installing)
- [Requirements](#requirements)
- [Using](#using)
- [Output](#output)

## Skill structure

```
mavlink-command-review/
├── SKILL.md                        # orchestration: Scope → Dispatch → Report, plus Authoring mode
├── references/
│   ├── shared.md                   # read-only rule, scope, sources of truth, XML-conflict handling, severity
│   ├── accuracy.md                 # lens: XML-checked vs. citation-needed claims
│   ├── change-discipline.md        # lens: wording changes hidden inside a labelled "pure move"
│   └── style-terseness.md          # lens: terseness and this repo's own CLAUDE.md conventions
├── preferences.example.md          # boilerplate to copy to ~/.config/mavlink-command-review/preferences.md
└── README.md                       # this file
```

## Sources of truth

Listed in precedence order in `references/shared.md`:

1. The matching entry in `en/messages/<dialect>.md` (mirrors the MAVLink XML)
2. The PR's own diff, if it changes anything else alongside the doc
3. A citable ArduPilot/PX4 source, test, or linked issue/PR discussion, for implementation-specific claims
4. Sibling sections on the same or a linked page
5. This repo's own `CLAUDE.md`
6. Past review comments on the same PR or a linked issue
7. This skill, last on purpose

## Installing

Clone this repo, then symlink the skill into Claude Code's skills directory:

```bash
git clone https://github.com/hamishwillee/my-work-ai-skills.git ~/github/hamishwillee/my-work-ai-skills
ln -s ~/github/hamishwillee/my-work-ai-skills/UAV/MAVLink/mavlink-command-review ~/.claude/skills/mavlink-command-review
```

Install at user level (`~/.claude/skills/`) rather than per-project, so it also fires in Authoring mode wherever you happen to be editing mavlink-devguide, not only when that repo is the current directory.

### Reviewer preferences, optional

```bash
mkdir -p ~/.config/mavlink-command-review
cp ~/.claude/skills/mavlink-command-review/preferences.example.md ~/.config/mavlink-command-review/preferences.md
```

## Requirements

- **`gh` CLI**, authenticated: the skill reads the PR, its diff, and any linked issue through it, in review mode.
- A local clone of `mavlink-devguide` (for cheap access to `en/messages/*.md` and `CLAUDE.md`) and, optionally, of `ArduPilot` and/or `PX4-Autopilot` (to check implementation-specific claims). Without these the skill falls back to the GitHub API, slower but functional.

## Using

```
/mavlink-command-review 761
```

A bare number is taken as a `mavlink/mavlink-devguide` PR. The skill also triggers with natural language ("review this mavlink-devguide PR") or a pasted PR URL.

**Authoring mode.** No PR needed — while you're drafting or editing a page in scope, the skill applies the same three lenses to your own draft before you finish, calling out any unevidenced claim or XML disagreement rather than smoothing over it.

## Output

The report has three sections:

1. **PR triage summary.** Bug count and location, whether a linked issue is solved, findings by area (XML/evidence accuracy / Change discipline / Style & terseness).
2. **Issue summary per file.** Counts per file, ordered by bug count.
3. **Detailed per-file review of changed lines.** A row per issue with line, severity, and suggested fix.

| Severity | Meaning |
| --- | --- |
| `bug` | A reader ends up misinformed, or the doc contradicts the XML or a cited source |
| `style` | An implementation-specific claim with no citation; a wording change bundled into a labelled "pure move"; terseness/house-style drift |
| `minor` | No rule violated; a preference the author can decline |
