# px4-uorb-review

A Claude Code skill for editorial review of [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) uORB message (`.msg`) documentation in pull requests.

It checks every changed `msg/*.msg` / `msg/versioned/*.msg` file for:

- Compliance with the [uORB documentation standard](https://docs.px4.io/main/en/uorb/uorb_documentation), verified in part by actually running the project's own `Tools/msg/generate_msg_docs.py -e` against the PR
- Field and constant naming — but **only** for a field/constant this PR is already introducing, renaming, or retyping; an unchanged field's name is never flagged, since renaming one breaks every publisher, subscriber, and logged `.ulg` that references it
- Whether a new or changed field/constant has the comment it needs, and whether that comment says the right thing, judged against both the written standard and the recurring norms a PX4 maintainer ([@MaEtUgR](https://github.com/MaEtUgR)) has argued for across real PR review threads
- The message-level short description's length (a label, not a sentence — flagged with a shorter suggestion when it runs long) and unexpanded acronyms where spelling one out parenthetically stays within that length budget (`UWB sensor` → `Ultra-wideband (UWB) sensor`) — but not its general clarity beyond that, which is too subjective to check reliably
- The message-level long description's substance — whether it actually says who publishes and subscribes the message's topic(s) and how it fits the architecture, checked against what `grep`ing the firmware source for `ORB_ID(<topic>)` actually finds, with suggested text offered when it's missing or wrong
- Spelling and grammar — full rigour on the message-level short/long description, spelling-only-at-full-rigour and grammar-as-a-non-blocking-hint on terse inline field/constant comments, since those are meant to be fragments, not sentences

The skill does not edit files or post comments to GitHub, and never proposes a rename for a field this PR isn't already touching.
The output is a tabular report in chat, and it can write that report to a markdown file or open it in an editor if you ask.

Inspired by [mdn-pr-review](https://github.com/mdn/smithy/tree/main/skills/mdn-pr-review) and its sibling [px4-doc-review](https://github.com/hamishwillee/px4-doc-review), adapted for a structured, machine-parseable file format with its own validator rather than free-form prose.

## Contents

- [Skill structure](#skill-structure)
- [Why this differs from mdn-pr-review / px4-doc-review](#why-this-differs-from-mdn-pr-review--px4-doc-review)
- [Sources of truth](#sources-of-truth)
- [Installing](#installing)
- [Requirements](#requirements)
- [Using](#using)
- [Output](#output)

## Skill structure

```
px4-uorb-review/
├── SKILL.md                        # the main agent's instructions: scope, dispatch, report
├── references/
│   ├── shared.md                   # read by every lens: read-only rule, scope, new-or-changed gate, sources, severity
│   ├── style-guide.md              # the uORB documentation standard, extracted as checkable rules
│   ├── community-conventions.md    # @MaEtUgR's documented naming/comment norms, with links to the source comments
│   ├── tool-check.md               # runs generate_msg_docs.py -e and reports its output
│   ├── naming.md                   # lens: field/constant naming, gated to new/renamed/retyped only
│   ├── comments.md                 # lens: comment presence and quality, gated to new/changed comments
│   └── grammar-spelling.md         # lens: two-tier grammar/spelling (full vs. hint)
├── preferences.example.md          # boilerplate to copy to ~/.config/px4-uorb-review/preferences.md
└── README.md                       # this file
```

## Why this differs from mdn-pr-review / px4-doc-review

Both precedents review free-form prose against a style guide, entirely by reading.
A `.msg` file isn't prose — it's a structured format with its own parser, and PX4 ships that parser (`Tools/msg/generate_msg_docs.py`) in the same repo.
Re-deriving its rules (allowed units, `@enum` consistency, whitespace) by hand risks disagreeing with the actual tool CI runs, so `tool-check.md` runs it directly against a disposable worktree of the PR's head and reports its real output, rather than hand-coding a "structural" lens the way the two prose-review skills do.

The other real difference is that a field's name and type are part of a wire contract, not just a stylistic choice — a rename breaks every publisher, subscriber, and archived log that reference it.
So naming findings are gated: `shared.md` classifies every declaration as New / Renamed-or-retyped / Comment-only-edit / Untouched before any lens runs, and `naming.md` only ever fires on the first two.
Comment findings use the same classification, gated slightly wider (comment-only edits are still in scope, since editing a comment is exactly what makes a comment finding relevant).

Grammar/spelling also splits in two, per how the text is used: a message's short/long description is prose and gets full grammar+spelling review; an inline field/constant comment is meant to be terse, so it gets full spelling but only a non-blocking `hint` tier for grammar — a fragment missing an article isn't a defect in an eight-word comment.

## Sources of truth

Listed in order of precedence in `references/shared.md`:

1. `Tools/msg/generate_msg_docs.py -e`'s own output, run against the PR's head
2. The written uORB documentation standard (`references/style-guide.md`)
3. Actual publisher/subscriber usage in `src/**`, found by searching for `ORB_ID(<topic>)` — what a long description is checked against
4. Internal consistency within the same PR
5. Sibling messages elsewhere in `msg/`
6. `references/community-conventions.md` (@MaEtUgR's documented norms), applied at `style`/`minor` only, never above the written standard
7. This skill, last on purpose

## Installing

Clone this repo, then symlink it into Claude Code's skills directory:

```bash
git clone https://github.com/hamishwillee/px4-uorb-review.git ~/github/hamishwillee/px4-uorb-review
ln -s ~/github/hamishwillee/px4-uorb-review ~/.claude/skills/px4-uorb-review
```

Install at user level (`~/.claude/skills/`) rather than per-project, otherwise the skill only fires when you're working inside this repo itself.

### Reviewer preferences, optional

```bash
mkdir -p ~/.config/px4-uorb-review
cp ~/.claude/skills/px4-uorb-review/preferences.example.md ~/.config/px4-uorb-review/preferences.md
```

## Requirements

- **`gh` CLI**, authenticated: the skill reads the PR, its diff, and any linked issue through it.
- **A local clone of `PX4-Autopilot`**, required for `tool-check.md` (it needs to run the repo's own script) and strongly recommended for the other lenses (reading sibling messages for precedent is far cheaper against a local clone than the API).
  The skill checks common locations (`~/github/PX4/PX4-Autopilot` and siblings). Without one, `tool-check.md`'s findings are skipped and the report says so.
- **`python3`**, to run the generator script.

## Using

```
/px4-uorb-review 25990
```

A bare number is taken as a `PX4/PX4-Autopilot` PR.
The skill also triggers with natural language, such as "review this uORB PR" or a pasted PR URL.

**No PR to hand?** Ask it to review anyway, or just say "review the current branch" / "review this locally."
It offers a selection list: **Enter PR**, **Local branch**, or **A particular message**.

Pick local branch, and it diffs your working tree (uncommitted edits included) against the default branch, works out which uORB **topics** changed, and offers another selection list — one entry per changed topic, plus one to review all of them together. If nothing changed, it just says so.

Already know which topic you want? Pick "a particular message" instead and name it directly — it skips straight to that topic (implicitly against the local branch, no separate "local vs PR" question), checks just that one file for a diff, and reviews it if it's changed. If it isn't, it audits that one message in full rather than a diff — naming findings in that mode are advisory-only (`minor`), since there's no PR here to justify a rename's compat break.

For any of these local runs, once the report's done it checks whether `code` (VS Code) is on your `PATH` and, if so, offers to open the report there. Skipped entirely for a PR review, where the report's destination is GitHub, not an editor.

## Output

The report has four sections:

1. **PR triage summary.** Bug count and location, whether a linked issue is solved, findings by area (`Generated-doc validity` / `Naming` / `Comments` / `Grammar & spelling`), and every bug-severity finding with its line.
2. **Issue summary per file.** Counts per file, ordered by bug count.
3. **Detailed per-file review of changed lines.** A row per issue with line, severity, and suggested fix.
4. **Hints**, when there are any — non-blocking grammar-only suggestions on terse inline comments. Never counted in the triage totals.

| Severity | Meaning |
| --- | --- |
| `bug` | Violates the written standard or fails the project's own generator |
| `style` | Violates a named convention but the meaning survives |
| `minor` | No rule violated; a preference the author can decline |
| `hint` | Grammar-only observation on a terse inline comment; never a blocker |
