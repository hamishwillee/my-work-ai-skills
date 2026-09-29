# Facts lens

Does the new text still tell a reader everything they need to configure the parameter, and is all of it true?
This is the lens that guards against "stripping that down too much", so it works fact by fact, never by impression.

Applies to Rewritten, New, Metadata-only and Removed parameters (`shared.md`, "Classification").

## Rewritten parameters: the fact ledger

For each Rewritten parameter:

1. **List the facts in the old text.**
   Split the base `short`, `long`, and option labels into atomic statements: one behaviour, condition, dependency, limit, special value, warning, unit, or piece of rationale each.
   "Set this parameter to zero to turn off the bluff body drag model for this axis" is one fact (0 disables it, per axis); "The drag produced by this effect scales with speed squared" is another.
2. **Find each fact in the new version.**
   Look in the head's `short`, `long`, option labels, and metadata (`unit`, `min`, `max`, `default`, `reboot_required`).
   A fact carried by metadata counts as kept: "expressed in amperes" is kept if `unit: A` is set.
3. **Classify every fact you can't find** by `description-standard.md` L4 and L5:
   - **Configuration-affecting** (L4): lost, a `bug`.
     Quote the old sentence, and suggest the shortest wording that restores it, in the place the standard puts it (label, `Label: effect.` line, or `long`).
   - **Droppable** (L5): a restatement, boilerplate, an example that repeats the rule, or rationale that doesn't change the value a reader picks.
     Not a finding; it goes in the dropped-content note (see "Returning findings").
   - **Borderline**: the fact is arguably carried by a label or by another parameter's description, or it's rationale a reader might use to pick a value.
     A `minor` finding saying what was dropped and where it arguably survives, so the reviewer decides.
4. **Check each kept fact still means the same.**
   A rewrite can keep a fact's words and change its meaning: a dropped "only", a merged condition, "below X speed and Y height" where the old text meant "below X speed or Y height".
   A changed meaning is a `bug` unless the code shows the new meaning is the right one, in which case it's a correction, and you say so.

Compare against the code, not only the old text (`shared.md`, source 1): where the rewrite merges or restates a condition or a special value, read the code that applies it.
`BAT${i}_I_OVERWRITE` in `examples.md` shows the check: "Set to 0 or less to disable." is right because the code tests `> FLT_EPSILON`.

## New parameters

There's no old text, so check the new text against the code:

- Every special value the code handles (0, -1, negatives, a sentinel) is described, or obvious from `min`/`max`.
- Every other parameter the code reads alongside it to decide the behaviour, and that a reader must set too, is named.
- Every behaviour the text states is what the code does.
- For an enum or bitmask, every value the code handles has a label, and no label names a value the code ignores.

A missing configuration-affecting fact is a `bug`; a wrong statement is a `bug`.

## Metadata-only parameters

Check whether the unchanged text still agrees with the new metadata: a `long` that states the old default, range, or unit, or describes an option key that was renumbered or removed, is a `bug`.

## Removed parameters

Search the head's definition files and the PR's changed docs for the removed name: a description that still tells the reader to set it is a `bug` on that description's line.

## References to other parameters

For every parameter name the text mentions (in any classification the lens applies to), confirm it exists at the head.
The script flags names it can't find; confirm each one, since a MAVLink message (`MANUAL_CONTROL`) or uORB topic name is a legitimate reference, and a `${i}` template may expand to the name.
A name that exists nowhere is a `bug` (`description-standard.md` S5).

## Returning findings

Return one row per finding: file, line, parameter, issue, severity, suggestion, and evidence (the old sentence quoted, and the code line where one was read).

Also return, separately, a **dropped-content note** for each Rewritten parameter: one line naming what was cut and the rule that permits it, as:

`EKF2_MCOEF`: momentum-transfer mechanism (L5, rationale); "see documentation for EKF2_BCOEF_X" folded into "Body drag is set by EKF2_BCOEF_X and EKF2_BCOEF_Y" (kept).

This is what lets the reviewer judge the trim without re-reading every old description, so write it for every Rewritten parameter, including those with no findings.
