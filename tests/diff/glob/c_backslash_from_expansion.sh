p='a\*'; case 'a*' in $p) echo escaped-star;; esac
case 'ab' in $p) echo no;; *) echo not-wild;; esac
