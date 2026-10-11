alias say='echo said'
if true; then say a; fi
{ say b; }
! say c >/dev/null; echo $?
(say d); true && say e; true | say f
