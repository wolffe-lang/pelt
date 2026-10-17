#!/bin/bash
# sh17: after the census, pax tools/mkpelt in a throwaway Ubuntu 24.04
# with clang, lld (ld.lld present, as pax CI has it) and binutils, against pelt REV
set -u
S=$HOME/lanes/sh17
REV=$1
until [ -f $S/logs/census.done ]; do sleep 30; done
podman run --rm -v $S/mkpelt/out:/out -v $S/mkpelt/work:/work docker.io/library/ubuntu:24.04 bash -c "
  apt-get update -q >/dev/null && apt-get install -y -q --no-install-recommends git curl ca-certificates clang lld binutils gcc libc6-dev >/dev/null &&
  ld.lld --version && clang --version | head -1 && gcc --version | head -1 && ldd --version | head -1 &&
  bash /out/mkpelt-run.sh $REV" > $S/logs/mkpelt.log 2>&1
echo mkpelt=$? >> $S/logs/mkpelt.log
sha256sum $S/mkpelt/out/pelt >> $S/logs/mkpelt.log
sha256sum $S/mkpelt/out/pelt >> $S/logs/mkpelt.log
echo done > $S/logs/mkpelt.done
