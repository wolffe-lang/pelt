set -e
trap 'echo exit-trap $?' EXIT
(exit 3)
echo not-reached
