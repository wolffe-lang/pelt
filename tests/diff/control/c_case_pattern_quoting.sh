p='a*'; s='a*'
case abc in $p) echo var-is-pattern;; esac
case abc in "$p") echo no;; *) echo quoted-var-literal;; esac
case 'a*' in "$s") echo literal-match;; esac
case 'a*' in a\*) echo escaped;; esac
case abc in 'a'*) echo mixed;; esac
