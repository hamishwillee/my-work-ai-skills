# Tool-check lens

Runs once, unbatched, over every changed `.msg` file in the PR — never split across subagents, since it's one script invocation either way.

This lens doesn't hand-check the structural rules in `style-guide.md`; it runs the project's own validator and reports what it says.
Don't re-derive units, `@enum` consistency, or whitespace rules by reading the standard — that's what the tool is for, and duplicating it by hand risks disagreeing with the actual parser.

## Local and audit modes

For local branch mode or single-message audit mode (`SKILL.md`, "No PR given"), there's no PR to fetch — the content to validate is already sitting in the reviewer's own working tree, uncommitted edits included.
Skip straight to step 4 below, running the script directly from the clone's root against whatever's currently checked out.
Nothing is created and nothing needs tearing down: running the generator only reads `msg/` and writes to its own `-d` output directory, so it's safe to run in place.

## Running the tool

1. Find a local `PX4-Autopilot` clone (`shared.md`, "Reaching the sources"). If none exists, say so in your return and skip this lens's checks entirely — don't try to hand-simulate the parser.
2. **PR mode only.** Fetch the PR's head into a scratch branch without touching the reviewer's own checkout:
   ```
   git -C <clone> fetch origin pull/<PR-number>/head:px4-uorb-review-scratch-<PR-number>
   ```
3. **PR mode only.** Create a disposable worktree at that branch:
   ```
   git -C <clone> worktree add <tmpdir> px4-uorb-review-scratch-<PR-number>
   ```
4. Collect the changed (or, in audit mode, the single audited) message names: for each `msg/*.msg` or `msg/versioned/*.msg` path in your assignment, take the filename without its `.msg` extension (`msg/versioned/Wind.msg` → `Wind`). Join them with spaces into one `-m` argument.
5. Run the tool from the repo root you're validating — `<tmpdir>` in PR mode, the clone's own working directory in local/audit mode (it resolves `msg/` relative to its own file, so it must be *that* checkout's copy of the script, or you'll validate the wrong version of the file):
   ```
   python3 Tools/msg/generate_msg_docs.py -d <scratch-output-dir> -e -m "Name1 Name2 Name3"
   ```
   The `-d` output directory just needs to exist; its generated markdown isn't used by this lens — only stdout matters.
6. Capture stdout in full.
7. **PR mode only.** Tear down: `git -C <clone> worktree remove --force <tmpdir>`, then `git -C <clone> branch -D px4-uorb-review-scratch-<PR-number>`. Do this even if the run failed or was interrupted — never leave a scratch worktree or branch behind. Local/audit mode created nothing, so there's nothing to tear down.

## Reading the output

Every line is prefixed `WARNING:` or `NOTE:` and carries the offending filename and line number in parentheses, e.g.:

```
WARNING: Unknown Unit: [meters] on `altitude` (msg/versioned/Wind.msg: 12)
NOTE: Line has trailing whitespace (msg/versioned/Wind.msg: 9): float32 tas_innov #  [m/s] True airspeed innovation
```

- **`WARNING:` → `bug`.** The tool is telling you the generated docs will render wrong or misleadingly, or a field/constant fails the standard outright (unknown unit, `@invalid`/`@frame` value not in the allowed set, constant not matched to its field's `@enum`, missing message summary, malformed command-parameter block).
- **`NOTE:` → `style`.** Whitespace and formatting nits (trailing whitespace, leading whitespace before a declaration, multiple internal spaces, an internal comment, an empty line at file start) — real, but cosmetic.

For each line, match its filename and line number against the diff:

- **Line falls inside a hunk this PR changed** (added or modified in this diff) → report it as a finding at the severity above.
- **Line falls outside any hunk this PR changed** (pre-existing, on an untouched declaration) → don't report it as a finding; instead pass it up as one of the "pre-existing issues" items for the main agent to place below the tables (`shared.md`, "New-or-changed determination"; `SKILL.md`, "What goes below the tables").

In single-message audit mode there's no diff to compare against — every line the tool prints for the audited message is a finding, at the severity above, none of them "pre-existing."

If the tool prints nothing for a message you asked about, that message is clean — say so rather than returning prose, same as any other lens with no findings.
