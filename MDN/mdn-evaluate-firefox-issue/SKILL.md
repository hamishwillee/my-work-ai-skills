---
name: mdn-evaluate-firefox-issue
description: Evaluates an MDN Firefox release-tracking issue (an mdn/content issue labelled "Firefox NNN" that lists Gecko bugs) and writes a report of what the linked Bugzilla bug(s) deliver — feature overview, release channel and platform, preferences, browser-compat-data status and PRs, related MDN issues and PRs, the docs affected (delivered and not delivered), the Experimental features page, and a suggested Firefox release note. Use when the user runs /mdn-evaluate-firefox-issue, gives an mdn/content issue number or URL and asks what it delivers, or asks to evaluate or triage a Firefox docs issue. Read-only apart from the report file. Use mdn-pr-review instead to review a PR's docs.
argument-hint: "[mdn/content issue number or URL]"
allowed-tools: Bash(gh issue view:*) Bash(gh issue list:*) Bash(gh pr list:*) Bash(gh pr view:*) Bash(gh search:*) Bash(gh api:*) Bash(curl -s:*) Bash(git -C:*) Bash(grep:*) Bash(code:*)
---

# Evaluate an MDN Firefox issue

You are evaluating an MDN Firefox tracking issue for an MDN technical writer.
The deliverable is a Markdown report that says what the Gecko work delivers, what it doesn't, and what MDN needs to do about it (BCD, docs, experimental features, release note).

**Read-only.**
Never edit a file in any repository, never commit, and never post to GitHub or Bugzilla (no `gh issue comment`, `gh pr create`, label changes, or `gh api -X POST/PATCH`).
The only file you create is the report, outside every clone.
If the writer then asks you to act on the report (add BCD, write a release note), that is a new task that follows their usual conventions, not part of this skill.

## Input

The argument is an mdn/content issue number (`46469`), `#46469`, or an issue URL.
If no argument was given, ask the writer for the issue number before doing anything else, and wait for the answer.

## Sources, and how to read them

Prefer local clones, read at the upstream tip without changing their checkout:

| Source | Local clone (if present) | Read with |
| ------ | ------------------------ | --------- |
| MDN content | `~/github/mdn/content` | `git -C <clone> fetch -q upstream main` (or `origin`), then `git -C <clone> show upstream/main:<path>` and `git -C <clone> grep <pattern> upstream/main -- <path>` |
| BCD | `~/github/mdn/browser-compat-data` | the same |
| WPT | `~/github/mdn/wpt` | the same |
| browser-specs | `~/github/mdn/browser-specs` | the same |

Never run `git checkout`, `git switch`, `git pull` or `git stash` in these clones: the writer may have work in progress there.
If a clone is missing, use the GitHub API (`gh api repos/<owner>/<repo>/contents/<path>`) or a raw URL instead.

Remote sources:

- **mdn/content issues and PRs:** `gh issue view <n> --repo mdn/content --json title,body,labels,url,comments`, `gh search issues`, `gh search prs`.
- **Bugzilla REST API** (no login needed for public bugs):
  - `curl -s "https://bugzilla.mozilla.org/rest/bug/<id>?include_fields=id,summary,status,resolution,product,component,keywords,whiteboard,depends_on,blocks,see_also,regressed_by,flags,url,cf_user_story,last_change_time"`
  - all comments: `curl -s "https://bugzilla.mozilla.org/rest/bug/<id>/comment"`
  - tracking and status flags for releases are fields named `cf_status_firefox<NNN>` and `cf_tracking_firefox<NNN>`; ask for `_all` (`include_fields=_all`) if you need them.
- **Gecko source** (GitHub mirror of mozilla-central): `https://raw.githubusercontent.com/mozilla-firefox/firefox/main/<path>`, or `gh api repos/mozilla-firefox/firefox/contents/<path>`.
  For a commit's diff use `https://github.com/mozilla-firefox/firefox/commit/<sha>.diff`; Bugzilla's "Pushed by" comments give the hg or GitHub commit for each landing.
- **Spec IDL:** `https://raw.githubusercontent.com/w3c/webref/curated/ed/idl/<series-shortname>.idl`.
  The curated files are per spec series, without the level, so CSS View Transitions Level 2 is in `css-view-transitions.idl` and HTML is in `html.idl`.
  The series shortname comes from browser-specs (`series.shortname`) or the BCD `spec_url`.

