# Contract for the monitoring bot

The bot never touches the graph. It appends rows to its own files and opens a pull request; a row enters the graph only when `make check` passes and a person merges.

## Files it writes

`data/raw/bot.sources.jsonl` and any of `data/raw/bot.{events,facts,roles,loans,flows,entities}.jsonl`. One JSON object per line. Field lists are in `SPEC.md`; the existing `dos3.*.jsonl` files are the closest worked example.

## Rules the validator enforces (`python3 tools/validate_rows.py --strict bot`)

1. Every claim row has a `prov` block: `asserted_by`, `source`, `locator`, `quote`, `confidence`.
2. `prov.source` points at a row in a sources file. For the bot, a source of kind `press`, `official` or `rating` must carry a full `url` (http/https, not truncated with "..."). No link, no row.
3. `asserted_by` is the voice making the claim, not the outlet printing it: `prosecution`, `rey`, `defence`, `regulator`, `rating_agency`, `company`, `press`, `analyst`.
4. `confidence` is `high`, `medium` or `low`. Use `medium` when only a headline or summary was read.
5. `quote` is at most 12 words, copied from the source.
6. Party ids are `org:`, `person:` or `auth:` plus a lowercase slug. Reuse an existing id (search `data/raw/*.entities.jsonl`) before minting one.
7. Event `category`, flow `instrument` and role `role` must be terms of `data/ontology.ttl`.
8. Ids are unique: `bot:event:0001`, `bot:fact:0001`, ... Never reuse or renumber.
9. Amounts are numbers; currency is `PYG` or `USD`.

## Rules a reviewer enforces (the validator cannot)

- Social media only as quoted by a news outlet; the outlet's article is the source.
- People appear only in publicly reported roles. No ID numbers, home addresses, family details or dates of birth. The validator warns on the obvious patterns; it does not catch everything.
- Everything is an allegation unless a court has ruled. Wording of `title_*` and `detail_*` must say who alleges.
- The quote really is in the linked page. The validator checks shape, not truth.

## Example

```json
{"id":"src:abc-2026-11-20-example","kind":"press","outlet":"ABC Color","title":"...","date":"2026-11-20","url":"https://www.abc.com.py/.../full-article-path/"}
{"id":"bot:event:0001","date":"2026-11-20","date_precision":"day","category":"supervisory","title_en":"...","title_es":"...","detail_en":"...","detail_es":"...","parties":["org:ueno-bank"],"amount":null,"currency":null,"prov":{"asserted_by":"regulator","source":"src:abc-2026-11-20-example","locator":"para. 3","quote":"...","confidence":"medium","note":""}}
```
