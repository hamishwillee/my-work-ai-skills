# Grammar-style lens

Applies to **every** changed `docs/en/` file, regardless of category.
This is the one check every part of the PX4 documentation shares, so it runs uniformly and doesn't consult the routing table.

Your rules are `references/style-guide.md` in full, plus the grammar/spelling checks and the audience-level check below.
All are `style` findings unless noted otherwise.
Run through each changed line once for grammar and spelling, once for audience level, and once for the style guide table, rather than skimming for all three at once.

## Grammar and spelling

- Spelling: British English throughout, minus the industry-terminology exceptions in `style-guide.md`.
  Flag genuine misspellings and Americanisms outside the exception list; don't flag a proper noun, product name, or anything inside a code span, parameter name, or file path.
- Grammar: subject-verb agreement, verb tense consistency within a procedure (a numbered-step list shouldn't drift between imperative and descriptive mood mid-list), pronoun-antecedent agreement, correct article use, comma splices, dangling or misplaced modifiers.
- Sentence-level clarity: a sentence that's grammatically valid but genuinely hard to parse (a long noun cluster, an ambiguous "it"/"this" with no clear antecedent, a modifier that could attach to either of two things) — flag it with the ambiguity named and a rephrase.
- Typos and duplicated words ("the the", "a a"), including inside headings and list items, not just paragraph prose.
- Terminology drift: the same concept named two different ways in nearby text (e.g. "flight controller" and "autopilot board" used interchangeably for the same thing on one page) without the page ever establishing they're synonyms.
  Flag once per page with both instances, not once per occurrence.

## Audience level

Write for a reader with roughly high-school knowledge: careful and capable, but without engineering or software training, and possibly reading in a second language.
The published style guide doesn't state an audience; this is this skill's standard, so name it as the rule in a finding ("audience level: ...").

- **Jargon and acronyms.** A technical term, abbreviation or acronym needs, at its first use on the page, either a link to a page that explains it or a short definition in place ("DShot, a digital protocol for controlling ESCs, ...").
  Flag one that has neither.
  Prefer a link to a PX4 docs page that explains the term; otherwise suggest a definition in place.
  Don't flag a term that is already defined or linked earlier on the same page, a term that is the page's own subject and is explained in its introduction, or an everyday term (USB, GPS, battery, Wi-Fi).
  Don't flag a term that is standard in drones and flight controllers either, such as IMU, FMU, ESC, PWM, UART, I2C, SPI or CAN.
  Readers of these pages know them, so never expand one in place; at most, link its first use in running text, and only when a PX4 docs page explains it.
  When no PX4 page explains such a term, leave it unlinked rather than inventing a definition.
- **Links, not glosses.** A link that explains a term is enough on its own: don't also add a parenthetical expansion after it ("[ESCs](...) (electronic speed controllers)").
- **Not in labels.** Don't link or expand a term inside a bold list label such as `**Main FMU processor:**`.
  The label acts as a heading, so a link belongs in the value after it, or in running text.
- **Assumed knowledge.** A step or explanation that depends on something the page neither explains nor links, such as what a parameter is, how to set one, how to open a terminal, how to flash firmware, or which connector is which.
  Suggest a link to the PX4 page that covers it.
- **Needless complexity.** Wording that is harder than the idea it carries: a long or abstract word where a plain one says the same thing (`utilise` → `use`, `in order to` → `to`), a chain of nouns, or a passive sentence that hides who does what.
- **Calibrate to the page.** Pages in the developer and simulation categories (`references/shared.md`, routing table) can assume the prerequisites they state or link, such as programming, a terminal, or git; flag only jargon beyond those.
  Never suggest replacing a precise technical term with a plainer one that would be wrong: suggest a definition or a link instead, so the precision stays.

Severity: an undefined, unlinked term or an assumed step that the reader needs in order to follow the page is `style`.
A plain-language rewording that is a preference is `minor`.
Flag each term once per page, at its first use.
A suggested link must point at a page or anchor that exists at the head SHA: check it before suggesting it.

## Style guide compliance

Work `references/style-guide.md` section by section against the diff:

- Spelling and grammar → already covered above, don't double-report.
- Emphasis markup table: bold/italic/code used for the wrong purpose.
- Headings: wrong level, wrong capitalisation, styled heading text.
- Admonitions: an altered `::: tip`/`::: info`/`::: warning` keyword — this one is `bug`, not `style`, because it breaks rendering.
- Line breaks: a paragraph hard-wrapped to a fixed column instead of broken on sentences.
- Videos: a YouTube embed not in `<lite-youtube>` form; a new long tutorial video where a shorter written procedure would serve (flag as `minor`, not `style` — this is a preference, not a hard rule).
- File/folder placement and naming, and image sizing/format/alt-text conventions — only when the diff actually adds or renames a file or image; don't re-litigate an unchanged file's name.

## What this lens doesn't cover

Leave to the structural lens: heading *order* within a page template, SUMMARY.md entries, and whether a page belongs in its folder at all.
Leave to the accuracy lenses: whether a claim is technically true.
This lens only checks how something is said, never whether it's correct.

Also leave alone, because tooling already catches it and re-reporting it is noise: Prettier-fixable whitespace/indentation down to the character, markdownlint-style list marker consistency, and trailing newline issues.
Flag formatting only when it's visibly wrong to a reader, not merely non-canonical.
