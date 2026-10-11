(trap 'echo bye' EXIT; exit 3); echo $?
(trap 'echo bye; exit 9; echo no' EXIT; exit 3); echo $?
(trap 'echo status-in-trap=$?' EXIT; (exit 6)); echo $?
(trap 'echo at-eof' EXIT)
