# Project conventions

## Line breaks in markdown

Use semantic (sentence) line breaks in every markdown file in this repo, not fixed-width hard wraps.
Break after each sentence, not at an arbitrary column — a paragraph is one sentence per line, not one 80-character line wrapped mid-sentence.
This makes diffs land on the sentence that actually changed instead of reflowing the whole paragraph.

Exceptions: table rows and YAML frontmatter values stay on one line each (markdown tables and YAML don't tolerate a mid-cell break), and fenced code blocks are left exactly as their source formats them.

## Editing this skill

- `SKILL.md` orchestrates (Scope → Tool check → Dispatch → Report); `references/*.md` hold the rules each lens applies. Changing what a lens checks usually means updating both the lens file and the Dispatch prompt in `SKILL.md`.
- `references/description-standard.md` is the single statement of the standard, and every lens cites its rule IDs. Add a rule there, with where it came from (the #27758 spec, or a linked review comment), rather than inside a lens file. Don't renumber existing IDs: reports cite them.
- The script's flags are candidates, never findings. Keep its checks mechanical and cheap to confirm; judgement belongs in the lenses. When adding a check, run it over a large file at `--all` to see the false-positive rate before keeping it.
- Test changes against PR 28850 (head `b36ca53ca4367ce3a33d688a3a2aa4e0cb1690e9`, base `5fb15552bb187e32b330402a54f0e7846c0aac60`): its text is the reviewed, merged calibration point, so it should come back with few findings (the `SDLOG_PROFILE` label bug is a known true positive), and its base text should trip most of the rules.
