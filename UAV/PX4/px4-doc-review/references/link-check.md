# Link check

Read by the main agent, never by a lens.
It runs the project's own link checker, `markdown_link_checker_sc`, over `docs/en/`, triages what it reports, and researches a fix for each finding.

It runs in two modes:

- **PR review**: part of every review, over the PR's changed `docs/en/**/*.md` files only, the same set CI checks.
  Findings go into the report like any other structural finding.
- **Standalone**: when the reviewer asks for a link check on their own checkout rather than on a PR.
  On `main`, or when the reviewer asks for everything, it checks the whole of `docs/en/`.
  On any other branch it checks the `docs/en/**/*.md` files changed since the branch's merge base with `main`, then offers a full run.

## Running the checker

The checker is a dev dependency of `docs/package.json`, and `yarn linkcheck` in `docs/` runs it over every file:

```sh
cd <clone>/docs && yarn linkcheck
```

That script is `markdown_link_checker_sc -r .. -d docs -e en -i assets -u docs.px4.io`.
Errors go to standard output, one block per page, and an empty output means no errors.
If `docs/node_modules` is missing, ask the reviewer before running `yarn install`, rather than installing it yourself.

**Changed files only.**
Add `-f <list.json>`, a JSON array of paths relative to the repo root (`-r`), such as `["docs/en/advanced/rtk_gps.md"]`.
Only `.md` files under `docs/en/` go in the list, and never deleted files.
Write the list to a scratch directory, not into the clone.

```sh
cd <clone>/docs && npx markdown_link_checker_sc -r .. -d docs -e en -i assets -u docs.px4.io -f <scratch>/files.json
```

**A PR is checked at its head SHA, not the clone's working tree.**
The review is read-only, so never check out the PR in the reviewer's clone.
Fetch the head commit and extract the docs from it into a scratch directory, then point `-r` there, running the binary from the clone's `docs/node_modules`:

```sh
git -C <clone> fetch https://github.com/PX4/PX4-Autopilot.git pull/<number>/head
git -C <clone> archive <head-sha> docs/en docs/assets docs/_link_checker_sc | tar -x -C <scratch>/pr-<number>
<clone>/docs/node_modules/.bin/markdown_link_checker_sc -r <scratch>/pr-<number> -d docs -e en -i assets -u docs.px4.io -f <scratch>/files.json
```

Take the file list from `gh pr view <number> --json files`, keeping `docs/en/**/*.md` paths that weren't deleted.
Delete the scratch extract when the report is done.

**External links.**
The runs above check internal links only, and CI never checks external links.
After the internal results, offer an external-link run as one line; don't run it unasked, since it is slow and requests every URL in the tree.
It adds `-x`, run from `docs/`, and for a PR review it keeps the `-f` list and the scratch `-r`:

```sh
cd <clone>/docs && npx markdown_link_checker_sc -r .. -d docs -e en -i assets -u docs.px4.io -x
```

`-x` logs to standard output; capture it to a file in the scratch directory, never in the clone, since the reviewer may keep their own logs there.

**Ignore list.**
The checker already drops errors listed in `docs/_link_checker_sc/ignore_errors.json`.
Don't re-raise them.
Only a standalone check adds to the list, and only as Adding ignore entries below describes; never in a PR review, and never with `--interactive`.

## Triage

The checker names each finding by type.
Link-check findings count under **Structural** in the report's triage table.

| Type | Severity | Notes |
| --- | --- | --- |
| `LinkedInternalPageMissing` | `bug` | Link to a page that doesn't exist |
| `LinkedFileMissingAnchor`, `CurrentFileMissingAnchor` | `bug` | Link to a heading anchor that doesn't exist, on another page or the same one |
| `LocalImageNotFound` | `bug` | The page shows a broken image |
| `ReferenceForLinkNotFound`, `ReferenceLinkEmptyReference` | `bug` | A reference-style link with no definition, which renders as literal brackets |
| `PageNotInTOC` | `bug` | Unreachable from the sidebar, as in the structural lens's New pages rule |
| `PageNotLinkedInternally` | `minor` | Only reachable from the sidebar; worth a link from its parent topic |
| `InternalLinkToHTML`, `UrlToLocalSite` | `style` | Works, but the docs link other pages by relative `.md` path |
| `OrphanedImage` | `minor` | See Orphaned images below |
| `ExternalLinkError`, 404 or 410 | `bug` | See External links below |
| `ExternalLinkError`, 301 or 308 | `style` | A permanent redirect; see External links below |
| `ExternalLinkError`, anything else | note | Such as 402, 429 or a TLS failure: list it below the tables with its status, and suggest no fix |
| `ExternalLinkWarning` | none | Temporary redirects (302, 303, 307), 403, and transient 5xx: do nothing, and don't list them |

A type not in this table is new to the checker: report it as a note with the checker's own message, and don't guess a severity.

**Line numbers.**
The checker names the page, not the line.
Anchor each finding to its line by exact string match on the link's URL or path in the file (at the head SHA for a PR).
A page-level finding (`PageNotInTOC`, `PageNotLinkedInternally`, `OrphanedImage`) anchors to line 1 of the page, or of the image's nearest referencing page.
If no line matches, drop the finding, as `references/shared.md` requires.

**In a PR review, a finding on a line the PR didn't change is pre-existing.**
It goes below the tables with the other pre-existing issues, not in the per-file tables or the counts.
A `PageNotInTOC` on a page the PR adds, or an `OrphanedImage` whose last reference the PR removed, is the PR's own and goes in the tables.

