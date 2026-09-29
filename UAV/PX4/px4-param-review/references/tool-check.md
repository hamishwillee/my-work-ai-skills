# Tool check

Run by the main agent, once, before dispatching the lenses: its output classifies every parameter, and the lenses need that classification and the line numbers.

`scripts/param_desc_check.py` in this skill does four things for a list of YAML definition files:

- classifies each parameter as new, rewritten, metadata-only, or removed, by comparing the base and head versions (untouched parameters aren't printed)
- prints the line of each parameter's `short`, `long`, and labels in the head file, and its description size (characters of `short` + `long` + option labels) before and after
- prints candidate flags for the standard's mechanical rules, each with a line number and the rule's gist
- runs the head's own `Tools/validate_yaml.py` against the head's `validation/module_schema.yaml`, on scratch copies of the head files

It needs Python 3 with `pyyaml` and `cerberus` (the same modules PX4's own build uses to validate YAML).
If either is missing, say so, and run the lenses without the script's output: classify parameters from the diff by hand, and note in the report that schema validation didn't run.

## Running it

1. Find the local clone and the remote pointing at `PX4/PX4-Autopilot` (`shared.md`, "Reaching the sources").
   Without a clone the script can't run; classify from `gh pr diff` by hand and say so in the report.
2. **PR mode.** Fetch both commits, without checking anything out:
   ```
   git -C <clone> fetch <remote> <head-sha> <base-sha>
   ```
   If fetching a SHA directly is refused, fetch `pull/<N>/head` from the same remote.
   Then use the merge-base as the base, so changes on the base branch since the PR branched aren't counted as the PR's:
   ```
   git -C <clone> merge-base <base-sha> <head-sha>
   ```
3. **Local-branch mode.** The base is `git -C <clone> merge-base HEAD <remote>/main`, and the head is the literal `WORKTREE`, which reads the working tree, uncommitted edits included.
4. **Audit mode.** Pass `--all` and no `--base`; the head is `WORKTREE` or a SHA.
5. Run it over every changed definition file (`*.yaml` under `src/` whose diff touches a `parameters:` definition), with a scratch directory outside the clone:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/param_desc_check.py --repo <clone> --base <merge-base> --head <head-sha|WORKTREE> --scratch <scratch-dir> <file> [<file> ...]
   ```
   Legacy `.c` definitions aren't read by the script; list them for the lenses to check by hand.

## Using the output

- **Classification and line numbers** go to every lens in its dispatch prompt, for the parameters in its batch.
- **Flags** go to the lenses too, as candidates.
  The script never produces a finding directly: every flag is confirmed or dropped by a lens against `description-standard.md`.
- **Validator errors** are findings in their own right, `bug` severity, under "Schema validity" in the triage table.
  Quote the validator's line.
  An error on a parameter the PR didn't touch is pre-existing, and goes below the tables.
- **Size totals** go in the triage summary's opening lines, as "Description text of the changed parameters: 9705 → 4448 characters (−54.2%)".
  When the PR description claims a figure, compare it; a large mismatch is worth a line, since the size is often the PR's stated purpose.
