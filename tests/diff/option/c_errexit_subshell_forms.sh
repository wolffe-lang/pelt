set -e
(false; echo no) || echo sub-failed
x=$(false; echo no); echo "not-reached [$x]"
