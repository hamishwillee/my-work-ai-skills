# Lens: change discipline

This lens exists because of exactly one failure mode: a commit or PR labelled as a pure reorganization (a move, a rename, a file split) that also quietly changes what the text means. The reviewer then has to manually diff old and new content by hand to find the changes, because nothing about the PR's shape told them to look.

## Classify every hunk

For each changed hunk in an in-scope file, classify it as one of:

- **Pure move.** Text relocated (possibly to a different file) with no wording change at all — diff it against its prior location word-for-word if the PR's description or commit messages claim a move; if even one word differs, it isn't pure.
- **Content change.** Wording added, altered, or removed — a new sentence, a reworded sentence, a deleted claim, a table row whose text changed, a scope statement widened or narrowed (e.g. a cross-reference link added to a param row that didn't have one before).

## Bundling is the finding, not the content change itself

A content change is not, by itself, a problem this lens raises — that's `accuracy.md`'s job.
This lens's finding is specifically: **a commit (or, if the PR is a single commit, the PR itself) contains both a pure-move hunk and a content-change hunk, with nothing in the commit message or PR description distinguishing them.**

- Severity `style`: recommend splitting into separate commits — one that moves text verbatim, one (or more) that changes wording — so a reviewer can diff each independently. Name specifically which hunks are the move and which are the change.
- If the commit message or PR description explicitly says "no wording changes" or similar, and a content-change hunk exists anyway, raise it as `bug`: the description is actively wrong, which is worse than no description at all — it tells the reviewer not to look.

## Unevidenced additions are a change-discipline finding too, not just accuracy's

If a content-change hunk asserts something new with no evidence at all attached (not even a claim of it being tested, not a citation, not a source of any kind) *and* it's bundled into a commit that isn't clearly labelled as adding new evidenced content, flag it here as well as (not instead of) whatever `accuracy.md` finds on the same line — this lens's angle is that the bundling itself hid the new claim from review, which is a distinct problem from the claim being uncited.

## What this lens doesn't cover

Whether a specific claim is actually true, or whether it's cited well enough — that's `accuracy.md`.
Terseness and house style — that's `style-terseness.md`.
