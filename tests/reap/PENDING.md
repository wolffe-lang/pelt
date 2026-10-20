# tests/reap — nothing pending

`tools/reap-witness` runs this corpus (`PELT_DIFF_DIR`): one case,
`hang/tree`, that times out on purpose, so that a harness's timeout is
seen ending the whole tree the case started. No case here is pending.
