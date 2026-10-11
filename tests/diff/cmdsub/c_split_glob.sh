touch f1 f2
set -- $(echo 'a  b f*'); echo $# "$@"
set -- "$(echo 'a  b f*')"; echo $# "$@"
