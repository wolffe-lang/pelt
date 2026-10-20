# a prefix assignment
command_not_found_handle() { echo "in: FOO=${FOO-unset} env=$(env | grep -c '^FOO=')"; }
FOO=bar nosuch; echo "after: FOO=${FOO-unset} st=$?"
