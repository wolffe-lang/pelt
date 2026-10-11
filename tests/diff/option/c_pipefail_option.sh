set -o pipefail; echo "st=$?"
set +o | grep pipefail
set +o pipefail; set +o | grep pipefail
