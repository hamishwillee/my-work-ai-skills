# px4-param-review

A Claude Code skill for reviewing parameter descriptions in [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot) pull requests: the `short` and `long` description and the enum/bitmask option labels of every parameter a PR adds or changes.

Parameter descriptions are compiled, xz-compressed, into flash on most boards, and shown in QGroundControl and the docs [parameter reference](https://docs.px4.io/main/en/advanced_config/parameter_reference).
[PX4-Autopilot#27758](https://github.com/PX4/PX4-Autopilot/pull/27758) set out a standard for trimming them, and [#28850](https://github.com/PX4/PX4-Autopilot/pull/28850) was its first reviewed batch.
This skill reviews against that standard:

- **Facts**: nothing that affects how the parameter is configured is lost in a rewrite, and what's kept is still true to the code that reads the parameter.
  Every rewritten parameter gets a fact-by-fact comparison of old and new, and the report lists what was dropped and why that was allowed, so you can judge the trim without re-reading every old description.
- **Concision**: `short` is terse and only changed when it was wrong; `long` holds only what `short`, the metadata and the option labels don't already say; option lists aren't repeated in `long`; per-option detail sits in the label or a `Label: effect.` line; stock phrases ("Set to 0 to disable.") are used so the text compresses well.
- **Wording**: grammar and clarity, no invented abbreviations or symbols as words, and YAML that renders correctly in both QGC and the docs.
- **Schema validity and size**: the PR's own `Tools/validate_yaml.py` run against its head, and the description size before and after.

The skill does not edit files or post comments to GitHub.
The output is a tabular report in chat, and it can write that report to a markdown file if you ask.

`px4-doc-review` hands any parameter definition changes in a docs PR to this skill.

## Skill structure

```
px4-param-review/
├── SKILL.md                       # the main agent's instructions: scope, tool check, dispatch, report
├── scripts/
│   └── param_desc_check.py        # classifies changed parameters, flags mechanical rule breaks, counts size, runs the validator
├── references/
│   ├── shared.md                  # read by every lens: read-only rule, scope, classification, sources, severity
│   ├── description-standard.md    # the standard as checkable rules (S/L/O/W IDs), with where each came from
│   ├── examples.md                # how #28850 applied it, before-and-after, and lessons from #27758's review
│   ├── tool-check.md              # running the script and using its output
│   ├── facts.md                   # lens: fact ledger, old vs new, checked against the code
│   ├── concision.md               # lens: placement and redundancy rules
│   └── wording.md                 # lens: grammar, clarity, YAML form and rendering
├── preferences.example.md         # boilerplate to copy to ~/.config/px4-param-review/preferences.md
└── README.md                      # this file
```

## Installing

Symlink the skill into Claude Code's skills directory:

```bash
ln -s ~/github/hamishwillee/my-work-ai-skills/UAV/PX4/px4-param-review ~/.claude/skills/px4-param-review
```

Optionally copy the preferences file:

```bash
mkdir -p ~/.config/px4-param-review
cp ~/.claude/skills/px4-param-review/preferences.example.md ~/.config/px4-param-review/preferences.md
```

## Requirements

- **`gh` CLI**, authenticated, for PR reviews.
- **A local clone of `PX4-Autopilot`**, for the script and for reading the code that uses each parameter.
  The skill fetches the PR's commits into it from whichever remote points at `PX4/PX4-Autopilot` (often `upstream` in a fork-based clone), and checks nothing out.
- **Python 3 with `pyyaml` and `cerberus`**, the same modules PX4's build uses to validate YAML.

## Using

```
/px4-param-review 28850
```

A bare number is taken as a `PX4/PX4-Autopilot` PR.
With no PR, it offers to review the parameter changes on your local branch (uncommitted edits included), or to audit named parameters as they stand.

The script can also be run by hand, for instance while rewriting a batch:

```bash
python3 scripts/param_desc_check.py --repo ~/github/px4/PX4-Autopilot \
  --base $(git -C ~/github/px4/PX4-Autopilot merge-base HEAD upstream/main) --head WORKTREE \
  --scratch /tmp/param-check src/modules/logger/module.yaml
```

## Output

1. **PR triage summary.** Bug count and location, parameters by classification, description size before and after, and findings by area (`Schema validity` / `Facts` / `Concision` / `Wording`).
2. **Issue summary per file.**
3. **Detailed per-file review.** A row per issue with line, parameter, the rule it breaks, severity, and a suggested fix.
4. **Dropped content**, below the tables: one line per rewritten parameter saying what was cut and why that was allowed.

| Severity | Meaning |
| --- | --- |
| `bug` | A configuration-affecting fact lost or wrong, a reference to a nonexistent parameter, or a schema failure |
| `style` | A named rule of the standard broken, meaning intact |
| `minor` | A preference the author can decline |
