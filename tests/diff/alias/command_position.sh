alias hi='echo hello'
x=1 hi there
>/dev/null hi gone; echo "redir=$?"
2>/dev/null hi there
! hi bang >/dev/null; echo "bang=$?"
{ hi; } | cat
case x in x) hi case;; esac
alias x='y'
case x in x) echo patx;; y) echo paty;; esac
for hi in a; do echo "$hi"; done
