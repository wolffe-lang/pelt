# set -e and a handler that fails
command_not_found_handle() { return 3; }
set -e
nosuch || echo "or-list st=$?"
nosuch; echo "not reached?"
