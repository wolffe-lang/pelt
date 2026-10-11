for c in a b c d - ']' '!' x; do
  case $c in [abc]) echo "$c set";; [!a-cx]) echo "$c complement";; *) echo "$c none";; esac
done
case - in [a-]) echo trailing-dash;; esac
case ']' in []]) echo leading-bracket;; esac
case a in [!]]) echo not-bracket;; esac
