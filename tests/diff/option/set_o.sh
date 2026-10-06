set -o errexit
case $- in *e*) echo on;; esac
set +o errexit
case $- in *e*) echo still;; *) echo off;; esac
