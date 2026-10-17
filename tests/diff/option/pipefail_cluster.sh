set -eo pipefail; set +o | grep -e errexit -e pipefail
set +eo pipefail; set +o | grep -e errexit -e pipefail
set -o errexit -o pipefail; set +o | grep -e errexit -e pipefail
set +e +o pipefail
o=$(set -o pipefail; set +o); eval "$o"; false | true; echo "reinput $?"
