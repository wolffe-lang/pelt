#!/bin/bash
# sh21: the baseline (pelt trunk be1a75d, no hook) on both tiers, and lope 5ac37df native+release
set -u
S=$HOME/lanes/sh21
export TMPDIR=$S/tmp
cd $S/pelt && git log --oneline -1
tools/fetch-toolchain; echo fetch=$?
tools/build --all; echo build=$?
mkdir -p $S/base && cp target/native/pelt $S/base/pelt-native && cp target/release/pelt $S/base/pelt-release && sha256sum $S/base/*
cd $S/lope && git log --oneline -1
tools/fetch-toolchain; echo lope-fetch=$?
tools/build --release; echo lope-build=$?
sha256sum target/release/lope
echo done
