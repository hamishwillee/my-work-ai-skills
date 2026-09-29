# Concision lens

Is each description as short as the standard asks, with every piece of information in the right place?
This lens doesn't judge whether facts were lost (that's the facts lens); it judges where the kept text sits and whether any of it is redundant.

Applies to Rewritten and New parameters (`shared.md`, "Classification").
Read `description-standard.md` in full, and `examples.md` for how the rules were applied in practice.

## What to check

Work every Rewritten and New parameter through these, in order.

**Short** (S2 to S6):

- Is it a terse phrase that says what the parameter is or controls?
- Does it repeat the type ("(integer bitmask)"), or say "This parameter"?
- For a Rewritten parameter: did `short` change, and if so was the old one wrong, unclear, or repeating the type (S3)?
  A correct `short` reworded for taste is a `minor` finding: it discards translations for no gain.
- Would one qualifier moved into `short` make `long` unnecessary (S4)?
- Does it refer to another parameter or a mode by anything other than the full parameter name (S5)?
- Does it use an abbreviation a reader can't expand (S6)?

**Long** (L1 to L3, L5 to L7, L9):

- Remove, in your head, every sentence that says what `short`, the metadata, or the labels already say.
  Anything you removed is a finding (L1, L2); if nothing is left, the finding is to delete `long`.
- Does `long` list the options, numbered or not, or say "By default..." when the default is already stated (L3)?
- Does it carry boilerplate, restatement, an example that repeats the rule, or rationale that doesn't change the value a reader picks (L5)?
- Where the text disables, conditions, or cross-references, does it use the stock phrase (L6)?
  "Set to 0 to disable.", "Set to -1 to disable.", "Only used when X is enabled.", "e.g."
- Where sibling parameters in the same file say the same thing, do they use the same words (L6)?
- Is a unit given in prose that could be a `unit:` field the schema allows (L7)?
- If the option labels use an abbreviation or coined term, does `long` explain it once (L9)?

**Option labels** (O1 to O4):

- Is per-option detail in the right place: a few words in the label's parentheses (O1), more as a `Label: effect.` line in `long` (O2)?
- Does each `Label:` in a per-option line match its label text exactly (O2)?
- Does each label addition still read on its own, or has it been cut to fragments that lose the meaning (O3)?
  This is the check the tracking PR's review flagged as "data loss"; a cryptic label is `style`, or `bug` when the facts lens would count the lost meaning as configuration-affecting (report it once, as `bug`).
- Were any options renumbered or dropped while rewording (O4)?

## The script's flags

The main agent passes you `param_desc_check.py`'s output for your parameters.
Its flags (boilerplate, symbol-as-word, non-stock wording, unit in prose, numbered option lists, per-option labels that match no label, short repeating the type) are candidates, not findings: confirm each against the text and the rule, and drop false positives.
Then do the checks above yourself; most redundancy is a restatement in different words, which no pattern finds.

## Suggestions

Every finding suggests the replacement text, not just the problem: the rewritten sentence, the label with its parenthesis, or "delete `long`".
Prefer wording already used in the same file or `examples.md` (L6).
A replacement longer than one line goes below the tables as a suggestion block, as a YAML snippet the author can paste.

## Returning findings

One row per finding: file, line, parameter, issue (naming the rule ID), severity, suggestion, and evidence (the quoted text and, for a redundancy, where the same information already is).
