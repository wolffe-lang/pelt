The oracle-of-record image (pelt#69)

tests/diff/ORACLE names the oracle of record and the second opinion by package
and by the sha256 of the programs the corpus runs: Arch's dash 0.5.13.4-1 and
bash 5.3.20-1, in this image. Its inputs are pinned, and they are the image's
identity:

  the base, docker.io/library/archlinux by registry digest (Containerfile),
  which already carries python 3.14.7-1 for the corpus runner;
  every package file by sha256 (packages.sha256): dash, libedit (dash's one
  dependency the base lacks) and bash, all from the archive's repositories of
  the base's date (2026-09-20).

Build (the network is used only to pull the base by digest and fetch the
pinned files; the build itself has none):

  podman pull docker.io/library/archlinux@sha256:8185e444e45ba166146b244b41f1cba2d7d91f3eddce533a839cc9591e0fa785
  tools/oracle-image

It refuses before any download if a line is malformed, UNAVAILABLE or outside
archive.archlinux.org, checks each file against its digest, refuses before the
build unless pacman, in the base and with no network, resolves the files
against what the base has installed, and refuses after the build unless the
image's /usr/bin/dash and /usr/bin/bash are the programs ORACLE names. The image id it prints is an observed value, not a pin; nothing
is published.

Run by that id:

  tools/oracle-container sha256:<64-hex-image-id> [--write] [area ...]
  tools/oracle-container sha256:<64-hex-image-id> [--write] --session [case ...]

The default is --check: nothing is written, the checkout is mounted read-only,
and every drifting case is named with its old and new lines (and every
second-opinion flag that would change). --write records. No host /usr or
package-database mounts, no network. $ORACLE_ENGINE names the engine.
