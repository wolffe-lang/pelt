case '' in *) echo empty;; esac
case abc in a*c) echo mid;; esac
case abcabc in *b*b*) echo two;; esac
case abc in *abc*) echo both-empty;; esac
case abc in a*d) echo no;; *) echo none;; esac
case a/b in *) echo slash-in-case;; esac
