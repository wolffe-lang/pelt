#!/bin/bash
# sh23: one planted break, run locally (ruling #104 R2; RULES §7): the
# head (HEAD, the code at 497d104) in a scratch worktree with PATCH
# applied, both tiers built on kasumi's host, then the cases inside the
# lane's container (ctr.sh) under taskset -c 0-3. `full`: the whole
# corpus and every session on both tiers; `quick`: native, `simple/` and
# the autocd_* and cnf_* sessions. Each step's exit status in
# logs/plant-NAME/status; a build that fails is recorded and nothing runs
# (a compile error is not a red row).
# usage: plant.sh NAME PATCH full|quick
N=$1; P=$2; M=$3
S=$HOME/lanes/sh23
HEAD=${HEAD:-497d1041c44c1269c8236b9b2a9329239975dc44}
WT=$S/plant-wt
L=$S/logs/plant-$N
export TMPDIR=$S/tmp
rm -rf "$L"; mkdir -p "$L"
St=$L/status
[ -d "$WT" ] || git -C "$S/pelt" worktree add -q --detach "$WT" "$HEAD"
ln -sfn "$S/pelt/.wolf-bin" "$WT/.wolf-bin"
git -C "$WT" reset -q --hard "$HEAD" && git -C "$WT" clean -qfdx -e .wolf-bin
git -C "$WT" apply "$P"; echo "apply=$?" > "$St"
echo "head=$(git -C "$WT" rev-parse HEAD) patch=$(basename "$P") $(sha256sum "$P" | cut -c1-12) diffstat: $(git -C "$WT" diff --shortstat)" >> "$St"
(cd "$WT" && tools/build --all) > "$L/build.log" 2>&1; b=$?; echo "build=$b" >> "$St"
if [ $b -ne 0 ]; then echo done >> "$St"; exit 0; fi
sha256sum "$WT/target/native/pelt" "$WT/target/release/pelt" >> "$St"
SESS="autocd_bare autocd_hook autocd_invoked autocd_list autocd_not_dir autocd_off autocd_slash autocd_status autocd_wins autocd_words cnf_127 cnf_assign cnf_cd cnf_contexts cnf_redirect cnf_rerun cnf_skipped cnf_status cnf_words"
if [ "$M" = full ]; then
  T="native release"; DARGS=""; SARGS=""
else
  T="native"; DARGS="simple"; SARGS="$SESS"
fi
CTRDIR=$WT "$S/ctr.sh" bash -c '
  for t in '"$T"'; do
    taskset -c 0-3 tools/difftest --bin target/$t '"$DARGS"' > '"$L"'/diff-$t.log 2>&1; echo "diff-$t=$?"
    taskset -c 0-3 tools/session --bin target/$t '"$SARGS"' > '"$L"'/sess-$t.log 2>&1; echo "sess-$t=$?"
  done' >> "$St"
echo "ctr=$?" >> "$St"
echo done >> "$St"
