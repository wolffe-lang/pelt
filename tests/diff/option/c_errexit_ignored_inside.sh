set -e
f() { false; echo f-continues; }
if f; then echo then; fi
f || echo no
{ false; echo brace-continues; } && echo and
! { false; echo bang-continues; }
echo end