Network calls can be flaky. Retry a failed `gh` or `curl` call two or three times before reporting it as unavailable, and say in the report which sources you couldn't reach.

## Workflow

### 1. Read the issue

- Get the title, body, labels and comments.
  The `Firefox NNN` label gives the release; the `Content:*` label gives the area.
- Collect every Gecko bug the issue mentions: `bugzil.la/<id>`, `bugzilla.mozilla.org/show_bug.cgi?id=<id>`, and "Bug <id>" text.
- Note the issue's acceptance-criteria checklist state (BCD, release notes, experimental features), but verify each item yourself rather than trusting the ticks.

### 2. Read the bugs

For each bug:

- Read the summary, status, keywords (`dev-doc-needed`, `dev-doc-complete`), whiteboard, and all comments.
- Follow `depends_on`, `blocks`, `see_also` and `regressed_by` one level, and up to the meta bug if there is one.
  The meta bug usually says what the whole feature is; the issue's bug is often one step of it (for example "enable on Nightly").
- Find what actually landed: the patches attached to or pushed for the bug.
  Read the diffs for preference changes, WebIDL changes, and the WPT expectation changes under `testing/web-platform/meta/`.
- Look for later bugs that change the same preference or feature (search Bugzilla for the pref name, or read the meta bug's dependencies), so you can say what is planned next, for example "enabled on all channels in 162 by bug NNN".

### 3. Work out preferences, channels and platforms

- Find each preference in `modules/libpref/init/StaticPrefList.yaml`, as it is at the release, not just on `main`.
  Values such as `@IS_NIGHTLY_BUILD@`, `@IS_EARLY_BETA_OR_EARLIER@`, `@IS_NOT_ANDROID@` and `#ifdef` blocks decide the channel and platform.
- Check for overrides in `browser/app/profile/firefox.js` (desktop) and `mobile/android/app/geckoview-prefs.js` or `mobile/android/app/mobile.js` (Android).
- Say plainly which of these it is: release on all channels, release on desktop only or Android only, Nightly only (enabled by default there), or disabled by default behind a pref on every channel.

### 4. Map what is delivered against the feature

- Get the spec's IDL (for APIs), syntax (for CSS), or element and attribute definitions (for HTML), and list every entity in it.
- Compare with Gecko:
  - WebIDL in `dom/webidl/*.webidl`: `[Pref="..."]` or `[Func="..."]` attributes say which interfaces and members are gated by the pref.
  - CSS: the property or descriptor's `gecko_pref` or `enabled_in` in the Servo style system (`servo/components/style/`), and `layout/style/` for at-rules.
  - HTML attributes and keywords: the parser and element code, and the bug's patches.
  - WPT expectations in `testing/web-platform/meta/` show what passes or fails in Firefox.
- Mark each entity as **delivered**, **not delivered**, or **partial**, with the evidence (IDL file and line, patch, or WPT expectation).
- List anything Gecko ships that isn't in the spec, as non-standard.
- When the spec and the tests disagree, go with the spec and note the difference.

### 5. Check BCD

- Find the BCD feature for each entity (`api.X`, `api.X.member`, `css.at-rules.X`, `html.elements.X.attr`, …) at `upstream/main`.
- Report its current `firefox` and `firefox_android` data: `version_added`, `preview`, flags, `impl_url`.
- Search for BCD PRs, open and merged, that update these features for this work: `gh search prs --repo mdn/browser-compat-data "<feature or bug id>"`, and `gh pr list --repo mdn/browser-compat-data --search "<keyword>" --state all`.
- Say what is missing and what needs to change.
  The writer's BCD conventions:
  - a feature that is enabled only in Nightly gets `"version_added": "preview"` and an `impl_url` for the implementation bug;
  - a feature behind a pref that is off by default gets a `flags` entry;
  - `status` fields are generated automatically, so don't suggest editing them;
  - when a feature gains its second engine in a BCD PR, `experimental` must be set to `false` (lint requires it).

### 6. Find related MDN issues and PRs

- **Same release:** issues in mdn/content with the same `Firefox NNN` label that are part of the same feature (`gh search issues --repo mdn/content --label "Firefox NNN" <keywords>`).
- **Earlier releases:** issues for the same work under earlier `Firefox` labels, for example the implementation or Nightly issue before a release issue. Search for the bug ids and the feature name.
- **Open work on the same entities:** open issues and PRs in mdn/content (and BCD) that touch the same pages or features, including recent PRs that changed them (`git -C <content clone> log upstream/main -- <folder>`).
- Give each as a link with its number and title.

### 7. Assess the docs

- For each entity, check whether an MDN page exists (`files/en-us/<slug lowercased>/index.md` at `upstream/main`), and link to it as `https://developer.mozilla.org/en-US/docs/<slug>` if it does.
- Note guides and overview pages that cover the feature, and any whose content is now wrong or incomplete for Firefox.
- Docs describe the spec and cross-browser behaviour. Firefox-specific caveats belong in BCD or release notes, not on reference pages.
- Summarize what docs work is needed: new pages, updates, or none.

### 8. Check the Experimental features page

- Search `files/en-us/mozilla/firefox/experimental_features/index.md` at `upstream/main`, and in any open PR, for the preference names and feature names.
- Link to each matching section (`https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Experimental_features#<anchor>`).
- Propose additions, table updates (Nightly, Developer Edition, Beta and Release rows, each with version added and whether it's enabled by default), or removal once the feature ships on Release on all platforms.

### 9. Check release notes

- Look in the bug for a release-note request or suggestion: the `relnote-firefox` flag, and comments with "Release Note Request" or suggested wording.
- Check the release's notes (`files/en-us/mozilla/firefox/releases/<NNN>/index.md` at `upstream/main` and in open PRs), and earlier releases' notes, for entries on this feature.
  Search for the bug ids and the preference names.
- Suggest release-note text that matches what is actually delivered:
  - **Nightly-only or pref-gated work** goes under `## Experimental web features`, in this form:

    ```md
    - **Feature name** (Nightly): `pref.name`

      Short description of what is enabled and what it lets developers do.
      ([Firefox bug NNNNNNN](https://bugzil.la/NNNNNNN)).
    ```

  - **Released work** goes under the matching `### HTML`, `### CSS`, `### APIs` (and so on) heading, as one bullet ending with `([Firefox bug NNNNNNN](https://bugzil.la/NNNNNNN)).`
  - If the whole feature is delivered, the note can link to the API overview or guide. If only part is, name and link only the delivered parts.
  - Use MDN macros (`{{domxref()}}`, `{{cssxref()}}`, `{{HTMLElement()}}`) and one sentence per line.

## The report

Write the report to the session's scratchpad directory if there is one, otherwise to a temporary directory, never inside a clone.
Name it `mdn-evaluate-firefox-issue-<issue number>.md`.
Use these sections, in this order:

```md
# Evaluation: mdn/content#<n> — <issue title>

- Issue: <URL> (label: Firefox NNN)
- Bugs: <bug links with summaries>
- Evaluated: <date>; sources not reachable: <list or "none">

## Summary
<3–6 bullets: what it delivers, where, and the main MDN actions>

## What the feature delivers
<overview of the feature or spec; if partial, what part and the larger context; where it is released: Release, Nightly, behind a pref, desktop, Android>

## Preferences
<each pref, its default per channel and platform, with the source line; later changes planned>

## Browser compat data
<per feature: exists?, current Firefox data, PRs that update it, what's missing, summary of the BCD changes needed>

## Associated issues
### Same release
### Earlier releases
### Open issues and PRs on the same entities

## Docs
<summary of the docs work needed>
<table: entity | MDN page (link, or "no page") | delivered? | evidence | notes, with non-standard entities marked>

## Experimental features
<matching sections (links), and proposed additions, updates or removals>

## Release note
<existing or requested notes (links), earlier notes and experimental entries (links), suggested text>
```

Rules for the report:

- Back every claim with a source: a spec URL, a file and line, a bug comment, a test, or a PR. Say "not found" rather than guessing, and keep facts separate from your inferences.
- Use one sentence per line in prose.
- Write for a high-school reading level: explain jargon, and give the reason for a claim.

When the report is written, open it in VS Code with `code <path>`, and give the writer its full path and the Summary bullets.
