# Grammar-spelling lens

Two tiers, by where the text lives. Run each changed piece of text through exactly one tier — never both.

## Tier 1: message-level short and long description

Any message this PR adds, or whose short/long description block this PR edits.
Full grammar and spelling check, same rigour as prose documentation review:

- **Spelling**: British English throughout. Don't flag a proper noun, protocol/product name (MAVLink, DroneCAN, DShot, EKF2, RTK...), unit, acronym, or anything inside a code span.
- **Grammar**: subject-verb agreement, tense consistency, pronoun-antecedent agreement, article use, comma splices, dangling/misplaced modifiers.
- **Clarity**: a grammatically valid sentence that's still genuinely hard to parse (ambiguous "it"/"this," a modifier that could attach to either of two things) — flag it, name the ambiguity, suggest a rephrase.
- **Typos and duplicated words** ("the the").

Severity: `bug` if the sentence is actually misleading or unparseable as written; `style` for a correct-but-imperfect sentence (wrong tense, minor spelling); `minor` for a stylistic nit that doesn't affect meaning.

## Tier 2: inline field and constant comments

Any field/constant comment this PR adds or edits (any of **New**, **Renamed or retyped**, **Comment-only edit** from `shared.md`'s gate).
These are meant to be terse — a fragment, not a sentence — so the bar is different:

- **Spelling**: checked fully, same rules and severity as Tier 1 (`style` for a genuine misspelling).
- **Grammar**: checked, but every finding is severity `hint`, never `bug`/`style`/`minor`. A hint is a "could tighten this" observation, not a claim the comment is wrong — a fragment missing an article, or an odd verb form, is expected in an eight-word field comment and isn't a defect.
- Don't flag terseness itself, missing terminal periods (that's `comments.md`'s territory per the written standard), or sentence-fragment structure as a grammar problem — those are the point of a field comment, not an error.

## Returning findings

Return Tier 1 findings alongside every other lens's findings, same shape.
Return Tier 2 spelling findings the same way, at `style`.
Return Tier 2 grammar findings separately, tagged `hint` — the main agent lists these in their own section below the tables, per `SKILL.md`, never inside the triage totals.