**Generated pages.**
A finding on a generated page (see Generated docs in `references/shared.md`) is fixed in its source, never in the page.
The one exception is `PageNotInTOC` on a `docs/en/msg_docs/` page: the `SUMMARY.md` block for uORB messages isn't regenerated by CI.
Running `Tools/msg/generate_msg_docs.py -d <scratch>` writes the correct block to `<scratch>/_del_summary_fragment.txt`, and the fix is to replace the block in `SUMMARY.md` (from `[uORB Message Reference](msg_docs/index.md)` to the last `msg_docs/` line) with it.
That script also rewrites `docs/en/middleware/dds_topics.md` in the clone, so run it only in standalone mode, and restore that file afterwards with `git -C <clone> checkout -- docs/en/middleware/dds_topics.md`.

**Orphaned images.**
Never suggest deleting an orphaned image that a page under `docs/<lang>/` still references, even if nothing under `docs/en/` does: translations lag behind English and still need it.
Check with `grep -rl <image-name> <clone>/docs --include=*.md` before suggesting deletion.

## Researching a fix

Offer a fix for a finding only when there's a sensible one, and give the evidence for it.
With no sensible fix, say what you searched and that nothing suitable turned up.

**Internal links.**

- **Missing page**: find where it went.
  `git -C <clone> log --diff-filter=R --name-status --format= -- '<old path>'` shows a rename, and a `SUMMARY.md` entry or page title matching the link text finds a page covering the same topic.
- **Missing anchor**: read the target page's headings (and any `{#custom-anchor}`) and suggest the one matching the link text or the old anchor's words.
  A heading renamed by this PR, or by a recent commit, is the usual cause.
- **Page not in TOC**: suggest where in `SUMMARY.md` it belongs, beside its siblings in the same folder.

**External links.**

- **Permanent redirect (301, 308)**: recommend the redirect target when it's plausibly the same resource: its URL follows a similar pattern to the original (same path with a new domain or prefix, the same slug), or its page name matches the link text.
  Fetch the target to confirm it returns a real page, not a login wall or a home page.
- **Redirect to a clear 404, or to a generic page** such as a home page or a product listing: don't recommend the target.
  Present the finding as a note, then search for an alternative as for a 404.
- **404 or 410**: search for the resource's new location.
  First on the original site, with `WebSearch` limited to its domain (`site:example.com`) using terms from the old URL's path and from the link text.
  Then on the wider internet, with the same terms.
  Recommend a result only when it's clearly the same resource: the same product, datasheet, or document, not just the same topic.
- **Temporary redirect (302, 303, 307)**: do nothing.

## Output

**PR review.**
Merge link-check findings into the report as structural findings: same file and line as a lens finding describing the same broken link is one row.
Put a suggested fix in the Suggestion column as usual, with the evidence behind it (the redirect target, the renamed file, the search that found it).
The offer of an external-link run goes last in the report, as one line.
If the reviewer accepts, report its findings as their own captioned section, **External link check**, with a table per file in the report's format.

**Standalone.**
There's no PR to triage, so open with the count of findings by severity and the number of pages carrying them, then one table per page in the report's per-file format.
Below the tables, offer to apply the suggested fixes, and offer the external-link run if it hasn't run yet.
Once the fixes are settled, offer to add ignore entries for the external errors that remain (see Adding ignore entries below).

The skill's read-only rule covers PR review.
In standalone mode the checkout is the reviewer's own, so you may apply the fixes they accept, and only those.
Edit files under `docs/en/` only, fix generated pages in their source, and never touch a file under `docs/<lang>/`.
The one file outside `docs/en/` you may edit is `docs/_link_checker_sc/ignore_errors.json`, as below.

## Adding ignore entries

Standalone mode only, and only for external errors that have no fix.
Offer it in one line, asking how long the entries should last (the checker's default is 3 months).
If the reviewer says no, stop there.

Sort the remaining errors into two groups, since only one of them can be confirmed by opening the link:

- **Likely to work in a browser**: the site blocks automated requests, as with a 402, 403, 429, or a 202 with an empty body.
  Present these one at a time, each as a clickable markdown link with the page and line it's on and the status the checker got, and ask the reviewer to open it and say whether it works.
  Wait for the answer before presenting the next link.
  Add an entry only for a link the reviewer confirms works; one that doesn't work goes back to the reviewer as a dead link, to research a fix as for a 404.
- **Can't be confirmed by opening it**: for example, an expired or invalid TLS certificate, which fails in a browser too, or a 404 waiting on a vendor's reply.
  List these together, each with its reason, and add them all if the reviewer agrees.

Add each entry with the checker's own option, run from `docs/`, using the URL exactly as the page spells it (with or without a trailing slash):

```sh
npx markdown_link_checker_sc -r .. -d docs -e en --add-ignore-url "<url>" --add-ignore-reason "<reason>" --ignore-expiry-months <n>
```

The reason is what the next person to read the list will act on, so make it accurate:

- A confirmed link: the status and that it works in a browser, such as "402/403 returned to automated requests; confirmed working in a browser".
- A certificate: the expiry date, read from `openssl s_client -servername <host> -connect <host>:443 </dev/null | openssl x509 -noout -enddate`, and "recheck before expiry"; never "works in a browser".
- A 404 awaiting a reply: who was asked and where, such as a PR number.

The option rewrites the file without its final newline, so restore it afterwards (`echo >> docs/_link_checker_sc/ignore_errors.json`) to keep the diff to the new entries.
Then rerun the external check with `-f` on the affected pages to confirm the entries suppress their errors.
