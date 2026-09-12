# Shared rules

Read by every lens, before that lens's own file.
This holds what all lenses share: the read-only rule, the scope reminder, sources of truth and their precedence, verification, and severity.

## Read-only

You are read-only.
Never modify a file in the repository under review, and never run `gh pr comment`, `gh pr review`, `gh pr edit`, or any other write operation.
The one file you may create is the report itself, and only the main agent does that, only when the reviewer asks for it, and only outside the clone.

## Scope reminder

In scope: hand-authored mavlink-devguide pages whose primary subject is the meaning, parameters, or per-autopilot behaviour of one or more specific `MAV_CMD` commands or message fields.
`en/services/mission_item_detail.md` is the model case: one `###` section per command, a Params table, sometimes an Autopilot Support subsection.

Out of scope, always: `en/messages/*.md`.
Those files are generated from the MAVLink XML by this repo's own build tooling — they are never hand-edited in a PR.
A PR that touches one is a `bug`-severity finding from `change-discipline.md`, not a content review of what it says.

Out of scope for this skill (belongs to a future services-focused sibling): a page or section that's primarily about a *protocol* — upload/download sequencing, retry/ack behaviour, a state machine — even when it mentions specific commands in passing. `en/services/mission.md`'s own body (as opposed to `mission_item_detail.md`, which it links out to) is the example: it describes the mission upload protocol, not what any one `MAV_CMD` means.

`zh/`, `ko/` and any other translated copy are Crowdin-managed and never hand-edited against `main`; a PR touching one is the same `bug`-severity structural finding as touching a generated `messages/*.md` file.

## Sources of truth

Listed in precedence order: a claim backed by a higher source outranks one backed by a lower source. Where two genuinely contradict each other, report the contradiction — don't pick a winner yourself.

1. **The corresponding entry in `en/messages/<dialect>.md`** (`common.md`, `ardupilotmega.md`, etc.), which mirrors the MAVLink XML directly. This is the fastest, cheapest, and most authoritative check for anything about a param's existence, number, name, or the description/units/values the spec itself gives it.
2. **The PR's own diff**, when it changes something else alongside the doc (rare in this repo, but a linked XML PR or a cited source snippet pasted into the description counts).
3. **A citable implementation source**, for any claim about what a specific autopilot (ArduPilot, PX4) actually does — a file/line in that project's own repo, a linked test, or a linked GitHub issue/PR discussion. This is required for any claim more specific than what the XML already states; the XML describes the protocol, not what any given flight stack has actually implemented.
4. **Sibling sections on the same page or a linked page**, for consistency (e.g. do the other `MAV_CMD_NAV_LOITER_*` sections use the same phrasing for the shared multicopter/fixed-wing behaviour sentence).
5. **This repo's own `CLAUDE.md`** ("Authoring Conventions"), for style/terseness/link/callout rules.
6. **Past review comments** on the same PR or a linked issue.
7. **This skill**, last on purpose: everything above it is published and reviewable, `SKILL.md` and these references aren't.

### Reaching the sources

- **PR diff, description, linked issue**: `gh pr view`, `gh pr diff`, `gh api`.
- **`en/messages/*.md` on the base branch**: read it directly from a local clone if one exists, otherwise `gh api repos/mavlink/mavlink-devguide/contents/en/messages/<dialect>.md?ref=<base-sha>` or fetch the raw file at that SHA.
- **ArduPilot/PX4 source**: prefer a local clone if the reviewer has one (check `~/github/ArduPilot/ardupilot` and `~/github/PX4/PX4-Autopilot` and siblings); otherwise fetch the file at a recent commit on the project's default branch via the GitHub API, and say in the finding that the source wasn't pinned to a specific commit.
- **This repo's `CLAUDE.md`**: read it directly; it's short and worth reading in full rather than grepping.

### When the doc and the XML disagree

If a proposed or existing sentence states something about a param's meaning, range, or units that contradicts `en/messages/<dialect>.md` (and so the XML), that is never resolved by rewriting the prose to assert a third, different thing, and it is never resolved by silently preferring the prose over the XML either.
Report it as a `bug` framed as a conflict needing a decision, not a typo needing a fix: state what the XML says, what the prose says, and that resolving it means either (a) correcting the prose to match the XML, or (b) opening a fix against the MAVLink XML itself (`mavlink/mavlink`) if the XML is what's actually wrong, since this repo can't override the spec by describing it differently.
Never write or suggest doc text that disagrees with the current XML as a fait accompli — a prose "correction" that contradicts the XML always needs one of those two paths named explicitly, not applied.

## Verification

Every finding needs evidence you actually checked, not evidence you expect to be true:

- **Accuracy**: name the source you checked it against (file/line in `en/messages/*.md`, a file/line in the ArduPilot/PX4 repo, a linked test or issue) and what it says. "Seems right" or "seems like it should work this way" is not evidence — if you can't point to a source, the finding is "unevidenced claim," not "confirmed correct" or "confirmed wrong."
- **Line numbers**: match the head SHA's file, not a cached or paraphrased version. If you can't find the line by exact string match, drop the finding rather than guess its location.

A finding that fails verification is dropped, not downgraded.

## Severity

| Severity | Meaning |
| --- | --- |
| `bug` | A reader ends up misinformed about what a command/param does, or the doc states something that contradicts the XML or a cited implementation source |
| `style` | A claim more specific than the XML with no citation attached; a wording change bundled into a commit labelled as a pure move; new prose that doesn't match the page's existing terseness |
| `minor` | No rule violated; a preference the author can decline |

An uncited implementation-specific claim is `style`, not `bug`, precisely because it might be true — the problem is that nobody can tell from the PR alone. It only becomes `bug` once it's checked against a source and found to actually contradict that source, or found to contradict the XML directly.
