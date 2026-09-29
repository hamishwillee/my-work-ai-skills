# Wording lens

Is the text that this PR wrote readable, correctly formed YAML, and rendered correctly in both QGC and the docs?

Applies to the `short`, `long`, and option labels of Rewritten and New parameters, and only to text the PR wrote or changed (`shared.md`, "Classification").
Read `description-standard.md` in full; the W rules are this lens's, and S6 and O3 overlap it.

## Grammar and clarity

- Grammar: subject-verb agreement, articles, tense, comma splices, dangling modifiers.
  `short` and labels are phrases, so a missing verb or article there isn't an error.
  `long` may be terse (W1): a noun-phrase opening or a clipped clause is fine when its meaning is plain, and isn't a finding.
  Flag a fragment only when it's ambiguous, as a clarity finding below.
- Clarity: a sentence that's valid but hard to parse, or ambiguous about what "it" or "this" refers to, or which parameter a condition belongs to.
  Name the ambiguity and suggest a rephrase.
  Compressed text is where ambiguity creeps in: "Conditional mode only fuses it below EKF2_RNG_A_VMAX speed and EKF2_RNG_A_HMAX height" should leave no doubt about "it".
- Symbols and invented abbreviations used as words (W1, S6).
- Spelling (W6): British English in text this PR wrote, except industry-standard terms, names, and code identifiers.
  Flag at `minor`: existing parameter text is mostly American and consistency within a file matters as much.
- Typos and duplicated words, at `style`.

Severity: `bug` if a sentence is misleading or unparseable; `style` for a named-rule break or a real grammar error; `minor` for a nit.

## YAML form and rendering

Check the raw YAML at the head, not just the parsed text:

- **W2.** Is prose in a `|` literal block wrapped mid-sentence?
  Each newline shows as a line break in QGC.
  The fix is a plain or quoted scalar (which YAML folds) or joining the lines.
- **W2.** Does a `|` or `|-` block hold anything other than one `Label: effect.` line per option?
- **W3.** Does every per-option line end in a full stop?
  The docs reference joins the lines, and without one the options run together.
- **W4.** Is a scalar containing `: ` unquoted?
  YAML either fails to parse it or reads it as a mapping; the script's validator run shows which.
- **W5.** Does a multi-instance (`${i}`) description keep its placeholder where the old one had it?
- Does `short` end with a full stop in one parameter and not its neighbours in the same file?
  Only flag it when the PR introduced the inconsistency, at `minor`: the generator adds one anyway.

## Returning findings

One row per finding: file, line, parameter, issue, severity, suggestion, and evidence (the quoted text, and for W2 to W4 the raw YAML lines).
