f() { echo brace; }; g() ( echo subshell; exit 3 ); h() if true; then echo if-body; fi
i() for x in 1; do echo for-body; done; j() while :; do echo while-body; break; done; k() case x in x) echo case-body;; esac
f; g; echo $?; h; i; j; k
