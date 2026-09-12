# Project conventions

## Line breaks in markdown

Use semantic (sentence) line breaks in every markdown file in this repo, not fixed-width hard wraps.
Break after each sentence, not at an arbitrary column.

Exceptions: table rows and YAML frontmatter values stay on one line each, and fenced code blocks are left exactly as their source formats them.

## Editing this skill

- `SKILL.md` orchestrates (Scope → Dispatch → Report, plus the lightweight Authoring mode); `references/*.md` hold the substantive rules each lens applies. Changing what a lens checks almost always means updating both files.
- `accuracy.md`'s protocol-level/implementation-level split is the core of this skill — it exists so a citation is required exactly where the XML can't answer the question, and not demanded where it already does. Don't collapse the two tiers into one "needs evidence" rule; that either over-demands citations for restated XML facts or under-demands them for autopilot-specific claims.
- `references/shared.md`'s "When the doc and the XML disagree" section is the direct answer to this skill's founding requirement (never let generated prose silently override the spec). Keep it phrased as "name the conflict and the two resolution paths," never as "here's how to decide which one wins" — that decision belongs to a human with authority over the XML, not to this skill.
- `change-discipline.md` only fires on the *bundling*, never on the content change itself — that's deliberately `accuracy.md`'s job. If you're tempted to add a "this claim is probably wrong" check to `change-discipline.md`, it belongs in `accuracy.md` instead.
