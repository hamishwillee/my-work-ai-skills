---
name: px4-docs-followup-review
description: Follow-up review of a PX4-Autopilot docs or board PR after an earlier (often AI-assisted) review round. Resolves review threads the author has fixed, pushes a commit with the unambiguously correct fixes (typos, formatting, changes the author has confirmed but not made), then posts one grouped review with inline comments and suggestions plus a summary listing the commit, non-line questions and still-outstanding threads. Use when the user asks for a follow-up, follow-on or re-review of a PX4 PR, or to "resolve fixed threads and post a review", or invokes /px4-docs-followup-review with a PR number.
---

# PX4 docs follow-up review

A follow-up round on a PR that has already had at least one review.
The user has authorized these writes for this workflow: pushing one commit to the PR branch, resolving review threads, and posting one review.
This overrides the read-only rule in `px4-board-doc-review`, `px4-gnss-doc-review`, `px4-rangefinder-doc-review` and `px4-doc-review`. Use those skills' references as checklists, but do the writes described here.

Argument: a PR number or URL (bare number means `PX4/PX4-Autopilot`). With no argument, use the PR for the current branch (`gh pr view`).

## 1. Gather

- `gh pr view <n> --json number,title,url,headRefName,headRepositoryOwner,maintainerCanModify,state,files`.
  Stop if the PR is closed or merged. If `maintainerCanModify` is false, skip the commit step and put the fixes in the review as suggestions instead; say so to the user.
- Fetch all reviews, PR comments, and review threads (with `id`, `isResolved`, `isOutdated`, `path`, `line`, and each comment's `databaseId`, author, body) in one GraphQL query. Save it to the scratchpad; it's large.
- Find the last review by the user. Its body lists what was asked and what was still open: that's the baseline.
- Diff the branch from the commit that review covered to the PR head (`git fetch <fork-url> <branch>` first, and make sure the local branch matches the PR head). Exclude binaries from the text diff, but list them.

## 2. Assess each open thread and each "still open" item

For every unresolved thread and every item in the last review's "still open" list, decide from the diff and from the author's replies:

- **Fixed**: resolve it.
- **Fixed except a mechanical remainder**: make the remainder in the commit, then resolve it.
- **Partly answered**: leave it open, and say what's still missing in the outstanding list.
- **Unanswered**: leave it open and list it as outstanding.

Check the author's new changes for regressions and new issues too:
- the board files (`boards/<vendor>/<board>/`), for dead code or leftovers the change exposed
- images: render SVGs (a scratchpad venv with `cairosvg`) and look at them, and check whether new assets are actually referenced
- CI status (`gh api repos/PX4/PX4-Autopilot/commits/<sha>/check-runs`)
- facts the author supplied, checked against their own sources (drawings, board files) where possible

For board, GNSS or rangefinder pages, use the matching specialist skill's references (page template, board-sources worksheet) for the checks. A follow-up round is scoped to what changed and what's still open; it isn't a full new review.

## 3. Commit the unambiguous fixes

Make only changes that are clearly correct and need no input from the author:
- typos, formatting, quote and backtick style, one sentence per line
- changes the author confirmed in a thread but didn't make
- edits that bring the page in line with the board source, where the fact itself is settled

Unit spacing needs the user's go-ahead first: PX4 prefers no space between a value and its unit symbol (`3V`, not `3 V`), and dimensions give the unit once, at the end (`36 x 42 x 8.63mm`).
Ask the user once whether to fix every case on the page, listing the lines, and make it one change in the commit.

Anything that's a content decision (adding images, removing a claim, a firmware change) goes in the review as a suggestion.
Docs-only changes are preferred. Leave firmware changes as suggestions unless the user says otherwise.

Then:
- run Prettier on the changed markdown (`cd docs && npx --no-install prettier --check <files>`)
- commit with the `/commit` skill: `docs(boards): ...` or a fitting scope, with the `Assisted-by:` trailer and no `Co-Authored-By`. Stage only the intended files, never submodule changes.
- push to the contributor's fork: `git push https://github.com/<owner>/<repo>.git HEAD:<headRefName>`

## 4. Resolve the fixed threads

Use `resolveReviewThread` (GraphQL) for each thread judged fixed in step 2, after the commit is pushed.

## 5. Post one grouped review

Post with `gh api repos/PX4/PX4-Autopilot/pulls/<n>/reviews --input <json>`, using `event: "COMMENT"` and `commit_id` set to the full SHA of the new head.

**Inline comments**, one per issue, each on the line it's about:
- Before posting, print each anchor line with `sed -n <line>p` and check it's the intended line. Never anchor on a blank line.
- Use `suggestion` blocks wherever the fix is concrete. An empty suggestion block deletes the line(s). Use `start_line`/`line` for multi-line ranges.
- Use `side: "RIGHT"` on lines in the head version.
- Keep comments terse: say what's wrong, give the evidence (`file:line`, a commit SHA), and ask one clear question. No contrast clauses ("X, not Y"): state the fact.

**Review body**, in this order:
1. A note that this is an AI review: `> [!NOTE]` / `> This is an AI review (Claude).`
2. "I've resolved the N threads that are now fixed, and pushed `<short-sha>` to your branch with these changes:", then a bullet per change with a bold label. Then: "Please pull before making further changes."
3. **New since the last review**: a one-line pointer to the inline comments, then any questions that can't go on a specific line (CI state, files the PR doesn't change, cross-file questions).
4. **Still open from earlier reviews**: one bullet per outstanding thread, linked as `https://github.com/PX4/PX4-Autopilot/pull/<n>#discussion_r<first-comment-databaseId>`, with what's still missing when it was partly answered.

Don't reply inside existing threads. A follow-up on an open thread goes in the "still open" bullet.

## 6. Report to the user

Give the review link, then:
- the commit SHA, and a line for each change
- the threads resolved
- each inline comment, in one line
- the outstanding list
- anything you couldn't verify (blocked URLs, unrendered assets), and any mistake made while posting

Keep it short. The user will read the PR itself.
