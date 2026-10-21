# Structural lens

Applies to **every** changed `docs/en/` file, and to the PR as a whole rather than line-by-line — it runs unbatched over the full set of changed doc files, the same way the grammar-style lens runs over every file but per-line.

Your job is placement, navigation, and page mechanics: whether the change is *findable* and *renders*, not whether its prose or its facts are right.

## Translated-file guard

If any changed file is under `docs/<lang>/` for a `<lang>` other than `en` (`docs/ko/`, `docs/zh/`, `docs/uk/`, ...), that's a `bug`: translations are Crowdin-managed and shouldn't be hand-edited in a PR against `main`.
Name every such file; don't review the translation quality itself.

## New pages

- A new `.md` file under `docs/en/` needs a corresponding entry in `docs/en/SUMMARY.md`.
  Check the PR's file list for both; a new page with no `SUMMARY.md` change is a `bug` (unreachable via navigation), not a `style` finding.
- A new page sits in an existing, appropriately-topical sub-folder of `docs/en/` with no further nesting under it — a new file placed directly under `docs/en/` (outside any topic folder) or nested two levels deep is a `style` finding per the style guide's file-placement rule.
- A genuinely new topic area with no existing folder to hold it is worth a note rather than a rule violation — flag it as a question for the reviewer, not a `bug`.

## Heading structure

- Exactly one `#` (the page title), matching or closely paraphrasing the `SUMMARY.md` entry text for that page — a page title that no longer matches its sidebar entry is `style`.
- No heading level skips from where the diff last touched (`##` straight to `####`).
- A moved or renamed heading that other pages link to by anchor: check whether any changed or nearby page links `#old-anchor-text`; a dangling in-repo anchor link is a `bug`.

## Version badges

Documentation for a new user-visible feature is marked with a VitePress `<Badge>` naming the first release that includes it, so readers on an older release know it doesn't apply to them.
Use the PR description and its code diff to decide whether something is new: a new mode, module, driver, board, parameter, option or value, command, or build target counts; a bug fix, or a rewrite of the docs for an existing feature, doesn't.

- **Page level**: a new page for a new feature (including a new board page) carries the badge on its own line directly after the `#` title, separated from it by a blank line.
- **Heading level**: a new section for a new feature on an existing page carries the badge on its own line directly after that heading, separated by a blank line.
- **Inline**: a smaller addition, such as a new list item, table row, parameter, or option value, carries the badge inline, at the start or end of the item.
- **Text**: a feature only on `main` uses `<Badge type="tip" text="main (PX4 vX.Y)" />`, where `vX.Y` is the version `docs/en/releases/main.md` says `main` is heading for (its intro reads "features that are going to be in `main` (PX4 v2.0 or later)").
  A feature already in a release uses `<Badge type="tip" text="PX4 vX.Y" />`.
  A feature the PR or its code marks as experimental also gets `<Badge type="warning" text="Experimental" />` beside it.

A missing badge on a new feature is `style`, anchored to the heading, title, or item that should carry it.
A badge naming the wrong release is `bug`, since it tells readers the feature exists in a release where it doesn't.
Don't flag existing features that the PR doesn't add, and don't add badges to release-note pages under `docs/en/releases/`.

## Images and assets

- A newly referenced image path resolves (`../../assets/...` two levels up from the page's folder into `/assets/`) and the target file exists in the diff or already in the repo.
  A reference to an image that isn't in either is `bug` — the page will show a broken image.
- New image files land under a sub-folder of `/assets/`, not loose in `docs/en/`.

## Cross-links

- An in-repo relative link (`../../hardware/...`, `./index.md`, etc.) added or changed by the PR resolves to a real file at its head SHA.
  A broken relative link is `bug`.
- An external link added by the PR: spot-check it resolves (`WebFetch`) rather than assuming; a link that 404s is `bug`.

## What this lens doesn't cover

Leave prose quality, spelling, and style-guide emphasis/heading-capitalisation rules to the grammar-style lens.
Leave whether a claim is factually correct to the relevant accuracy lens.
This lens only checks that the page is structurally sound and reachable.
