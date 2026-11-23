.PHONY: check js payouts rows graph shapes store queries test pub hooks
check: rows graph shapes payouts js          ## what the commit hook and CI run (~35 s)
rows:   ; python3 tools/validate_rows.py --strict bot
graph:  ; python3 data/build_graph.py --quiet > build.log 2>&1 && grep -q "all checks passed" build.log && tail -1 build.log || (tail -40 build.log; exit 1)
shapes: ; python3 tools/validate_graph.py
js: ; for f in site/js/*.js; do node --check $$f || exit 1; done
payouts: ; python3 data/build_payouts.py && python3 data/build_updates.py
store:  ; python3 store/load.py
queries: store ; python3 store/load.py --all
test:   ; python3 tests/test_pipeline.py
pub:    ; rm -rf pub && cp -r site pub && python3 make_pub.py
hooks:  ; git config core.hooksPath hooks
