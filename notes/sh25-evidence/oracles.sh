#!/bin/bash
set -u
for sh in /usr/bin/dash /usr/bin/bash /home/mfwolffe/lanes/sh25/base-bin/native/pelt; do
 echo "SHELL=$sh"
 for arg in '--' '-LP' '-PL' '-- -x' 'foo -x' '-x' '-'; do
  "$sh" -c "pwd $arg >/dev/null; echo status=\$?"
 done
 for n in '12x' '+12x' '-12x' '0x12x' '078' ' 12x' '+' '-' '0x' '08x' '-0x1fx'; do
  "$sh" -c 'printf "%d\n" "$1"; echo status=$?' x "$n"
 done
 d=$(mktemp -d); (cd "$d" && "$sh" -c 'mkdir r; cd r; rmdir ../r; cd -P -e .; echo status=$?; pwd -P; echo pwdstatus=$?'); rmdir "$d"
done
