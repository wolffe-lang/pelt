#!/bin/bash
# sh23: the baseline (pelt trunk 3b0bab9) on both tiers, kept as base/,
# and lope 5ac37df built at its own pin (release), for the session rows.
set -u
S=$HOME/lanes/sh23
export TMPDIR=$S/tmp CARGO_INCREMENTAL=0
cd $S/pelt && git log --oneline -1
tools/fetch-toolchain; echo fetch=$?
tools/build --all; echo build=$?
mkdir -p $S/base && cp target/native/pelt $S/base/pelt-native && cp target/release/pelt $S/base/pelt-release && sha256sum $S/base/*
cd $S/lope && git log --oneline -1
tools/fetch-toolchain; echo lope-fetch=$?
tools/build --release; echo lope-build=$?
sha256sum target/release/lope
echo done
