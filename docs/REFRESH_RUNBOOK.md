# Refresh runbook (for the agent that reviews, merges and republishes)

Run after each bot delivery. Everything is done from a clone of `VictorJServin/ueno-case-graph`. The public page is the artifact **"Ueno Bank Case File"**, slug `0db7f651-2eb0-4d14-bb00-da23bccae955`, which is shared publicly: every publish needs `shared_live: "public"`, `artifact_title: "Ueno Bank Case File"` and the current `base_version` from `get_artifact`.

Rules that do not bend: the page names people facing unproven allegations; nothing is published that breaks `SPEC.md` or the editorial rules in `docs/BOT_HANDOFF.md`; never publish from a failing build; never force-push; never edit rows that are already on `main` (corrections are new rows).

## 0. Is there anything to do?

List open pull requests: `gh api repos/VictorJServin/ueno-case-graph/pulls --jq '.[] | {number,title,head:.head.ref}'`.
No open pull request from `bot/inbox` means nothing to do: stop, change nothing, report "no new delivery".

## 1. Review the delivery (do not skip)

Read `inbox/runs/<run>.json` and every new line in `data/raw/bot.*.jsonl` on the branch.

Stop without merging, and report to the owner, if any of these is true:
- the pull request's `validate` check is not green;
- the diff touches anything outside `inbox/` and `data/raw/bot.*.jsonl`, or changes or deletes existing lines;
- a row breaks an editorial rule: an accusation stated as fact; a named relative or private person who is not a party to an official act; an ID number, address, date of birth, health detail or account number; third-party criminal history; an unverified accusation against a named person; a social-media link as the source; missing "presumed innocent" where a named person is under suspicion;
- a figure looks off by a factor of a thousand (guaraní "millones" versus "mil millones").

Items in `needs_human` do not block by themselves. Read them: if one says a row may break a rule, treat it as a stop; if it is a note about an unreconciled figure or a pending outcome, carry on and repeat the list in your report.

## 2. Merge and apply

```
gh api -X PUT repos/VictorJServin/ueno-case-graph/pulls/<n>/merge -f merge_method=squash
git pull --rebase origin main
pip install --break-system-packages -r requirements.txt
python3 tools/apply_run.py          # logs the run in data/updates.json ("What's new")
```

If an event refers to a party with no entity row, add the row to `data/raw/fix.entities.jsonl` (same shape as other entity rows, sourced to the event's source).

Payouts tab: if the manifest's `payouts` list is not empty, update the matching text and `refs` in `data/build_payouts.py` (and its `as_of` date). Change only what the new rows support; every sentence there must rest on a row id. If you are not sure how a point changes the tab, leave the tab as it is and say so in the report.

Update the two "data to <date>" / "public reporting up to <date>" strings in `site/js/overview.js` and `site/js/app.js` (English and Spanish) to the run's date.

## 3. Build and check

```
make check      # rows, graph, SHACL, vocabulary, payouts, updates, JavaScript syntax
make queries    # six saved queries must each return rows
make test       # end-to-end tests
make pub        # public copy; must end with "still mentioning: []"
```

Any failure: fix it if the cause is in your own edits; otherwise stop and report. Then serve `pub/` locally and load `#overview`, `#payouts`, `#timeline` and `#missing` in headless Chrome (`/usr/bin/google-chrome --headless=new --no-sandbox --dump-dom`); each must render and the overview must show the new "Updated" time.

## 4. Commit, push, publish

Commit and push to `main`. Then publish from `pub/` with `publish_files` (call `list_files` and `get_artifact` first). Always send `data/graph.json`, `data/graph.trig.txt`, `data/graph.ttl.txt`, `data/stats.json`, `data/README.md`, `data/updates.json`, `data/payouts.json`, plus any file under `js/`, `css/` or `index.html` that changed.

## 5. Report

Send the owner a short message: which run was applied, how many rows, the "what's new" lines, anything from `needs_human`, anything you left undone, and the triple count. If you stopped at step 1 or 3, say exactly why and what you need.

## Not part of the refresh

The missing-money estimate, the charges table on the Legal analysis tab, the written reports, and anything in `analysis/`. Do not touch them unattended.
