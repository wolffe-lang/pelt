case .hidden in *) echo dot-matched;; esac
case a/b in a?b) echo slash-matched;; esac
x=a/b/c; echo ${x#*/} ${x%%/*} ${x##*[/]}
