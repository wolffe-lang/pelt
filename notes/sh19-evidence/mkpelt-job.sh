#!/bin/bash
# sh19 (sh18's, its paths moved; usage: REV TAG): pax tools/mkpelt in a throwaway Ubuntu 24.04 with clang, lld
# (ld.lld present, as pax CI has it) and binutils, against pelt REV
set -u
S=$HOME/lanes/sh19
REV=$1
TAG=$2
mkdir -p $S/mkpelt/out $S/mkpelt/work
rm -rf $S/mkpelt/work/pax $S/mkpelt/out/pelt
cp $S/mkpelt-run.sh $S/mkpelt/out/
podman run --rm -v $S/mkpelt/out:/out -v $S/mkpelt/work:/work docker.io/library/ubuntu:24.04 bash -c "
  apt-get update -q >/dev/null && apt-get install -y -q --no-install-recommends git curl ca-certificates clang lld binutils gcc libc6-dev >/dev/null &&
  ld.lld --version && clang --version | head -1 && gcc --version | head -1 && ldd --version | head -1 &&
  bash /out/mkpelt-run.sh $REV" > $S/logs/mkpelt-$TAG.log 2>&1
echo mkpelt=$? >> $S/logs/mkpelt-$TAG.log
sha256sum $S/mkpelt/out/pelt >> $S/logs/mkpelt-$TAG.log
sha256sum $S/mkpelt/out/pelt >> $S/logs/mkpelt-$TAG.log
echo done > $S/logs/mkpelt-$TAG.done
mkdir -p $S/sc && cp $S/mkpelt/out/pelt $S/sc/pelt-static-$TAG
