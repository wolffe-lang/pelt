alias q='echo x'
command -v q
command -V q >/dev/null; echo "V=$?"
type q >/dev/null; echo "type=$?"
alias if='echo IF'; command -v if
