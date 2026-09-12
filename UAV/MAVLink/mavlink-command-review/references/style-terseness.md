# Lens: style & terseness

## This repo's own conventions

Read `CLAUDE.md` at the root of `mavlink-devguide` in full — it's short. As of this skill's writing it establishes:

- VitePress callout syntax (`::: info`, `::: tip`, `::: warning`, `::: danger`) — never `> **Note**` or `> **Tip**` blockquote-style callouts.
- Math via `markdown-it-mathjax3` (`$...$`, `$$...$$`).
- Internal links as relative paths to `.md` files (`../messages/common.md#MAV_CMD_...`), not absolute `https://mavlink.io/...` URLs to the site's own pages.
- Content only in `en/` — never hand-edit `zh/`, `ko/`, or any other translated copy.

A page's own established pattern outranks a generic preference below when the two conflict and the page's pattern isn't itself a bug (e.g. if every sibling command section on a page uses a specific table column order, match it, even if a different order would also be reasonable).

## Terseness

The house style for these pages is short, direct sentences and compact param-table cells — look at the surrounding, unchanged sections on the same page as the actual baseline, not this file's own examples.

- A new sentence describing a param or command should be roughly the same length and register as the sibling entries around it. A table cell that runs noticeably longer than its siblings for a comparable param, with no added information density to justify it, is `style`.
- Prefer restating a fact once over restating it with added hedges or qualifiers that don't change its truth value ("generally tends to typically," "in most normal cases"). Flag padding, not caution — a genuinely uncertain claim should stay hedged (and cited per `accuracy.md`), just not padded on top of that.
- Rewriting already-accepted wording with no stated reason (not a correction, not new information, purely a style preference) is `minor` on its own — but see `change-discipline.md` if it's also bundled into a commit that doesn't disclose it.
- A duplicated word, a dropped word, or an internally inconsistent term for the same thing (calling one param "Heading Required" in one row and "heading required" as a different concept two rows down) is `style`, or `bug` if it changes what a reader would understand the param to do.

## Structure

- A new page or section should follow the shape of its nearest sibling: heading levels, whether params get their own `#### Params` subsection, whether there's a per-command "Autopilot Support" subsection (only when it has evidenced content — see `accuracy.md`, "Newly invented sections").
- `SUMMARY.md` must be updated in the same PR that adds a new page (see the repo's `CLAUDE.md`, "Navigation / Sidebar") — a new page with no `SUMMARY.md` entry is `bug`, since it silently never appears in the built site's sidebar.
- A relative link to an anchor on another page (`#some-anchor`) should be checked that the anchor still exists after the PR's own changes, when the PR moves or renames headings on the target page — a stale anchor is `bug`.
