# Project conventions

## Line breaks in markdown

Use semantic (sentence) line breaks in every markdown file in this repo, not fixed-width hard wraps.
Break after each sentence, not at an arbitrary column — a paragraph is one sentence per line, not one 80-character line wrapped mid-sentence.
This makes diffs land on the sentence that actually changed instead of reflowing the whole paragraph.

Exceptions: table rows and YAML frontmatter values stay on one line each (markdown tables and YAML don't tolerate a mid-cell break), and fenced code blocks are left exactly as their source formats them.

## Editing this skill

- `SKILL.md` orchestrates (Scope → Dispatch → Report); `references/*.md` hold the substantive rules each lens applies. Changing what a lens checks almost always means updating both files — the reference file's own rules, and `SKILL.md`'s Dispatch prompt template if the lens's job description changed too.
- The `comments` subagent never drafts a long-description suggestion itself — for a missing one, it only flags presence/absence, using the literal placeholder text `(pending source search)`. Only the main agent's own "Long-description verification" step (in `SKILL.md`) may replace that placeholder with real drafted text, because only it can time the publisher/subscriber search and pause to check in with the reviewer. Keep that boundary sharp if you touch either file.
- Report merging distinguishes two things that are easy to conflate: a true duplicate (the same problem, caught by two lenses) dedupes to one row; different problems on the same line combine into one row naming all of them, never dropping the less prominent one in favor of a more narrative finding. `SKILL.md`'s "3. Report" section once contradicted itself on this and silently dropped mechanical tool-check findings as a result — don't reintroduce that gap.
