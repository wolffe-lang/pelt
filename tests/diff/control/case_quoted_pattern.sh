x='a*'
case abc in $x) echo glob;; esac
case abc in "$x") echo quoted;; *) echo literal;; esac
