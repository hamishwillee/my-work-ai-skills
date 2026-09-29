# Shared rules

Read by every lens, before that lens's own file.
This holds what all lenses share: the read-only rule, scope, the classification of each parameter, sources of truth, verification, and severity.

## Read-only

You are read-only with respect to the PR and GitHub: never modify a file in the clone, never push, and never run `gh pr comment`, `gh pr review`, `gh pr edit`, or any other write operation.
The one file the review may create is the report itself, and only the main agent does that, only when the reviewer asks for it, and only outside the clone.

Two things touch the filesystem, and neither changes the clone's files:

- The main agent may `git fetch` the PR's head and base commits into the reviewer's clone, which adds objects but checks nothing out.
- `scripts/param_desc_check.py` writes copies of the head's YAML files, validator and schema into a scratch directory outside the clone, and validates those copies.

## Scope

A parameter is defined in one of two ways, and both are in scope:

- **YAML**: a `module.yaml` or `*_params.yaml` file under `src/` with a top-level `parameters:` list, each group holding `definitions:` keyed by parameter name.
  The description is `description.short` and `description.long`; option labels are `values:` (enum) or `bit:` (bitmask).
  Almost every parameter is now defined this way.
- **Legacy C**: a `/** ... */` comment block above `PARAM_DEFINE_INT32` or `PARAM_DEFINE_FLOAT` in a `.c` file.
  The first line of the comment is the short description, the following paragraph the long one, and `@value` and `@bit` lines the option labels.
  The helper script doesn't read these, so a lens checks them by hand against the same standard.

`docs/en/advanced_config/parameter_reference.md` is generated from these sources.
A PR that hand-edits it is a `bug`; a regenerated copy is ignored, and its source reviewed instead.

Any other file the PR changes (`.cpp`, `.hpp`, `CMakeLists.txt`) is never reviewed itself, but it's a source of truth for what a parameter does: read the code that reads the parameter.

## Classification

The main agent classifies every parameter in a changed definition file before dispatching, using the helper script's output, and passes it to each lens.

- **Rewritten.** The parameter existed at the base and its `short`, `long`, or option labels changed.
  Every lens applies, and the facts lens compares the old text with the new.
- **New.** The parameter didn't exist at the base (or the whole file is new).
  Every lens applies; the facts lens checks the text against the code, since there's no old text to preserve.
- **Metadata-only.** The description is unchanged but a default, range, unit, type, or option key changed.
  Only the facts lens applies: does the unchanged text now contradict the new metadata?
- **Untouched.** Nothing about the parameter changed.
  Out of scope.
  A problem you notice in one anyway is pre-existing, reported once below the tables, never as a finding.
- **Removed.** The parameter no longer exists at the head.
  Not reviewed as text; the facts lens checks that nothing the PR leaves in place still refers to it.

**Audit mode** (the reviewer names parameters, or asks for a file to be audited without a diff) treats every named parameter as New.

## Sources of truth

In precedence order: a claim backed by a higher source outranks one backed by a lower source.

1. **The code that reads the parameter**, at the head: find it with `grep -rn "<NAME>"` over `src/` (for a `${i}` parameter, search the name with the instance part removed, and the `snprintf` pattern that builds it), and read the lines that use the value.
   This is what "true to the code" means in `description-standard.md` L8.
2. **The parameter's own metadata at the head**: `type`, `default`, `min`, `max`, `unit`, `reboot_required`, and option keys.
3. **The description at the base**, for a Rewritten parameter: what the text said before is evidence of what the author knew, not proof that it was right.
   Where the old text and the code disagree, the code wins, and the disagreement is reported.
4. **`validation/module_schema.yaml` and `Tools/validate_yaml.py`** at the head, for what's structurally valid.
5. **`references/description-standard.md`**, the written standard, and `references/examples.md` for how it was applied.
6. **Sibling parameters** in the same file or module, for how the same idea is already worded (L6).
7. **This skill**, last on purpose: everything above it is published and reviewable.

Where two genuinely contradict each other, report the contradiction instead of picking a winner.

### Reaching the sources

- **PR diff, description, linked issue**: `gh pr view`, `gh pr diff`, `gh api`.
- **A local `PX4-Autopilot` clone**: look in `~/github/PX4/PX4-Autopilot`, `~/github/px4/PX4-Autopilot`, and sibling locations.
  Fetch from the remote that points at `PX4/PX4-Autopilot`, which in a contributor's clone is often `upstream` rather than `origin`: `git -C <clone> remote -v` says which.
- **A file at a commit**: `git -C <clone> show <sha>:<path>`, or `gh api repos/PX4/PX4-Autopilot/contents/<path>?ref=<sha>` without a clone.
- **Code that reads a parameter**: `git -C <clone> grep -n "<NAME>" <head-sha> -- src/`.

## Verification

Every finding needs evidence you checked:

- **A standard rule**: cite its ID from `description-standard.md` and quote the offending text.
- **A lost fact**: quote the sentence in the base text that carried it, and say where in the head's `short`, `long`, labels, or metadata you looked for it and didn't find it.
- **A claim against the code**: name the file and line that contradicts it, and quote the line.
- **A script flag**: never report a flag on the script's say-so; confirm it against the text and the rule, and drop it if it's a false positive (a MAVLink message name taken for a parameter, say).
- **Line numbers**: match the head's file.
  The script prints the line of each parameter's `short`, `long`, and labels; use those.
  If you can't find the line by exact string match against the head file, drop the finding rather than guess.

A finding that fails verification is dropped, not downgraded.

## Severity

| Severity | Meaning |
| --- | --- |
| `bug` | A reader configures the parameter wrongly or can't find out how: a configuration-affecting fact lost or changed (L4), text contradicting the code or metadata, a reference to a parameter that doesn't exist, a schema validation failure, or YAML that no longer parses |
| `style` | A named rule in `description-standard.md` is broken but the meaning survives: restated options, boilerplate, a non-stock phrase, a mid-sentence `|` wrap, an unexplained abbreviation, a cryptic label |
| `minor` | A preference the author can decline: a tighter wording, a unit that could move to `unit:`, a spelling variant, a borderline dropped fact that the metadata arguably still carries |

Removing words is the point of these PRs, so length alone is never a finding: text is `style` only when it breaks a rule, and `minor` when it could simply be shorter.
